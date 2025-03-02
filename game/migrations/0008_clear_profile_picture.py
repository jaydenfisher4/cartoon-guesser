from django.db import migrations

def clear_profile_pictures(apps, schema_editor):
    UserPreference = apps.get_model('game', 'UserPreference')
    # Option 1: Clear all profile_picture data (simplest)
    UserPreference.objects.all().update(profile_picture=None)
    
    # Option 2: If you want to keep URLs for later use, save them elsewhere
    # For example, add a temporary field (requires prior migration to add it)
    # UserPreference.objects.update(old_profile_picture=F('profile_picture'), profile_picture=None)

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0007_remove_cartoonsuggestion_name_and_more'),  
    ]

    operations = [
        migrations.RunPython(clear_profile_pictures, reverse_code=migrations.RunPython.noop),
    ]