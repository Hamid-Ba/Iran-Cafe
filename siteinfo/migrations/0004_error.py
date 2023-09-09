# Generated by Django 4.1 on 2023-09-09 03:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("siteinfo", "0003_alter_robots_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Error",
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
                ("time_raised", models.DateTimeField(auto_now_add=True)),
                ("reference", models.CharField(max_length=20)),
                ("status", models.CharField(blank=True, max_length=3, null=True)),
                ("description", models.TextField()),
            ],
        ),
    ]
