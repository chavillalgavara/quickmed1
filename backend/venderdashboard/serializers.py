from rest_framework import serializers
from .models import VendorMedicine, Order
from accounts.models import UserProfile   # ✅ ADD THIS

class VendorMedicineSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.pharmacy_name', read_only=True, required=False)
    vendor_email = serializers.CharField(source='vendor.email', read_only=True, required=False)
    vendor_id = serializers.IntegerField(source='vendor.id', read_only=True, required=False)
    
    class Meta:
        model = VendorMedicine
        fields = [
            "id",
            "medicine_name",
            "category",
            "batch_no",
            "quantity",
            "min_stock",
            "price",
            "expiry_date",
            "supplier",
            "prescription_required",
            "vendor_name",
            "vendor_email",
            "vendor_id",
        ]


class OrderSerializer(serializers.ModelSerializer):
    # Vendor information
    vendor_name = serializers.CharField(source='vendor.pharmacy_name', read_only=True, required=False)
    vendor_email = serializers.CharField(source='vendor.email', read_only=True, required=False)
    vendor_phone = serializers.CharField(source='vendor.phone', read_only=True, required=False)
    vendor_address = serializers.CharField(source='vendor.business_address', read_only=True, required=False)
    vendor_city = serializers.CharField(source='vendor.city', read_only=True, required=False)
    vendor_state = serializers.CharField(source='vendor.state', read_only=True, required=False)
    vendor_pincode = serializers.CharField(source='vendor.pincode', read_only=True, required=False)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_time', 'updated_at')
