# Generated by Django 2.0.7 on 2018-10-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoppers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hopper',
            name='published_at',
        ),
        migrations.AlterField(
            model_name='hopper',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
    ]
