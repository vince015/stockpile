import os
import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    def create_groups(self):
        if not Group.objects.filter(name='Cashier').exists():
            group = Group.objects.create(name='Cashier')

        if not Group.objects.filter(name='Crew').exists():
            Group.objects.create(name='Crew')

    def create_users(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dirname, 'users.csv')

        with open(filename, 'rt', encoding='utf8') as csvfile:
            item_reader = csv.reader(csvfile, delimiter=',')
            # username,password,hint
            for row in item_reader:
                username = row[0]
                password = row[1]

                new_user = User.objects.create(username=username,
                                               password=password)

                if username == 'cashier':
                    group = Group.objects.get(name='Cashier')
                    group.user_set.add(new_user)
                elif username == 'crew':
                    group = Group.objects.get(name='Crew')
                    group.user_set.add(new_user)

    def handle(self, *args, **options):

        self.create_groups()
        self.create_users()
