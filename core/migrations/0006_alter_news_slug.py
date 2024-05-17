# Generated by Django 5.0.4 on 2024-05-17 09:29

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_news_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
    ]
