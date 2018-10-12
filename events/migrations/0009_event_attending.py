# Generated by Django 2.0.7 on 2018-10-11 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0011_auto_20181008_1609'),
        ('ribbits', '0013_auto_20181011_1300'),
        ('events', '0008_remove_event_attending'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attending',
            field=models.ManyToManyField(related_name='attending', through='ribbits.Ribbit', to='hoppers.Hopper'),
        ),
    ]
