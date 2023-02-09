# Generated by Django 4.1 on 2023-01-23 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0016_menuitem_calorie"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("title", models.CharField(max_length=125)),
                ("content", models.CharField(max_length=500)),
                ("status", models.BooleanField()),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="cafe.cafe",
                    ),
                ),
            ],
        ),
    ]
