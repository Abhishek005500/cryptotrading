# Generated by Django 4.2.9 on 2024-01-18 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0007_remove_cryptouser_email_remove_cryptouser_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptouser',
            name='mobilenumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]