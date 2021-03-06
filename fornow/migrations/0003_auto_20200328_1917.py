# Generated by Django 2.2.6 on 2020-03-28 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fornow', '0002_auto_20191025_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='age_requirments',
            field=models.CharField(choices=[('12', '12 years and older'), ('16', '16 years and older'), ('18', '18 years and older'), ('21', '21 years and older')], default=18, max_length=50),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ToursTravelAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel_agent_name', models.CharField(max_length=150, verbose_name='Travel agent name')),
                ('travel_agent_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fornow.City', verbose_name='Travel agent location')),
            ],
        ),
    ]
