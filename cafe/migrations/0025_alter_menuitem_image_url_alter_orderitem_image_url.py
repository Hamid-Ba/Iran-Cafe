# Generated by Django 4.1 on 2023-08-21 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0024_cafe_menu_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="image_url",
            field=models.URLField(
                blank=True,
                error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="image_url",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]