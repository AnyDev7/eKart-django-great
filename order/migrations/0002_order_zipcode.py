# Generated by Django 5.0.2 on 2024-06-13 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='zipcode',
            field=models.CharField(default=None, max_length=10, verbose_name='CP'),
            preserve_default=False,
        ),
    ]