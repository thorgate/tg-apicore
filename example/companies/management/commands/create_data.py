from django.core.management.base import BaseCommand

from companies.factories import create_full_example_data


class Command(BaseCommand):
    help = "Create test data"

    def handle(self, *args, **options):
        create_full_example_data()
