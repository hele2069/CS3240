# Generated by Django 3.2.13 on 2022-05-03 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0010_alter_profile_toggled_courses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_course', models.CharField(max_length=100, verbose_name='Course(s)')),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=5000, verbose_name='Location')),
                ('other_people', models.ManyToManyField(related_name='study_partner', to='studybuddy.Profile')),
                ('user_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='studybuddy.profile')),
            ],
        ),
    ]
