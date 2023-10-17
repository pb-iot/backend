# Generated by Django 4.2.6 on 2023-10-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse_management', '0002_greenhouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greenhouse',
            name='crop_type',
            field=models.CharField(choices=[('TT', 'Tomatoes'), ('PT', 'Potatoes')], default='TT', max_length=2),
        ),
    ]
