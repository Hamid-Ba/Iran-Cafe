# Generated by Django 4.1 on 2023-05-20 13:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_storeorder_fullname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storeorder",
            name="postal_code",
            field=models.CharField(max_length=10),
        ),
    ]
