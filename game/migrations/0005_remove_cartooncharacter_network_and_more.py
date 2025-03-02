from django.db import migrations, models

def migrate_show_data(apps, schema_editor):
    CartoonCharacter = apps.get_model('game', 'CartoonCharacter')
    Show = apps.get_model('game', 'Show')
    
    # Update each Show with data from its first associated CartoonCharacter
    for show in Show.objects.all():
        characters = CartoonCharacter.objects.filter(show=show)
        if characters.exists():
            first_char = characters.first()
            show.network = first_char.network
            show.release_year = first_char.release_year
            show.still_airing = first_char.still_airing
            show.save()

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0004_alter_cartooncharacter_name_alter_show_name'), 
    ]

    operations = [
        # Add fields to Show with temporary defaults
        migrations.AddField(
            model_name='show',
            name='network',
            field=models.CharField(max_length=50, default='Unknown'),
        ),
        migrations.AddField(
            model_name='show',
            name='release_year',
            field=models.IntegerField(default=2000),
        ),
        migrations.AddField(
            model_name='show',
            name='still_airing',
            field=models.BooleanField(default=False),
        ),
        # Migrate data from CartoonCharacter to Show
        migrations.RunPython(migrate_show_data),
        # Remove fields from CartoonCharacter
        migrations.RemoveField(
            model_name='cartooncharacter',
            name='network',
        ),
        migrations.RemoveField(
            model_name='cartooncharacter',
            name='release_year',
        ),
        migrations.RemoveField(
            model_name='cartooncharacter',
            name='still_airing',
        ),
    ]