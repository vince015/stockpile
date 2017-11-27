from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from stockpile_app.models import (Item,
                                  Transaction,
                                  Sale)
from stockpile_app.forms import (ItemForm)
import json


@login_required()
def edit(request, item_id):

    try:
        context_dict = dict()
        instance = Item.objects.get(pk=item_id)

        if request.method == "POST":
            form = ItemForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully edited Item No. {0}.'.format(instance.id))
                return redirect('/stockpile/items')
        else:
            template = 'stockpile_app/item_edit.html'

            form = ItemForm(instance=instance)
            context_dict['form'] = form

            return render(request, template, context_dict)

    except Exception as e:
        messages.error(request, 'Unable to edit Item.')
        return redirect('/stockpile/items')

@login_required()
def detail(request, transaction_id):

    try:
        context_dict = dict()
        template = 'stockpile_app/transaction_detail.html'

        instance = Transaction.objects.get(pk=transaction_id)
        context_dict['sales'] = Sale.objects.filter(transaction=instance)
        context_dict['transaction'] = instance

        return render(request, template, context_dict)

    except Exception as e:
        messages.error(request, 'Unable to get Transaction details.')
        return redirect('/stockpile/transactions')

class TransactionList(TemplateView):
    template_name = 'stockpile_app/transaction.html'

class TransactionListJson(BaseDatatableView):
    model = Transaction
    columns = ['id', 'date', 'count', 'status', 'author']
    order_columns = ['id', 'date', 'count', 'status', 'author']

    def get_initial_queryset(self):
        return Transaction.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            search = int(search)
            qs = qs.filter(id=search)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            status_choice = {
                'N': 'New',
                'S': 'Seen',
                'D': 'Done',
                'C': 'Cancel'
            }
            json_data.append([
                item.id,
                item.date.strftime("%Y-%m-%d"),
                item.count,
                status_choice.get(item.status, 'New'),
                item.author.username
            ])
        return json_data
