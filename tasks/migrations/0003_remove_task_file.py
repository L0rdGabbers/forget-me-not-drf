# Generated by Django 3.2.23 on 2023-12-07 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20231202_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='file',
        ),
    ]