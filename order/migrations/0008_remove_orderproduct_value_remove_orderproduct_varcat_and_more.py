# Generated by Django 5.0.2 on 2024-06-22 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_rename_order_note_order_note_and_more'),
        ('store', '0019_alter_product_description_alter_stockvar_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='value',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='varcat',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.stockvar', verbose_name='Variaciones'),
        ),
    ]