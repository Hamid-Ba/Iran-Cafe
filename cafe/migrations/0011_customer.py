# Generated by Django 4.1 on 2022-10-12 12:27

import cafe.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cafe", "0010_bartender_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=11, validators=[cafe.validators.PhoneValidator]
                    ),
                ),
                ("firstName", models.CharField(max_length=65)),
                ("lastName", models.CharField(max_length=85)),
                ("birthdate", models.DateField()),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customers",
                        to="cafe.cafe",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
