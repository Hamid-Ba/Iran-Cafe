# Generated by Django 4.1 on 2023-01-23 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0017_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
