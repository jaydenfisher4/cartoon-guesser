from django.db import migrations, models
from django.contrib.auth.models import User

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '__latest__'),
    ]
    operations = [
        migrations.CreateModel(
            name='CartoonCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('show', models.CharField(max_length=100)),
                ('network', models.CharField(max_length=50)),
                ('is_main', models.BooleanField(default=True)),
                ('release_year', models.IntegerField()),
                ('still_airing', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=20)),
                ('image_url', models.URLField(max_length=999, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartoonSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('submitter_ip', models.GenericIPAddressField(null=True, blank=True)),
            ],
        ),
    ]