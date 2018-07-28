import json
import traceback
import logging

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from stockpile_app.models import (Item,
                                  Transaction)
from stockpile_app.serializers import (TransactionSerializer)

from util.util import is_cashier

LOGGER = logging.getLogger('django')

SHOWN_ITEM = 10

def get_recent_items():
    recent_items = []
    exclude_list = []

    transactions = Transaction.objects.all().order_by('-created', '-timestamp')
    for transaction in transactions:
        for particular in transaction.particulars.all():
            if particular.item not in recent_items:
                recent_items.append(particular.item)
                exclude_list.append(particular.item.id)

    items = Item.objects.all().exclude(id__in=exclude_list)
    for item in items:
        if len(recent_items) < SHOWN_ITEM:
            recent_items.append(item)
        else:
            break

    return recent_items

@login_required()
@user_passes_test(is_cashier, login_url="/stockpile/403")
def cashier(request):

    try:
        template = "cashier/cashier.html"
        context_dict = dict()

        if request.method == "GET":
            context_dict["items"] = get_recent_items()
            return render(request, template, context_dict)

    except:
        raise

@login_required()
def item_search(request):

    try:
        template = "cashier/item_search.html"
        context_dict = dict()

        if request.method == "POST":
            q = request.POST.get("q")
            if q:
                print('dammmmn')
                items = Item.objects.filter(description__icontains=q)
            else:
                print('fuuuck')
                items = get_recent_items()

            context_dict["items"] = items

    except:
        context_dict["error"] = "Unable to retrieve Items"
        LOGGER.error(traceback.format_exc())

    finally:
        print(context_dict)
        return render(request, template, context_dict)

@login_required()
def transaction_add(request):

    try:
        if request.method == "POST":
            transaction_data = {
                "number": request.POST.get("number"),
                "transaction_type": "OUT",
                "status": "N",
                "assignee": request.POST.get("assignee"),
                "remarks": request.POST.get("remarks"),
                "author": {
                    "id": request.user.id,
                    "username": request.user.username
                },
                "particulars": []
            }

            """[{'id': '6', 'qty': 1, 'price': 927}, {'id': '8', 'qty': 1, 'price': 232}]"""
            items = json.loads(request.POST.get('items')) or []
            for item in items:
                item_id = item.get("id")
                qty = int(item.get("qty"))
                price = float(item.get("price", "0.01"))
                subtotal = qty * price

                particular_data = {
                    "quantity": qty,
                    "subtotal": subtotal,
                    "item": {
                        "price": price,
                        "id": item_id
                    }
                }
                transaction_data["particulars"].append(particular_data)

            serializer = TransactionSerializer(data=transaction_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)

    except:
        LOGGER.error(traceback.format_exc())
        error = {"error": "Unable to add Transaction"}
        return JsonResponse(error, status=500)
