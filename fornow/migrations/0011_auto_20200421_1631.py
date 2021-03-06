# Generated by Django 2.2.6 on 2020-04-21 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fornow', '0010_auto_20200402_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='creater',
        ),
        migrations.AddField(
            model_name='tour',
            name='creator',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Tour creator'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tourimage',
            name='file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
