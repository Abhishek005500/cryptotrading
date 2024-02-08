# Generated by Django 4.2.9 on 2024-01-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0013_cryptocurrency_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='buy_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
            preserve_default=False,
        ),
    ]
