# Generated by Django 5.0.4 on 2024-06-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_alter_news_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Ньюс'),
        ),
    ]
