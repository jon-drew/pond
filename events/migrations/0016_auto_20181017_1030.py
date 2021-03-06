# Generated by Django 2.0.7 on 2018-10-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_remove_event_published_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start']},
        ),
        migrations.AddField(
            model_name='event',
            name='private',
            field=models.BooleanField(default=True),
        ),
    ]
