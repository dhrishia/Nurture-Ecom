# Generated by Django 4.1.7 on 2023-04-14 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_price_cartitem_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
