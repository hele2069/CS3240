# Generated by Django 3.2.13 on 2022-05-03 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0011_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='other_people',
            field=models.ManyToManyField(default=None, related_name='study_partner', to='studybuddy.Profile'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user_profile',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='studybuddy.profile'),
        ),
    ]
