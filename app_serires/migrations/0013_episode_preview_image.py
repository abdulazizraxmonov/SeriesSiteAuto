# Generated by Django 5.1.2 on 2024-10-30 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_serires', '0012_fragment'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='episode_previews/'),
        ),
    ]