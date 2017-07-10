from django.contrib import admin
from manager.models import user_profile, bank_accounts, transactions


admin.site.register(user_profile)
admin.site.register(bank_accounts)
admin.site.register(transactions)
