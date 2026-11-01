from django.contrib import admin
from .models import Product, Review, Order, StoreSettings

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'status', 'created_at')
    list_filter = ('category', 'status')
    search_fields = ('name', 'desc')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('name', 'text')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'phone', 'total', 'channel', 'date')
    list_filter = ('channel', 'date')
    search_fields = ('customer', 'phone', 'product_summary')

@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email_config_owner_email')
