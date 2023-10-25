# Generated by Django 4.2.6 on 2023-10-18 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse_management', '0005_alter_device_functionality'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=6)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=6)),
            ],
        ),
        migrations.AlterField(
            model_name='greenhouse',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhouse_management.location'),
        ),
        migrations.DeleteModel(
            name='Localization',
        ),
    ]
