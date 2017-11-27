from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from stockpile_app.views import views, item, sale, transaction, processor

home_url = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^home/$', views.dashboard, name='home'),
    # url(r'^processor/$', views.processor, name='processor'),
    url(r'^items/search$', views.item_search, name='items_search'),
    url(r'^items/$', login_required(item.ItemsList.as_view()), name="item_list"),
    url(r'^items/json/$', login_required(item.ItemsListJson.as_view()), name="item_list_json"),
    url(r'^items/add/$', item.add, name="item_add"),
    url(r'^items/edit/(?P<item_id>[0-9]+)$', item.edit, name="item_edit"),
    url(r'^sales/$', login_required(sale.SaleList.as_view()), name="sale_list"),
    url(r'^sales/json/$', login_required(sale.SaleListJson.as_view()), name="sale_list_json"),
    url(r'^transactions/$', login_required(transaction.TransactionList.as_view()), name="transaction_list"),
    url(r'^transactions/json/$', login_required(transaction.TransactionListJson.as_view()), name="transaction_list_json"),
    url(r'^transactions/detail/(?P<transaction_id>[0-9]+)$', transaction.detail, name='transactions_detail'),
    url(r'^transactions/add$', views.transaction_add, name='transactions_add'),
    url(r'^transactions/latest$', views.transaction_latest, name='transaction_latest'),
    url(r'^processor/$', processor.ProcessorList.as_view(), name='processor'),
    url(r'^processor/transactions/$', processor.listing, name='processor_listing'),
    url(r'^processor/detail/(?P<transaction_id>[0-9]+)$', processor.process_transaction_details, name='process_transaction_details')
]


urlpatterns = home_url