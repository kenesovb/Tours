# Generated by Django 2.2.6 on 2020-04-21 17:25

from django.db import migrations, models
import fornow.models


class Migration(migrations.Migration):

    dependencies = [
        ('fornow', '0011_auto_20200421_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourimage',
            name='file',
            field=models.ImageField(blank=True, upload_to=fornow.models.content_file_name),
        ),
    ]
