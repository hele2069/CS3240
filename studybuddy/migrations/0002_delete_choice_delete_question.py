# Generated by Django 4.0.2 on 2022-03-27 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
