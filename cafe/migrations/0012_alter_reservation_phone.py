# Generated by Django 4.1 on 2022-10-21 15:22

import cafe.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0011_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="phone",
            field=models.CharField(
                max_length=11, validators=[cafe.validators.PhoneValidator]
            ),
        ),
    ]
