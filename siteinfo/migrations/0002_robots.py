# Generated by Django 4.1 on 2022-11-06 15:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("siteinfo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Robots",
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
                ("name", models.CharField(max_length=50)),
                ("text", models.TextField()),
            ],
        ),
    ]
