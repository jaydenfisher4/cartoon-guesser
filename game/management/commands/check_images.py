# game/management/commands/check_images.py
from django.core.management.base import BaseCommand
from game.models import CartoonCharacter
import requests
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Checks all character image URLs and updates image_restricted field'

    def handle(self, *args, **options):
        characters = CartoonCharacter.objects.all()
        total = characters.count()
        self.stdout.write(f"Checking {total} character images...")

        for i, character in enumerate(characters, 1):
            if not character.image_url:
                character.image_restricted = True
                character.save()
                logger.info(f"Marked {character.name} as restricted (no URL)")
                self.stdout.write(f"[{i}/{total}] {character.name}: No URL - marked restricted")
                continue

            try:
                # Send a HEAD request to check if the image is accessible
                response = requests.head(character.image_url, timeout=5)
                if response.status_code == 200 and 'image' in response.headers.get('Content-Type', '').lower():
                    # Check CORS headers (optional, but simulates browser behavior)
                    if 'Access-Control-Allow-Origin' not in response.headers:
                        character.image_restricted = True
                        logger.warning(f"{character.name} lacks CORS headers")
                    else:
                        character.image_restricted = False
                        logger.info(f"{character.name} image OK")
                else:
                    character.image_restricted = True
                    logger.warning(f"{character.name} returned {response.status_code}")
                character.save()
                self.stdout.write(f"[{i}/{total}] {character.name}: {'Restricted' if character.image_restricted else 'OK'}")
            except requests.RequestException as e:
                character.image_restricted = True
                character.save()
                logger.error(f"Error checking {character.name}: {str(e)}")
                self.stdout.write(f"[{i}/{total}] {character.name}: Error - marked restricted")

        self.stdout.write(self.style.SUCCESS("Image check complete"))