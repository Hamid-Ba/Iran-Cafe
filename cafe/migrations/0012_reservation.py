# Generated by Django 4.1 on 2022-09-18 11:29

import cafe.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cafe', '0011_suggestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=125)),
                ('phone', models.CharField(max_length=11, unique=True, validators=[cafe.validators.PhoneValidator])),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.CharField(blank=True, max_length=500, null=True)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve', to='cafe.cafe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
