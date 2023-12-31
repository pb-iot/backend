# Generated by Django 4.2.6 on 2023-10-14 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('crop_type', models.CharField(max_length=255)),
                ('authorized_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhouse_management.localization')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_greenhouses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
