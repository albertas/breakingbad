from django.core.management.base import BaseCommand

from breakingbadapi_task.utils import load_character_data_from_external_api


class Command(BaseCommand):
    help = "Load Character data from https://breakingbadapi.com"

    def handle(self, *args, **options):
        load_character_data_from_external_api()

        message = "Successfully loaded Characters from https://breakingbadapi.com"
        self.stdout.write(self.style.SUCCESS(message))
