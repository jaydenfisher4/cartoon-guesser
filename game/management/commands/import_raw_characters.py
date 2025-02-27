from django.core.management.base import BaseCommand
from game.models import CartoonCharacter
import json
import os

class Command(BaseCommand):
    help = 'Imports raw character data from a JSON file into CartoonCharacter model'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the raw JSON file')

    def handle(self, *args, **options):
        json_path = options['json_file']
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"File {json_path} not found"))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            characters = json.load(f)

        for fields in characters:
            # Ensure all required fields are present
            required_fields = ['name', 'show', 'network', 'is_main', 'release_year', 'still_airing', 'gender']
            if not all(field in fields for field in required_fields):
                self.stdout.write(self.style.ERROR(f"Skipping {fields.get('name', 'unknown')}: Missing required fields"))
                continue

            # Check for duplicates
            if CartoonCharacter.objects.filter(name=fields['name']).exists():
                self.stdout.write(self.style.WARNING(f"Skipping duplicate: {fields['name']}"))
                continue

            try:
                # Create the character instance
                CartoonCharacter.objects.create(
                    name=fields['name'],
                    show=fields['show'],
                    network=fields['network'],
                    is_main=fields['is_main'],
                    release_year=fields['release_year'],
                    still_airing=fields['still_airing'],
                    gender=fields['gender'],
                    image_url=fields.get('image_url', '')  # Optional field, default to empty string
                )
                self.stdout.write(self.style.SUCCESS(f"Added {fields['name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding {fields['name']}: {e}"))