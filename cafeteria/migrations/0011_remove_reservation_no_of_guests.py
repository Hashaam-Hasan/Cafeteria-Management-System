# Generated by Django 5.0.3 on 2024-06-29 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0010_alter_reservation_reservation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='no_of_guests',
        ),
    ]
