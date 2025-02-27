from django.db import migrations
import json

def load_initial_data(apps, schema_editor):
    CartoonCharacter = apps.get_model("cartoon_guesser", "CartoonCharacter")
    CartoonSuggestion = apps.get_model("cartoon_guesser", "CartoonSuggestion")
    with open("initial_data.json", "r") as f:
        data = json.load(f)
        for obj in data:
            if obj["model"] == "cartoon_guesser.cartooncharacter":
                CartoonCharacter.objects.create(**obj["fields"])
            elif obj["model"] == "cartoon_guesser.cartoonsuggestion":
                CartoonSuggestion.objects.create(**obj["fields"])

class Migration(migrations.Migration):
    dependencies = [("cartoon_guesser", "0001_initial")]
    operations = [migrations.RunPython(load_initial_data)]