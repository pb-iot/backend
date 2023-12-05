# Generated by Django 4.2.6 on 2023-10-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse_management', '0004_location_alter_greenhouse_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('functionality', models.CharField(choices=[('PA', 'Passive device'), ('AC', 'Active device')], default='AC', max_length=2)),
            ],
        ),
    ]
