import os
from csv import DictReader

from django.core.management.base import BaseCommand
from django.conf import settings

from dishes.models import Ingredient


DATAFILES_DIR = os.path.join(settings.BASE_DIR.parent.parent, 'data')

FILENAME = 'ingredients.csv'

FIELDS = ['name', 'measurement_unit']


class Command(BaseCommand):
    """If you need to reload the data from the CSV file,
    database with tables"""

    help = 'Loads data from csv files to models'

    def handle(self, *args, **kwargs):
        path_to_file = os.path.join(DATAFILES_DIR, FILENAME)
        with open(path_to_file, newline='', encoding='utf8') as csvfile:
            created = 0
            for row in DictReader(csvfile, FIELDS):
                obj, create = Ingredient.objects.get_or_create(**row)
                created += create
            print(
                f'From file {FILENAME} created '
                f'{created} objects.'
            )
