from django.db.models.signals import post_save
import json
from django.dispatch import receiver
from stockpile_app.models import Transaction
from stockpile_app.serializers import TransactionSerializer
from channels import Group

@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):

    serializer = TransactionSerializer(instance)

    print("Sending notification...")
    Group('notif').send(
        {
            "text": json.dumps(serializer.data)
        }
    )