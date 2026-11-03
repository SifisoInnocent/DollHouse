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
    fieldsets = (
        ('Email Configuration', {
            'fields': ('email_config_key', 'email_config_service', 'email_config_template', 'email_config_owner_email')
        }),
        ('Owner Image', {
            'fields': ('owner_photo',)
        }),
        ('Salon Gallery', {
            'fields': ('salon_image_1', 'salon_image_2', 'salon_image_3', 'salon_image_4')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
