# Generated by Django 4.1 on 2023-05-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_remove_storeorder_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="storeorder",
            name="fullName",
            field=models.CharField(default="Hamid Balalzadeh", max_length=255),
            preserve_default=False,
        ),
    ]
