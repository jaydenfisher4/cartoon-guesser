from django.db import migrations, models
from django.contrib.auth.models import User

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '__latest__'),
    ]
    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartoonCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('show', models.ForeignKey(on_delete=models.CASCADE, to='game.Show')),
                ('network', models.CharField(max_length=50)),
                ('is_main', models.BooleanField(default=True)),
                ('release_year', models.IntegerField()),
                ('still_airing', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=20)),
                ('image_url', models.URLField(blank=True, max_length=999, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartoonSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('submitter_ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to='auth.User')),
                ('excluded_shows', models.JSONField(blank=True, default=list)),
                ('excluded_characters', models.JSONField(blank=True, default=list)),
            ],
        ),
    ]