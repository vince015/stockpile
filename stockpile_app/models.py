import uuid
import decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.db.models import signals

class Transaction(models.Model):

    type_choice = (
        ('IN', 'in'),
        ('OUT', 'out')
    )
    status_choice = (
        ('N', 'new'),
        ('R', 'ready'),
        ('D', 'done'),
        ('C', 'cancel')
    )

    number = models.CharField(max_length=32,
                              null=False,
                              blank=False)
    transaction_type = models.CharField(max_length=3,
                                        choices=type_choice,
                                        default='OUT')
    status = models.CharField(max_length=2,
                              choices=status_choice,
                              default='N')
    timestamp = models.DateTimeField(blank=False,
                                     null=True,
                                     auto_now=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               default=None)
    assignee = models.CharField(max_length=64,
                                null=True,
                                blank=True)
    remarks = models.CharField(max_length=500,
                               null=True,
                               blank=True)

class Item(models.Model):
    description = models.CharField(max_length=256,
                                   null=True)
    unit = models.CharField(max_length=256,
                            null=True,
                            blank=True)
    stock = models.PositiveSmallIntegerField(blank=True,
                                             null=True,
                                             default=0)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                null=True,
                                validators=[MinValueValidator(decimal.Decimal('0.00'))],
                                default=0.0)

    def __str__(self):
      return self.description

class Particular(models.Model):

    transaction = models.ForeignKey(Transaction,
                                    related_name='particulars',
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    default=None)
    item = models.ForeignKey(Item,
                             related_name='item',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             default=None)
    quantity = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                default=1)
    subtotal = models.DecimalField(max_digits=7,
                                  decimal_places=2,
                                  null=True,
                                  validators=[MinValueValidator(decimal.Decimal('0.00'))],
                                  default=0.01)