# Generated by Django 2.2.6 on 2020-05-02 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fornow', '0016_auto_20200502_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourdetails',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_detail', to='fornow.Tour', verbose_name='Tour'),
        ),
    ]
