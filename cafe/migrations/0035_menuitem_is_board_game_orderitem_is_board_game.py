# Generated by Django 4.1 on 2024-04-15 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0034_order_delivered_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="is_board_game",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="is_board_game",
            field=models.BooleanField(default=False),
        ),
    ]
