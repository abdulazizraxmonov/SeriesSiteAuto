# Generated by Django 5.1.2 on 2024-10-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_serires', '0004_genre_rename_category_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/'),
        ),
    ]