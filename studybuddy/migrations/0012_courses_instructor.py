# Generated by Django 4.0.3 on 2022-05-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0011_remove_courses_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='instructor',
            field=models.CharField(default='temp', max_length=255, verbose_name='Instructor'),
            preserve_default=False,
        ),
    ]
