from rest_framework import serializers
from django.contrib.auth.models import User

from stockpile_app.models import (Transaction,
                                  Particular,
                                  Item)

import json
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Item
        fields = ('description', 'unit', 'stock', 'price', 'id')

class ParticularSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Particular
        fields = ('id', 'quantity', 'subtotal', 'item')
        read_only_fields = ('id',)

    def validate(self, data):
        try:
            item_data = data.get('item')
            item = Item.objects.get(**item_data)
            qty = data.get('quantity', 0)

            if qty > item.stock:
                msg = 'Quantity {0} for Item {1} is greater than its stocks {2}'.format(qty, item.description, item.stock)
                raise serializers.ValidationError(msg)

            return super(ParticularSerializer, self).validate(data)

        except:
            raise

    def create(self, validated_data):
        try:
            item_data = validated_data.pop('item')
            item = Item.objects.get(id=item_data)

            particular = Particular.objects.create(item=item,
                                                   **validated_data)

            return particular

        except:
            raise

class TransactionSerializer(serializers.ModelSerializer):
    particulars = ParticularSerializer(many=True, required=False)
    author = UserSerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'number', 'transaction_type', 'status', 'timestamp', 'assignee', 'remarks', 'particulars', 'author')
        read_only_fields = ('id', 'timestamp')

    def create(self, validated_data):
        try:
            particulars_data = validated_data.pop('particulars')

            author_data = validated_data.pop('author')
            author = User.objects.get(**author_data)

            transaction = Transaction.objects.create(author=author,
                                                     **validated_data)
            for particular_data in particulars_data:
                item_data = particular_data.pop('item')
                item = Item.objects.get(**item_data)

                Particular.objects.create(item=item,
                                          transaction=transaction,
                                          **particular_data)

            return transaction

        except:
            raise

    def update(self, instance, validated_data):
        try:
            if 'particulars' in validated_data:
                particulars_data = validated_data.pop('particulars')

            author_data = validated_data.pop('author')
            author = User.objects.get(**author_data)
            instance.author = author

            instance.number = validated_data.get('number', instance.number)
            instance.transaction_type = validated_data.get('validated_data', instance.transaction_type)
            instance.status = validated_data.get('status', instance.status)
            instance.assignee = validated_data.get('assignee', instance.assignee)
            instance.remarks = validated_data.get('remarks', instance.remarks)
            instance.save()

            return instance

        except:
            raise
