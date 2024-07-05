# Generated by Django 5.0.2 on 2024-06-11 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_city_account_country_account_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=50)),
                ('address_line_1', models.CharField(max_length=50, verbose_name='Direccion')),
                ('address_line_2', models.CharField(blank=True, max_length=50, verbose_name='...Direccion')),
                ('country', models.CharField(max_length=50, verbose_name='Pais')),
                ('state', models.CharField(max_length=50, verbose_name='Estado')),
                ('city', models.CharField(max_length=50, verbose_name='Ciudad')),
            ],
            options={
                'verbose_name': 'Direccion',
                'verbose_name_plural': 'Direcciones',
            },
        ),
    ]