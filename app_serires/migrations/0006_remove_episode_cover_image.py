# Generated by Django 5.1.2 on 2024-10-22 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_serires', '0005_episode_cover_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='cover_image',
        ),
    ]
