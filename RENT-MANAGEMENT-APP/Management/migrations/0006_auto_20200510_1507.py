# Generated by Django 3.0.5 on 2020-05-10 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0005_remove_rent_dueamnt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='id',
        ),
        migrations.AlterField(
            model_name='record',
            name='actionMonth',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
