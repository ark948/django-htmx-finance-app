from django.contrib import admin

# Register your models here.

from .models import Transaction, Category, User


admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(User)