# Generated by Django 2.0.7 on 2018-10-16 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0011_auto_20181008_1609'),
        ('ribbits', '0016_auto_20181014_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='ribbit',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='hoppers.Hopper'),
        ),
        migrations.AddField(
            model_name='ribbit',
            name='spots',
            field=models.ManyToManyField(related_name='spots', to='hoppers.Hopper'),
        ),
    ]
