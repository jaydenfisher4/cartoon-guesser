# In game/migrations/000x_convert_text_to_manytomany.py
from django.db import migrations

def forwards_func(apps, schema_editor):
    UserPreference = apps.get_model('game', 'UserPreference')
    Show = apps.get_model('game', 'Show')
    CartoonCharacter = apps.get_model('game', 'CartoonCharacter')
    for pref in UserPreference.objects.all():
        # Convert comma-separated shows
        show_names = [s.strip() for s in pref.excluded_shows.split(',') if s.strip()]
        for name in show_names:
            show, _ = Show.objects.get_or_create(name=name)
            pref.excluded_shows.add(show)
        # Convert comma-separated characters
        char_names = [c.strip() for c in pref.excluded_characters.split(',') if c.strip()]
        for name in char_names:
            char = CartoonCharacter.objects.filter(name=name).first()
            if char:
                pref.excluded_characters.add(char)

class Migration(migrations.Migration):
    dependencies = [('game', '0007_alter_cartooncharacter_show_alter_show_name')]  # Replace with actual previous migration
    operations = [
        migrations.RunPython(forwards_func),
    ]