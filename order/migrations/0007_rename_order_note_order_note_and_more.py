# Generated by Django 5.0.2 on 2024-06-22 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_options_alter_orderproduct_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_note',
            new_name='note',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_number',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_total',
            new_name='total',
        ),
    ]
