# Generated by Django 5.0.3 on 2024-06-29 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0008_reservation_is_reserve_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='slot',
            name='start_time',
            field=models.TimeField(),
        ),
    ]