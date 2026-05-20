import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True,
                help_text='Leave blank for free events. Set a price in USD to enable paid ticketing.',
            ),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('pending', 'Pending'), ('paid', 'Paid'), ('refunded', 'Refunded')],
                    default='pending', max_length=20,
                )),
                ('stripe_session_id', models.CharField(blank=True, max_length=255)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.event')),
                ('hopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('event', 'hopper')},
            },
        ),
    ]
