# Generated by Django 5.0.2 on 2024-06-22 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0005_cartitem_user_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.FloatField(blank=True, default=0, verbose_name='Precio'),
        ),
    ]