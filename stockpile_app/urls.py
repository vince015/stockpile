from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from stockpile_app.views import (home,
                                 dashboard,
                                 cashier,
                                 counter)

home_url = [
    url(r'^$', home.user_login, name='home'),
    url(r'^login/$', home.user_login, name='login'),
    url(r'^logout/$', home.user_logout, name='logout'),
    url(r'^403/$', home.Error403.as_view(), name='403'),
    url(r'^transaction/latest$', home.transaction_latest, name='transaction_latest')
]

dashboard_url = [
    url(r'^dashboard/$', login_required(dashboard.DashboardPage.as_view()), name='dashboard'),
    url(r'^dashboard/transactions$', dashboard.dashboard_transactions, name='dashboard_transactions'),
    url(r'^dashboard/transactions/details/(?P<transaction_id>[0-9]+)$', dashboard.dashboard_transactions_details, name='dashboard_transactions_details'),
    url(r'^dashboard/transactions/edit/(?P<transaction_id>[0-9]+)$', dashboard.dashboard_transactions_edit, name='dashboard_transactions_edit'),
    url(r'^items/$', login_required(dashboard.ItemsPage.as_view()), name='items'),
    url(r'^items/json$', login_required(dashboard.ItemsListJson.as_view()), name='items_json'),
    url(r'^items/edit/(?P<item_id>[0-9]+)$', dashboard.items_edit, name='item_edit'),
    url(r'^items/delete/(?P<item_id>[0-9]+)$', dashboard.items_delete, name='item_delete'),
    url(r'^transactions/$', login_required(dashboard.TransactionsPage.as_view()), name='transactions'),
    url(r'^transactions/json$', login_required(dashboard.TransactionListJson.as_view()), name='transactions_json'),
    url(r'^transactions/edit/(?P<transaction_id>[0-9]+)$', dashboard.transactions_edit, name='transaction_edit'),
    url(r'^transactions/delete/(?P<transaction_id>[0-9]+)$', dashboard.transactions_delete, name='transaction_delete'),
]

cashier_url = [
    url(r'^cashier/$', cashier.cashier, name='cashier'),
    url(r'^cashier/item/search$', cashier.item_search, name='cashier_item_search'),
    url(r'^cashier/transaction/add$', cashier.transaction_add, name='cashier_transaction_add')
]

counter_url = [
    url(r'^counter/$', login_required(counter.CounterPage.as_view()), name='counter'),
    url(r'^counter/transactions$', counter.transactions, name='counter_transactions'),
    url(r'^counter/transactions/details/(?P<transaction_id>[0-9]+)$', counter.transactions_details, name='counter_transactions_details'),
    url(r'^counter/transactions/edit/(?P<transaction_id>[0-9]+)$', counter.transactions_edit, name='counter_transactions_edit')
]

urlpatterns = (
    home_url +
    dashboard_url +
    cashier_url +
    counter_url
)