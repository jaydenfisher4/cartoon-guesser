from django.db import migrations
import json

def load_initial_data(apps, schema_editor):
    CartoonCharacter = apps.get_model("game", "CartoonCharacter")
    CartoonSuggestion = apps.get_model("game", "CartoonSuggestion")
    with open("initial_data.json", "r") as f:
        data = json.load(f)
        for obj in data:
            if obj["model"] == "game.cartooncharacter":
                CartoonCharacter.objects.create(**obj["fields"])
            elif obj["model"] == "game.cartoonsuggestion":
                CartoonSuggestion.objects.create(**obj["fields"])

class Migration(migrations.Migration):
    dependencies = [("game", "0001_initial")]  
    operations = [migrations.RunPython(load_initial_data)]