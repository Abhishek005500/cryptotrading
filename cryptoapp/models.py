from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    walletuser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.walletuser}"


class CryptoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobilenumber = models.IntegerField(blank=True, null=True)
    is_kyc_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class Kyc(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    documenttype = models.CharField(max_length=100)
    documentnumber = models.IntegerField(blank=True)
    dateofbirth = models.DateTimeField()
    address = models.CharField(max_length=100, blank=True)
    documentimage = models.ImageField()
    verified_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(decimal_places=2, max_digits=20)
    percent_change_24h = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    buy_price = models.DecimalField(decimal_places=2, max_digits=20)
    coin = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    total_cost = models.DecimalField(decimal_places=2, max_digits=20)  # Add this field

    timestamp = models.DateTimeField(auto_now_add=True)
