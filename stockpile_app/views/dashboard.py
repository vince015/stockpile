import traceback
import logging

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView

from stockpile_app.models import (Transaction,
                                  Particular,
                                  Item)
from stockpile_app.serializers import (TransactionSerializer)
from stockpile_app.forms import (ItemForm,
                                 TransactionForm,
                                 ParticularForm)

LOGGER = logging.getLogger('django')

@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/stockpile/403"), name='dispatch')
class DashboardPage(TemplateView):
    template_name = "dashboard/dashboard.html"

@login_required()
def dashboard_transactions(request):

    try:
        context_dict = dict()
        template_name = "dashboard/transactions_new.html"

        transactions = Transaction.objects.filter(status="N", transaction_type="out").order_by("timestamp")
        paginator = Paginator(transactions, 20)

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
def dashboard_transactions_details(request, transaction_id):

    try:
        context_dict = dict()
        template_name = "dashboard/transactions_detail.html"

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
def dashboard_transactions_edit(request, transaction_id):

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

@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/stockpile/403"), name='dispatch')
class ItemsPage(TemplateView):
    template_name = "dashboard/items.html"

class ItemsListJson(BaseDatatableView):
    model = Item
    columns = ['id', 'description', 'stock', 'price']
    order_columns = ['id', 'description', 'stock', 'price']

    def get_initial_queryset(self):
        return Item.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(description__icontains=search)
        return qs

@login_required()
def items_edit(request, item_id):

    try:
        context_dict = dict()
        instance = Item.objects.get(pk=item_id)

        if request.method == "POST":
            form = ItemForm(request.POST, instance=instance)
            context_dict["form"] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully edited Item No. {0}.'.format(item_id))
                return redirect('/stockpile/items')
        else:
            template = "dashboard/items_edit.html"

            form = ItemForm(instance=instance)
            context_dict["form"] = form

            return render(request, template, context_dict)

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        messages.error(request, 'Unable to edit Item No. {0}.'.format(item_id))
        return redirect('/stockpile/items')

'''
@login_required()
def items_delete(request, item_id):

    try:
        context_dict = dict()
        instance = Item.objects.get(pk=item_id)
        instance.delete()

        messages.success(request, 'Successfully deleted Item No. {0}.'.format(item_id))
        return redirect('/stockpile/items')

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        messages.error(request, 'Unable to edit Item No. {0}.'.format(item_id))
        return redirect('/stockpile/items')
'''

@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/stockpile/403"), name='dispatch')
class TransactionsPage(TemplateView):
    template_name = "dashboard/transactions.html"

class TransactionListJson(BaseDatatableView):
    model = Transaction
    columns = ['id', 'number', 'date', 'type', 'assignee', 'author']
    order_columns = ['id', 'number', 'timestamp', 'transaction_type', 'status', 'author']

    def get_initial_queryset(self):
        return Transaction.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            try:
                search = int(search)
                qs = qs.filter(Q(id=search) |
                               Q(number__icontains=search))
            except ValueError:
                qs = qs.filter(Q(number__icontains=search) |
                               Q(status__icontains=search) |
                               Q(timestamp__icontains=search) |
                               Q(assignee__icontains=search)|
                               Q(author__username__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            status_choice = {
                'N': 'New',
                'R': 'Ready',
                'D': 'Done',
                'C': 'Cancel'
            }

            if item.author:
                author = item.author.username
            else:
                author = ''
            json_data.append([
                item.id,
                item.number,
                item.timestamp.strftime("%Y-%m-%d"),
                status_choice.get(item.status, ''),
                author,
                item.assignee
            ])
        return json_data

@login_required()
def transactions_edit(request, transaction_id):

    try:
        context_dict = dict()
        instance = Transaction.objects.get(pk=transaction_id)

        if request.method == "POST":
            form = TransactionForm(request.POST, instance=instance)
            context_dict["form"] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully edited Transaction No. {0}.'.format(instance.id))
                return redirect('/stockpile/transactions')
        else:
            template = "dashboard/transactions_edit.html"

            form = TransactionForm(instance=instance)
            context_dict["form"] = form

            particulars = Particular.objects.filter(transaction=instance)
            context_dict["particulars"] = particulars

            return render(request, template, context_dict)

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        messages.error(request, 'Unable to edit Transaction No {0}.'.format(transaction_id))
        return redirect('/stockpile/transactions')

@login_required()
def particulars_edit(request, particular_id):

    try:
        context_dict = dict()
        instance = Particular.objects.get(pk=particular_id)

        if request.method == "POST":
            form = ParticularForm(request.POST, instance=instance)
            context_dict["form"] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully edited particular No. {0}.'.format(instance.id))
                return redirect('/stockpile/particulars')
        else:
            template = "dashboard/particulars_edit.html"

            form = ParticularForm(instance=instance)
            context_dict["form"] = form

            return render(request, template, context_dict)

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        messages.error(request, 'Unable to edit particular No {0}.'.format(particular_id))
        return redirect('/stockpile/transactions')

'''
@login_required()
def transactions_delete(request, transaction_id):

    try:
        if request.method == "POST":
            context_dict = dict()
            instance = Transaction.objects.get(pk=transaction_id)
            raise
            instance.delete()

            messages.success(request, 'Successfully deleted Transaction No. {0}.'.format(transaction_id))
            return redirect('/stockpile/transactions')

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        messages.error(request, 'Unable to delete Transaction No. {0}'.format(transaction_id))
        return redirect('/stockpile/transactions')
'''