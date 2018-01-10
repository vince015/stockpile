import logging
import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from stockpile_app.models import Transaction, Particular
from stockpile_app.serializers import (TransactionSerializer)

from channels import Group

LOGGER = logging.getLogger('django')


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):

    if instance.status == "D":
        particulars = Particular.objects.filter(transaction=instance)

        for particular in particulars:
            if instance.transaction_type == "OUT":
                particular.item.stock = particular.item.stock - particular.quantity
            elif instance.transaction_type == "IN":
                particular.item.stock = particular.item.stock + particular.quantity
            particular.item.save()

    serializer = TransactionSerializer(instance)
    LOGGER.info("Sending notification...")
    Group('notif').send(
        {
            "text": json.dumps(serializer.data)
        }
    )
