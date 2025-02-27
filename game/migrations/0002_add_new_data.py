from django.db import migrations
import os
import json

def add_new_data(apps, schema_editor):
    Show = apps.get_model('game', 'Show')
    CartoonCharacter = apps.get_model('game', 'CartoonCharacter')
    fixture_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'new_data.json')

    # Check if new_data.json exists
    if not os.path.exists(fixture_path):
        print("No new_data.json found in game/fixtures/, skipping data load.")
        return

    # Load the JSON file
    with open(fixture_path, 'r', encoding='utf-8') as f:
        new_characters = json.load(f)

    # Process each character
    for char_data in new_characters:
        show_name = char_data.get('show')
        if not show_name:
            print(f"Skipping character {char_data.get('name', 'unknown')}: No show specified.")
            continue

        # Create or get the Show
        show, _ = Show.objects.get_or_create(name=show_name)

        # Create the CartoonCharacter if it doesn’t exist
        CartoonCharacter.objects.get_or_create(
            name=char_data['name'],
            defaults={
                'show': show,
                'network': char_data.get('network', 'Unknown'),
                'is_main': char_data.get('is_main', True),
                'release_year': char_data.get('release_year', 0),
                'still_airing': char_data.get('still_airing', False),
                'gender': char_data.get('gender', 'Unknown'),
                'image_url': char_data.get('image_url', ''),
            }
        )

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(add_new_data),
    ]