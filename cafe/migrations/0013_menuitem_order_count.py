# Generated by Django 4.1 on 2022-10-26 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0012_alter_reservation_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='order_count',
            field=models.IntegerField(default=0),
        ),
    ]
