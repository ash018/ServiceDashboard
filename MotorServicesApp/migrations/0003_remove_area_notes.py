# Generated by Django 2.1.8 on 2019-09-18 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MotorServicesApp', '0002_area_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='Notes',
        ),
    ]
