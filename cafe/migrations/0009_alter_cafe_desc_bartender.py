# Generated by Django 4.1 on 2022-10-03 19:59

import cafe.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cafe", "0008_cafe_is_open"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cafe",
            name="desc",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Bartender",
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
                        max_length=11,
                        unique=True,
                        validators=[cafe.validators.PhoneValidator],
                    ),
                ),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bartender",
                        to="cafe.cafe",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bartender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
