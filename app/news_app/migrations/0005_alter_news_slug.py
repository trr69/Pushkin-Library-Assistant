# Generated by Django 5.0.4 on 2024-05-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_alter_news_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Слаг'),
        ),
    ]