# Generated by Django 4.1 on 2023-11-11 15:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0029_cafe_is_notify_expired_from_back_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="sort_index",
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
