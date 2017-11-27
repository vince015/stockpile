from django import forms
from stockpile_app.models import (Item, Sale, Transaction)

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
                    'description',
                    'unit',
                    'stock',
                    'price'
                ]
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Description'}),
            'stock': forms.NumberInput(attrs={'step': 1,
                                              'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'step': 0.01,
                                              'class': 'form-control'})
        }

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = [
                    'quantity',
                    'item',
                    'transaction'
                ]

class TransactionForm(forms.ModelForm):

    class Transaction:
        model = Sale
        fields = [
                    'status',
                    'date',
                    'count',
                    'author'
                ]
