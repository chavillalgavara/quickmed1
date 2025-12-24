from rest_framework import serializers
from .models import VendorMedicine, Order
from accounts.models import UserProfile   # ✅ ADD THIS

class VendorMedicineSerializer(serializers.ModelSerializer):
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
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_time', 'updated_at')
