# Generated by Django 4.1 on 2022-09-07 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='view_count',
            field=models.BigIntegerField(default=0),
        ),
    ]