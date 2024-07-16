# Generated by Django 5.0.6 on 2024-07-16 17:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_app', '0002_specialday_alter_timemodel_time_end_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SpecialDay',
        ),
        migrations.RemoveField(
            model_name='timemodel',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='timemodel',
            name='time_start',
        ),
        migrations.AddField(
            model_name='timemodel',
            name='custom_time_end',
            field=models.TimeField(blank=True, default=datetime.time(19, 0), verbose_name='Измененное время окончания работы'),
        ),
        migrations.AddField(
            model_name='timemodel',
            name='custom_time_start',
            field=models.TimeField(blank=True, default=datetime.time(9, 0), verbose_name='Измененное время начала работы'),
        ),
        migrations.AddField(
            model_name='timemodel',
            name='is_holiday',
            field=models.BooleanField(default=False, verbose_name='Выходной'),
        ),
    ]
