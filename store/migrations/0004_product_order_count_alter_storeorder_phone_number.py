# Generated by Django 4.1 on 2023-03-18 15:12

import config.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_storeorder_registered_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="order_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="storeorder",
            name="phone_number",
            field=models.CharField(
                max_length=20, validators=[config.validators.PhoneValidator]
            ),
        ),
    ]
