# Generated by Django 2.2.6 on 2020-05-02 10:45

from django.db import migrations, models
import django.db.models.deletion
import fornow.models


class Migration(migrations.Migration):

    dependencies = [
        ('fornow', '0012_auto_20200421_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=150, verbose_name='Hotel to provide for customer')),
                ('hotel_stars', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('hotel_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fornow.City')),
            ],
        ),
        migrations.CreateModel(
            name='TourDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_start_date', models.DateField(auto_now_add=True)),
                ('tour_end_date', models.DateField()),
                ('tour_person_number', models.IntegerField(verbose_name='Number of persons for one Tour')),
                ('cur_person_number', models.IntegerField(verbose_name='Current Number of persons for one Tour')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_id', to='fornow.Tour', verbose_name='Tour')),
                ('tour_end_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_end', to='fornow.City')),
                ('tour_start_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_start', to='fornow.City')),
            ],
        ),
        migrations.CreateModel(
            name='HotelsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=fornow.models.content_image_name)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fornow.Hotels')),
            ],
        ),
        migrations.AddField(
            model_name='tour',
            name='hotel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotel_id', to='fornow.Hotels'),
        ),
    ]