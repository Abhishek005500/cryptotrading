# Generated by Django 4.2.9 on 2024-01-18 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptoapp', '0008_cryptouser_mobilenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.CreateModel(
            name='Kyc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documenttype', models.CharField(max_length=100)),
                ('documentnumber', models.IntegerField(blank=True)),
                ('dateofbirth', models.DateTimeField()),
                ('address', models.CharField(blank=True, max_length=100)),
                ('documentimage', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
