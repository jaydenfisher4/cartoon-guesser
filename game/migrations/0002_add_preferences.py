from django.db import migrations, models
from django.contrib.auth.models import User

def migrate_show_data(apps, schema_editor):
    Show = apps.get_model('game', 'Show')
    CartoonCharacter = apps.get_model('game', 'CartoonCharacter')
    for char in CartoonCharacter.objects.all():
        if char.show:
            show, _ = Show.objects.get_or_create(name=char.show)
            char.show_temp = show
            char.save()

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
        ('auth', '__latest__'),
    ]
    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cartooncharacter',
            name='show_temp',
            field=models.ForeignKey(on_delete=models.CASCADE, to='game.Show', null=True),
        ),
        migrations.RunPython(migrate_show_data),
        migrations.RemoveField(model_name='cartooncharacter', name='show'),
        migrations.RenameField(model_name='cartooncharacter', old_name='show_temp', new_name='show'),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to='auth.User')),
                ('excluded_shows', models.JSONField(default=list, blank=True)),
                ('excluded_characters', models.JSONField(default=list, blank=True)),
            ],
        ),
    ]