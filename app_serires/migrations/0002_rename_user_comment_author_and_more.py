# Generated by Django 5.1.2 on 2024-10-22 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_serires', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
    ]
