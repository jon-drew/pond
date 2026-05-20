from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ribbits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ribbit',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
