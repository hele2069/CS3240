# Generated by Django 3.2.13 on 2022-05-03 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0012_auto_20220503_0129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='other_people',
            new_name='study_buddies',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='user_profile',
        ),
    ]
