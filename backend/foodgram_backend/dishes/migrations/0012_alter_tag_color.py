# Generated by Django 3.2.3 on 2024-03-05 16:50

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0011_auto_20240304_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None),
        ),
    ]
