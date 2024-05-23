# Generated by Django 5.0.2 on 2024-04-24 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockVar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='VarCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'variacion',
                'verbose_name_plural': 'variaciones',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='stockvar',
            field=models.ManyToManyField(to='store.stockvar'),
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('varcat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.varcat')),
            ],
            options={
                'verbose_name': 'valor de variacion',
                'verbose_name_plural': 'valores de variaciones',
            },
        ),
        migrations.AddField(
            model_name='stockvar',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.variation'),
        ),
    ]
