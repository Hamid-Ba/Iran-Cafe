# Generated by Django 4.1 on 2022-09-18 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('province', '0002_city_slug_province_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
    ]