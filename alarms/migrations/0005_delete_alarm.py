# Generated by Django 2.2.4 on 2019-08-15 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0004_alarm'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Alarm',
        ),
    ]
