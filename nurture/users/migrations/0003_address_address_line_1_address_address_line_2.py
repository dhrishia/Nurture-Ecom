# Generated by Django 4.1.7 on 2023-04-19 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(blank=True, default=0, max_length=255),
        ),
    ]
