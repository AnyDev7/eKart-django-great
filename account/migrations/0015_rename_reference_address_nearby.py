# Generated by Django 5.0.7 on 2024-07-16 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_address_reference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='reference',
            new_name='nearby',
        ),
    ]