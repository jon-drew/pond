# Generated by Django 2.0.7 on 2018-10-06 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0009_auto_20181006_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='hopper',
            name='anonymous',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='hopper',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]