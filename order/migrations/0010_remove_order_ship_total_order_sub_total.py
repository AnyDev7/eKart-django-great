# Generated by Django 5.0.2 on 2024-07-02 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_orderproduct_options_order_ship_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ship_total',
        ),
        migrations.AddField(
            model_name='order',
            name='sub_total',
            field=models.FloatField(default=0, verbose_name='Subtotal'),
        ),
    ]
