# Generated by Django 2.0.7 on 2018-10-14 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20181014_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='attending',
        ),
    ]
