import uuid
import decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.db.models import signals

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
                                validators=[MinValueValidator(decimal.Decimal('0.01'))],
                                default=0.0)

class Transaction(models.Model):

    status_choice = (
        ('N', 'new'),
        ('S', 'seen'),
        ('D', 'done'),
        ('C', 'cancel')
    )

    status = models.CharField(max_length=2,
                              choices=status_choice,
                              default='N')
    date = models.DateTimeField(blank=False,
                                null=True,
                                auto_now_add=True)
    count = models.PositiveSmallIntegerField(blank=True,
                                             null=True,
                                             default=0)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               default=None)

class Sale(models.Model):
    quantity = models.PositiveSmallIntegerField(blank=False,
                                                null=True)
    item = models.ForeignKey(Item,
                             related_name='specifics',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             default=None)
    transaction = models.ForeignKey(Transaction,
                                    related_name='items',
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    default=None)

    def clean(self):
        if self.quantity > self.item.stock:
            detail = 'Quantity for item, {0}, cannot be grater than its stock ({1}).'.format(self.item.description,
                                                                                             self.item.stock)
            raise ValidationError({'quantity': _(detail)})

    def save(self, *args, **kwargs):
        qty = getattr(self, 'quantity', 0)
        self.item.stock = self.item.stock - qty;
        self.item.save()

        super(Sale, self).save(*args, **kwargs)
