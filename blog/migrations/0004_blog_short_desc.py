# Generated by Django 4.1 on 2022-12-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_alter_blog_desc"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="short_desc",
            field=models.CharField(default="hi", max_length=300),
            preserve_default=False,
        ),
    ]
