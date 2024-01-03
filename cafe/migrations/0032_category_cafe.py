# Generated by Django 4.1 on 2023-12-06 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0031_alter_menuitem_sort_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="cafe",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories",
                to="cafe.cafe",
            ),
        ),
    ]