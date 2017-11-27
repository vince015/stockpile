import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from rest_framework.response import Response
from rest_framework import status

from stockpile_app.models import (Item,
                                  Transaction,
                                  Sale)
from stockpile_app.serializers import (ItemSerializer,
                                       TransactionSerializer,
                                       SaleSerializer)
from stockpile_app.forms import SaleForm

INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."
NOT_CREW = "You are authenticated as {0}, but are not authorized to access this page. Would you like to login to a different account?"

def user_login(request):

    try:
        # Redirection
        template = 'stockpile_app/login.html'
        redirect = request.GET.get('next', '/stockpile/home')

        context_dict = dict()
        context_dict['redirect_to'] = redirect

        # if not request.user.is_anonymous() and not is_crew(request.user):
        #     messages.error(request, NOT_CREW.format(request.user))

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect)
                else:
                    messages.error(request, INACTIVE_USER)
                    return render(request, template)
            else:
                messages.error(request, INVALID_CREDENTIALS)
                return render(request, template, context_dict)

    except Exception as e:
        raise

    return render(request, template, context_dict)

@login_required()
def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/stockpile/home')

# Create your views here.
@login_required()
def dashboard(request):

    try:
        context_dict = dict()
        template = 'stockpile_app/dashboard.html'

        items = Item.objects.all()[:18]
        context_dict['items'] = items

    except Exception as ex:
        return server_error(request)

    return render(request, template, context_dict)

def processor(request):

    try:
        context_dict = dict()
        template = 'stockpile_app/processor.html'

        transactions = Transaction.objects.all().order_by('date')
        serializer = TransactionSerializer(transactions, many=True)
        context_dict['transactions'] = serializer.data

    except Exception as ex:
        return server_error(request)

    return render(request, template, context_dict)

def item_search(request):

    try:
        context_dict = dict()
        template = 'stockpile_app/item_search.html'

        if request.method == 'POST':
            q = request.POST.get('q')
            if q:
                items = Item.objects.filter(description__icontains=q)
                context_dict['items'] = items
            else:
                items = Item.objects.all()[:18]
                context_dict['items'] = items

    except Exception as e:
        raise e

    return render(request, template, context_dict)

@login_required()
def transaction_add(request):

    try:
        if request.method == 'POST':
            order_data = json.loads(request.POST.get('order_data')) or []

            if order_data:
                transaction = Transaction.objects.create(author=request.user,
                                                         count=len(order_data))

                for item in order_data:
                    sale_data = {
                        'item': int(item.get('id')),
                        'quantity': int(item.get('qty')),
                        'transaction': transaction.id
                    }
                    sale_form = SaleForm(sale_data)
                    if sale_form.is_valid():
                        sale_form.save()
                    else:
                        return JsonResponse(sale_form.errors, status=400)

            detail = {'created': transaction.id}
            return JsonResponse(detail, status=200)
        else:
            detail = {'error': 'Only POST method is allowed'}
            return JsonResponse(detail, status=405)

    except Exception as e:
        detail = {'error': str(e)}
        return JsonResponse(detail, status=500)

@login_required()
def transaction_get(request, id):

    try:
        if request.method == 'GET':
            instance = Transaction.objects.get(id=id)
            serializer = TransactionSerializer(instance)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            detail = {'error': 'Only GET method is allowed'}
            return Response(detail, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        detail = {'error': str(e)}
        return Response(detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required()
def transaction_latest(request):

    try:
        context_dict = dict()
        template = 'stockpile_app/transaction_latest.html'

        if request.method == 'POST':
            transactions = Transaction.objects.all().order_by('-date')[:15]
            context_dict['transactions'] = transactions

    except Exception as e:
        raise e

    return render(request, template, context_dict)
