# Generated by Django 4.0.4 on 2022-05-02 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0008_remove_profile_enrollment_profile_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='toggled_courses',
            field=models.ManyToManyField(related_name='toggled_courses', to='studybuddy.courses'),
        ),
    ]
