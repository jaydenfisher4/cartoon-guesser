# Generated by Django 5.1.6 on 2025-02-28 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_cartooncharacter_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartooncharacter',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]
