# Generated by Django 5.0.2 on 2024-05-23 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_varcat_options_alter_variation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='low_price',
            field=models.FloatField(blank=True, default=0, verbose_name='Precio con descuento'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='varcat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.varcat', verbose_name='Catalogo variación'),
        ),
    ]
