from django import forms
from stockpile_app.models import (Item, Transaction, Particular)

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

class ParticularForm(forms.ModelForm):

    class Meta:
        model = Particular
        fields = [
                    'quantity',
                    'subtotal'
                ]
        widgets = {
            'subtotal': forms.TextInput(attrs={'type': 'number',
                                               'class': 'form-control',
                                               'placeholder': 'Subtotal',
                                               'readonly': True}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if self.instance:
            if self.instance.item.stock < quantity:
                error = 'Quantity, {0}, cannot be more than stock, {1}.'.format(quantity, self.instance.item.stock)
                raise forms.ValidationError(error,)

        return quantity