# Generated by Django 4.1 on 2022-09-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('phones', models.CharField(blank=True, max_length=60, null=True)),
                ('emails', models.CharField(blank=True, max_length=175, null=True)),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
    ]