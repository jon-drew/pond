# Generated by Django 2.0.7 on 2018-10-11 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_invitees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='invitees',
            field=models.ManyToManyField(related_name='invited', through='ribbits.Ribbit', to='hoppers.Hopper'),
        ),
    ]
