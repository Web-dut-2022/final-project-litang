# Generated by Django 4.0.3 on 2022-04-25 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_list_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='user',
            new_name='imguser',
        ),
    ]
