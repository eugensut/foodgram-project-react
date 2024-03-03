import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from dishes.models import Ingredient


DATAFILES_DIR = os.path.join(settings.BASE_DIR, 'data')

FILENAME = 'ingredients.json'


class Command(BaseCommand):
    """If you need to reload the data from the JSON file,
    database with tables"""

    help = 'Loads data from csv files to models'

    def handle(self, *args, **kwargs):
        path_to_file = os.path.join(DATAFILES_DIR, FILENAME)
        with open(path_to_file, encoding='utf8') as json_file:
            created = 0
            for row in json.load(json_file):
                obj, create = Ingredient.objects.get_or_create(**row)
                created += create
            print(
                f'From file {FILENAME} created '
                f'{created} objects.'
            )
