# Generated by Django 4.2.9 on 2024-01-23 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0014_transaction_buy_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
            preserve_default=False,
        ),
    ]
