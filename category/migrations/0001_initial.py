# Generated by Django 5.0.2 on 2024-04-16 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('desc', models.TextField(blank=True, max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='photos/catgories')),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
            },
        ),
    ]
