from django.db import migrations
import json

def forwards_func(apps, schema_editor):
    UserPreference = apps.get_model('game', 'UserPreference')
    for pref in UserPreference.objects.all():
        # Migrate excluded_shows (TextField) to excluded_shows_json (JSONField)
        if pref.excluded_shows:
            show_list = [s.strip() for s in pref.excluded_shows.split(',') if s.strip()]
            pref.excluded_shows_json = show_list
        else:
            pref.excluded_shows_json = []
        
        # Migrate excluded_characters (TextField) to excluded_characters_json (JSONField)
        if pref.excluded_characters:
            char_list = [c.strip() for c in pref.excluded_characters.split(',') if c.strip()]
            pref.excluded_characters_json = char_list
        else:
            pref.excluded_characters_json = []
        
        # Clear old TextFields and save
        pref.excluded_shows = None
        pref.excluded_characters = None
        pref.save()

def backwards_func(apps, schema_editor):
    UserPreference = apps.get_model('game', 'UserPreference')
    for pref in UserPreference.objects.all():
        pref.excluded_shows = ','.join(pref.excluded_shows_json)
        pref.excluded_characters = ','.join(pref.excluded_characters_json)
        pref.save()

class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_add_json_fields'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
        migrations.RemoveField(model_name='userpreference', name='excluded_shows'),
        migrations.RemoveField(model_name='userpreference', name='excluded_characters'),
        migrations.RenameField(model_name='userpreference', old_name='excluded_shows_json', new_name='excluded_shows'),
        migrations.RenameField(model_name='userpreference', old_name='excluded_characters_json', new_name='excluded_characters'),
    ]
