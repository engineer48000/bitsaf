from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Transactions)

admin.site.register(AdminHistory)
