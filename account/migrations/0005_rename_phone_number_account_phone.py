# Generated by Django 5.0.2 on 2024-06-12 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
