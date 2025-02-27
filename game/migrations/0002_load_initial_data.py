from django.db import migrations

def load_initial_data(apps, schema_editor):
    from django.core.management import call_command
    call_command('loaddata', 'initial_data', app_label='game')

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(load_initial_data),
    ]