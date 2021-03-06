# Generated by Django 2.2.6 on 2020-03-29 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fornow', '0007_auto_20200329_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Booking user'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='duration',
            field=models.CharField(choices=[('2-3 days', '2-3 hours'), ('5-6 days', '5-6 hours'), ('7-9 days', '7-9 hours'), ('9-12 days', '9-12 hours'), ('12-24 days', '12-24 hours')], max_length=50),
        ),
    ]
