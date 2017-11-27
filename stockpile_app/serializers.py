from rest_framework import serializers

from stockpile_app.models import (Item,
                                  Transaction,
                                  Sale)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        depth = 1

class TransactionSerializer(serializers.ModelSerializer):
    items = SaleSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'status', 'date', 'author', 'items')
        depth = 2
