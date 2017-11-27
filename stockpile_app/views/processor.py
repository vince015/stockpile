from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from stockpile_app.models import (Item,
                                  Transaction,
                                  Sale)
from stockpile_app.forms import (ItemForm)
import json
from datetime import datetime

from django.views.generic import TemplateView

class ProcessorList(TemplateView):
    template_name = 'stockpile_app/processor.html'

def listing(request):

    try:
        context_dict = dict()
        template_name = 'stockpile_app/transaction_new.html'

        transaction_list = Transaction.objects.filter(status='N').order_by('date')
        paginator = Paginator(transaction_list, 25) # Show 25 contacts per page

        page = request.GET.get('page')
        context_dict['transactions'] = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context_dict['transactions'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        if paginator.num_pages > 0:
            context_dict['transactions'] = paginator.page(paginator.num_pages)
    except Exception as e:
        print(str(e))

    return render(request, template_name, context_dict)

def process_transaction_details(request, transaction_id):

    try:
        context_dict = dict()
        template_name = 'stockpile_app/transaction_detail_process.html'

        transaction = Transaction.objects.get(pk=transaction_id)
        context_dict['transaction'] = transaction

        sales = Sale.objects.filter(transaction=transaction)
        context_dict['sales'] = sales

    except Exception as e:
        print(str(e))

    return render(request, template_name, context_dict)
