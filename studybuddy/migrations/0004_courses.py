# Generated by Django 4.0.3 on 2022-03-29 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Subject')),
                ('number', models.CharField(max_length=4, verbose_name='Number')),
                ('instructor', models.CharField(max_length=255, verbose_name='Instructor')),
            ],
        ),
    ]
