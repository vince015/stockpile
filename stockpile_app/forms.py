from django import forms
from stockpile_app.models import (Item, Transaction)

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

class TransactionForm(forms.ModelForm):

    class Meta:
        status_choice = (
            ('N', 'New'),
            ('R', 'Ready'),
            ('D', 'Done'),
            ('C', 'Cancel')
        )
        model = Transaction
        fields = [
                    'number',
                    'status',
                    'assignee',
                    'remarks'
                ]
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'S.I. No.'}),
            'status': forms.Select(choices=status_choice),
            'assignee': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Assignee'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Remarks'}),
        }
