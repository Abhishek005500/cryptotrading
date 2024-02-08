from django.contrib import admin
from .models import Wallet, CryptoUser, Kyc, CryptoCurrency, Transaction

# Register your models here.

admin.site.register(Wallet)
admin.site.register(CryptoUser)
admin.site.register(Kyc)
admin.site.register(CryptoCurrency)
admin.site.register(Transaction)
