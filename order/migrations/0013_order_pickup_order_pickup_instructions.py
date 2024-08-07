# Generated by Django 5.0.7 on 2024-07-19 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_order_shipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pickup',
            field=models.BooleanField(default=False, verbose_name='¿Retiro en almacen?'),
        ),
        migrations.AddField(
            model_name='order',
            name='pickup_instructions',
            field=models.CharField(default='', max_length=200, verbose_name='Comentarios para recolección'),
            preserve_default=False,
        ),
    ]
