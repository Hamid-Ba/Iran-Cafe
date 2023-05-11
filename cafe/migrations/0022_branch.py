# Generated by Django 4.1 on 2023-05-10 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("province", "0001_initial"),
        ("cafe", "0021_event_is_expired"),
    ]

    operations = [
        migrations.CreateModel(
            name="Branch",
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
                ("latitude", models.CharField(blank=True, max_length=125, null=True)),
                ("longitude", models.CharField(blank=True, max_length=125, null=True)),
                ("street", models.CharField(blank=True, max_length=250, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="branches",
                        to="cafe.cafe",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="province.city",
                    ),
                ),
                (
                    "province",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="province.province",
                    ),
                ),
            ],
        ),
    ]
