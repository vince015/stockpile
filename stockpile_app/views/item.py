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
def add(request):

    try:
        template = 'stockpile_app/item_add.html'
        context_dict = dict()

        if request.method == "POST":
            form = ItemForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully added new Item.')
                return redirect('/stockpile/items')
        else:
            form = ItemForm()
            context_dict['form'] = form

            return render(request, template, context_dict)

    except Exception as e:
        messages.error(request, 'Unable to add Item.')
        return redirect('/stockpile/items')

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

class ItemsList(TemplateView):
    template_name = 'stockpile_app/item.html'

class ItemsListJson(BaseDatatableView):
    model = Item
    columns = ['id', 'description', 'stock', 'price']
    order_columns = ['id', 'description', 'stock', 'price']

    def get_initial_queryset(self):
        return Item.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        print('search {0}'.format(json.dumps(self.request.GET, indent=2)))
        if search:
            qs = qs.filter(description__icontains=search)
        return qs