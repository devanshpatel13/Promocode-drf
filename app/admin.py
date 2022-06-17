from django.contrib import admin
from .models import *


# Register your models here.

# @admin.register(Creation)
# class CreationAdmin(admin.ModelAdmin):
#     list_display = ['gender', 'birthdate','username','email']


@admin.register(User)
class CreationAdmin(admin.ModelAdmin):
    list_display = ['gender', 'birthdate','username','email']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','coupon','user','total']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id','coupon','create_date','expiry_date','user','gender','discount','discount_type','is_active']

