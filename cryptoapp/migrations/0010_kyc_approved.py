# Generated by Django 4.2.9 on 2024-01-18 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0009_alter_wallet_balance_kyc'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
