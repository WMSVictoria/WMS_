# Generated by Django 4.2.11 on 2024-08-16 18:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
