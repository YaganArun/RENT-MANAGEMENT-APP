# Generated by Django 3.0.5 on 2020-05-10 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0004_auto_20200509_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='dueAmnt',
        ),
    ]
