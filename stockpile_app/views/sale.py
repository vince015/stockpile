from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages

from stockpile_app.models import (Item,
                                  Transaction,
                                  Sale)
from stockpile_app.forms import (ItemForm)
import json
from datetime import datetime

def add(request):

    try:
        template = 'stockpile_app/item_form.html'
        context_dict = dict()

        if request.method == "POST":
            form = ItemForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully added Item.')

                return redirect('/system/items')
        else:
            form = ItemForm()
            context_dict['form'] = form

            return render(request, template, context_dict)
    except Exception as e:
        raise e
    finally:
        pass

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
            template = 'stockpile_app/item_form.html'

            form = ItemForm(instance=instance)
            context_dict['form'] = form

            return render(request, template, context_dict)

    except Exception as e:
        raise e
    finally:
        pass

class SaleList(TemplateView):
    template_name = 'stockpile_app/sale.html'

class SaleListJson(BaseDatatableView):
    model = Sale
    columns = ['item', 'quantity', 'date', 'price']
    order_columns = ['item', 'quantity', 'transaction.date', 'item.price']

    def get_initial_queryset(self):
        return Sale.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(item__description__icontains=search)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.item.description,
                item.quantity,
                item.transaction.date.strftime("%Y-%m-%d"),
                item.item.price
            ])
        return json_data
