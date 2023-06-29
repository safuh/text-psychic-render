from django.contrib import admin

# Register your models here.
from .models import Ledger as Transactions

admin.site.register(Transactions)