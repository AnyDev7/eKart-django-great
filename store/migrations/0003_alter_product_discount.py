# Generated by Django 5.0.2 on 2024-04-17 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_options_product_data_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
