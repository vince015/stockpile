import json
import traceback
import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView

from stockpile_app.models import (Transaction)
from util.util import is_crew, is_cashier

LOGGER = logging.getLogger('django')

INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."
NOT_CREW = "You are authenticated as {0}, but are not authorized to access this page. Would you like to login to a different account?"

def get_home(user):
    if user.is_superuser:
        redirect = "/stockpile/dashboard"
    elif is_crew(user):
        redirect = "/stockpile/counter"
    elif is_cashier(user):
        redirect = "/stockpile/cashier"
    else:
        redirect = "/stockpile/403"

    return redirect

def user_login(request):

    try:
        # Redirection
        template = "login.html"
        context_dict = dict()

        redirect = request.GET.get("next", get_home(request.user))
        context_dict["redirect_to"] = redirect

        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect)

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect = get_home(user)
                    return HttpResponseRedirect(redirect)
                else:
                    messages.error(request, INACTIVE_USER)
                    return render(request, template)
            else:
                messages.error(request, INVALID_CREDENTIALS)
                return render(request, template, context_dict)

        return render(request, template, context_dict)

    except:
        raise

@login_required()
def user_logout(request):

    logout(request)
    return HttpResponseRedirect("/stockpile/login")

@login_required()
def notifications(request):

    try:
        template = "notifications.html"
        context_dict = dict()

        transactions = Transaction.objects.filter(transaction_type="out")
        context_dict["transactions"] = transactions.order_by('-timestamp')[:10]

    except:
        context_dict["error"] = "Unable to retrieve Transactions"
        LOGGER.error(traceback.format_exc())

    finally:
        return render(request, template, context_dict)

class Error403(TemplateView):
    template_name = "error/403.html"
