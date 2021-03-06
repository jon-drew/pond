# Generated by Django 2.0.7 on 2018-10-11 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0011_auto_20181008_1609'),
        ('events', '0007_auto_20181011_1241'),
        ('ribbits', '0009_auto_20181011_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ribbit',
            name='sent_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='hoppers.Hopper'),
        ),
        migrations.AlterUniqueTogether(
            name='ribbit',
            unique_together={('sent_by', 'sent_to', 'event')},
        ),
    ]
