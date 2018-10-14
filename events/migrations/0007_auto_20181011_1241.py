# Generated by Django 2.0.7 on 2018-10-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0011_auto_20181008_1609'),
        ('ribbits', '0009_auto_20181011_1233'),
        ('events', '0006_auto_20181011_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='invitees',
        ),
        migrations.AddField(
            model_name='event',
            name='attending',
            field=models.ManyToManyField(related_name='attending', through='ribbits.Ribbit', to='hoppers.Hopper'),
        ),
    ]