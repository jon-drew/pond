# Generated by Django 2.0.7 on 2018-10-25 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20181017_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
