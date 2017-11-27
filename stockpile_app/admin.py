from django.contrib import admin
from django.core import urlresolvers
from stockpile_app.models import (Item,
                                  Transaction,
                                  Sale)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'unit', 'stock', 'price')
    list_display_links = ['id']
    search_fields = ['id', 'description', 'price']
    list_per_page = 50
admin.site.register(Item, ItemAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'author_name')
    list_display_links = ['id']
    search_fields = ['id', 'status']
    list_per_page = 50

    def author_name(self, obj):
        if obj.author:
            link = urlresolvers.reverse("admin:auth_user_change", args=[obj.author.id])
            return '<a href="{0}">{1}</a>'.format(obj.author.id, obj.author.username)
        else:
            return '--'
    author_name.allow_tags = True
admin.site.register(Transaction, TransactionAdmin)

class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'item_id', 'transaction_id')
    list_display_links = ['id']
    search_fields = ['id']
    list_per_page = 50

    def item_id(self, obj):
        if obj.item:
            link = urlresolvers.reverse("admin:stockpile_app_item_change", args=[obj.item.id])
            return '<a href="{0}">{1}</a>'.format(obj.item.id, obj.item.description)
        else:
            return '--'
    item_id.allow_tags = True

    def transaction_id(self, obj):
        if obj.transaction:
            link = urlresolvers.reverse("admin:stockpile_app_transaction_change", args=[obj.transaction.id])
            return '<a href="{0}">{0}</a>'.format(obj.transaction.id)
        else:
            return '--'
    transaction_id.allow_tags = True
admin.site.register(Sale, SaleAdmin)
