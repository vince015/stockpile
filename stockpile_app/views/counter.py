import traceback
import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

from stockpile_app.models import (Transaction,
                                  Particular)
from stockpile_app.serializers import (TransactionSerializer)

from django.utils.decorators import method_decorator
from util.util import is_crew

LOGGER = logging.getLogger('django')

@method_decorator(user_passes_test(is_crew, login_url="/stockpile/403"), name='dispatch')
class CounterPage(TemplateView):
    template_name = "counter/counter.html"

@login_required()
def transactions(request):

    try:
        context_dict = dict()
        template_name = "counter/transactions.html"

        transactions = Transaction.objects.filter(status="R", transaction_type="out").order_by("timestamp")
        paginator = Paginator(transactions, 25)

        page = request.GET.get("page")
        context_dict["transactions"] = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context_dict["transactions"] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        if paginator.num_pages > 0:
            context_dict["transactions"] = paginator.page(paginator.num_pages)

    except:
        context_dict["error"] = "Unable to retrieve Transaction"
        LOGGER.error(traceback.format_exc())

    finally:
        return render(request, template_name, context_dict)

@login_required()
def transactions_details(request, transaction_id):

    try:
        context_dict = dict()
        template_name = "counter/transactions_details.html"

        transaction = Transaction.objects.get(pk=transaction_id)
        context_dict["transaction"] = transaction

        particulars = Particular.objects.filter(transaction=transaction)
        context_dict["particulars"] = particulars

    except:
        context_dict["error"] = "Unable to retrieve Transaction"
        LOGGER.error(traceback.format_exc())

    finally:
        return render(request, template_name, context_dict)

@login_required()
def transactions_edit(request, transaction_id):

    try:
        context_dict = dict()
        instance = Transaction.objects.get(pk=transaction_id)

        if request.method == "POST":
            data = {
                "number": instance.number,
                "status": request.POST.get("status"),
                "author": {
                    "id": instance.author.id,
                    "username": instance.author.username
                }
            }

            serializer = TransactionSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)

    except:
        LOGGER.error(traceback.format_exc())
        error = {"error": "Unable to add Transaction"}
        return JsonResponse(error, status=500)
