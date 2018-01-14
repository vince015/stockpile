from datetime import datetime

from django.contrib import admin
from django.core import urlresolvers
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from stockpile_app.models import (Transaction,
                                  Item,
                                  Particular)

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class ItemResource(resources.ModelResource):

    class Meta:
        model = Item
        fields = ('id', 'description', 'unit', 'stock', 'price')

class ItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'description', 'unit', 'stock', 'price')
    list_display_links = ['id']
    search_fields = ['id', 'description', 'price']
    list_per_page = 50
    resource_class = ItemResource
admin.site.register(Item, ItemAdmin)


class TransactionResource(resources.ModelResource):

    class Meta:
        model = Transaction
        fields = ('id', 'number', 'transaction_type', 'status', 'timestamp', 'author__username')

class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'number', 'transaction_type', 'status', 'timestamp', 'author__username')
    list_display_links = ['id']
    list_filter = ('transaction_type', 'status')
    search_fields = ['id', 'number', 'transaction_type']
    list_per_page = 50
    resource_class = TransactionResource

    def author__username(self, obj):
        if obj.author:
            link = urlresolvers.reverse("admin:auth_user_change", args=[obj.author.id])
            return '<a href="{0}">{1}</a>'.format(link, obj.author.username)
        else:
            return ''
    author__username.allow_tags = True
admin.site.register(Transaction, TransactionAdmin)

class ParticularResource(resources.ModelResource):

    class Meta:
        model = Particular
        fields = ('id', 'transaction__number', 'item__description', 'transaction__timestamp', 'quantity')

class ParticularAdmin(ImportExportModelAdmin):
    list_display = ('id', 'transaction__number', 'item__description', 'transaction__timestamp', 'quantity')
    list_display_links = ['id']
    search_fields = ['id', 'transaction__number', 'item__description', 'transaction__timestamp']
    list_per_page = 50
    resource_class = ParticularResource

    def transaction__number(self, obj):
        if obj.transaction:
            link = urlresolvers.reverse("admin:stockpile_app_transaction_change", args=[obj.transaction.id])
            return '<a href="{0}">{1}</a>'.format(link, obj.transaction.number)
        else:
            return ''
    transaction__number.allow_tags = True

    def item__description(self, obj):
        if obj.item:
            link = urlresolvers.reverse("admin:stockpile_app_item_change", args=[obj.item.id])
            return '<a href="{0}">{1}</a>'.format(link, obj.item.description)
        else:
            return ''
    item__description.allow_tags = True

    def transaction__timestamp(self, obj):
        if obj.transaction:
            link = urlresolvers.reverse("admin:stockpile_app_transaction_change", args=[obj.transaction.id])
            return '<a href="{0}">{1}</a>'.format(link, datetime.strftime(obj.transaction.timestamp, "%Y-%m-%d"))
        else:
            return ''
    transaction__timestamp.allow_tags = True
admin.site.register(Particular, ParticularAdmin)
