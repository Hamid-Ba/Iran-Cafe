# Generated by Django 4.1 on 2022-09-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='short_desc',
        ),
        migrations.AlterField(
            model_name='cafe',
            name='desc',
            field=models.TextField(),
        ),
    ]
