from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Category,Product

admin.site.register(User, UserAdmin)

admin.site.register(Category)

admin.site.register(Product)