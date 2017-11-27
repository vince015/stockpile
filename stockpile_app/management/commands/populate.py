import csv
import os
import random

from django.core.management.base import BaseCommand
from stockpile_app.models import Item

class Command(BaseCommand):

    def handle(self, *args, **options):
        dirname = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dirname, 'inventory.csv')

        with open(filename, 'rt', encoding='utf8') as csvfile:
            item_reader = csv.reader(csvfile, delimiter=',')
            for row in item_reader:
                if row[1]:
                    item = Item.objects.create(unit=row[0],
                                               description=row[1],
                                               price=random.randrange(1, 999),
                                               stock=random.randrange(1, 999))
