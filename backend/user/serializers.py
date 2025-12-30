from rest_framework import serializers
from .models import UserOrder
from accounts.models import UserProfile


class UserOrderSerializer(serializers.ModelSerializer):
    # Vendor information
    vendor_name = serializers.CharField(source='vendor.pharmacy_name', read_only=True, required=False)
    vendor_email = serializers.CharField(source='vendor.email', read_only=True, required=False)
    vendor_phone = serializers.CharField(source='vendor.phone', read_only=True, required=False)
    vendor_address = serializers.CharField(source='vendor.business_address', read_only=True, required=False)
    vendor_city = serializers.CharField(source='vendor.city', read_only=True, required=False)
    vendor_state = serializers.CharField(source='vendor.state', read_only=True, required=False)
    vendor_pincode = serializers.CharField(source='vendor.pincode', read_only=True, required=False)
    
    # User information
    user_name = serializers.CharField(source='user.full_name', read_only=True, required=False)
    user_email = serializers.CharField(source='user.email', read_only=True, required=False)
    
    class Meta:
        model = UserOrder
        fields = [
            'id',
            'order_id',
            'user',
            'user_name',
            'user_email',
            'vendor',
            'vendor_name',
            'vendor_email',
            'vendor_phone',
            'vendor_address',
            'vendor_city',
            'vendor_state',
            'vendor_pincode',
            'items',
            'subtotal',
            'tip',
            'total',
            'status',
            'delivery_type',
            'address',
            'payment_id',
            'razorpay_order_id',
            'razorpay_signature',
            'payment_status',
            'customer_name',
            'customer_phone',
            'prescription_required',
            'created_at',
            'updated_at',
            'notes',
            'rating',
            'review',
        ]
        read_only_fields = ('created_at', 'updated_at')

