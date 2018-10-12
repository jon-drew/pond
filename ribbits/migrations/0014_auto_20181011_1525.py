# Generated by Django 2.0.7 on 2018-10-11 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0011_auto_20181008_1609'),
        ('events', '0009_event_attending'),
        ('ribbits', '0013_auto_20181011_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ribbit',
            name='sent_to',
        ),
        migrations.AlterUniqueTogether(
            name='ribbit',
            unique_together={('sent_by', 'event')},
        ),
    ]
