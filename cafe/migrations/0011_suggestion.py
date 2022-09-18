# Generated by Django 4.1 on 2022-09-18 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0010_remove_cafe_slug_alter_cafe_google_map_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=125, null=True)),
                ('message', models.TextField()),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggest', to='cafe.cafe')),
            ],
        ),
    ]