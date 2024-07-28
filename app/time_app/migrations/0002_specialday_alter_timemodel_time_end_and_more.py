# Generated by Django 5.0.6 on 2024-07-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('is_holiday', models.BooleanField(default=False, verbose_name='Выходной')),
                ('custom_time_start', models.TimeField(blank=True, null=True, verbose_name='Время начала работы')),
                ('custom_time_end', models.TimeField(blank=True, null=True, verbose_name='Время окончания работы')),
            ],
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='time_end',
            field=models.TimeField(blank=True, null=True, verbose_name='Время окончания работы библиотеки'),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='time_start',
            field=models.TimeField(blank=True, null=True, verbose_name='Время начала работы библиотеки'),
        ),
    ]