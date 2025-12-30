from django.contrib import admin
from .models import UserOrder


@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'vendor_name', 'status', 'total', 'created_at']
    list_filter = ['status', 'delivery_type', 'prescription_required', 'created_at']
    search_fields = ['order_id', 'customer_name', 'customer_phone', 'vendor_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'user', 'vendor', 'status', 'delivery_type')
        }),
        ('Items & Pricing', {
            'fields': ('items', 'subtotal', 'tip', 'total', 'prescription_required')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'address')
        }),
        ('Vendor Information', {
            'fields': ('vendor_name', 'vendor_phone')
        }),
        ('Payment Information', {
            'fields': ('payment_id', 'razorpay_order_id', 'razorpay_signature', 'payment_status')
        }),
        ('Additional Information', {
            'fields': ('notes', 'rating', 'review', 'created_at', 'updated_at')
        }),
    )

