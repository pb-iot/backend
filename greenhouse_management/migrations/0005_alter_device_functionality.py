# Generated by Django 4.2.6 on 2023-10-18 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse_management', '0004_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='functionality',
            field=models.CharField(choices=[('PA', 'Passive device'), ('AC', 'Active device')], default='AC', max_length=2),
        ),
    ]
