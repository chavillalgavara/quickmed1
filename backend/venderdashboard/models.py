from django.db import models
from accounts.models import UserProfile
import json

class VendorMedicine(models.Model):

    vendor = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="vendormedicine"
    )

    medicine_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()
    # min_stock = models.PositiveIntegerField()
    min_stock = models.PositiveIntegerField(default=0)
    supplier = models.CharField(max_length=200, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    expiry_date = models.DateField()

    # supplier = models.CharField(max_length=200)
    batch_no = models.CharField(max_length=100)

    prescription_required = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine_name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('picked', 'Picked'),
        ('cancelled', 'Cancelled'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
    ]
    
    DELIVERY_TYPE_CHOICES = [
        ('home', 'Home Delivery'),
        ('pickup', 'Store Pickup'),
    ]
    
    # Order identification
    order_id = models.CharField(max_length=100, unique=True)
    
    # Customer (user who placed the order)
    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="customer_orders"
    )
    
    # Vendor (pharmacy/vendor receiving the order)
    vendor = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="vendor_orders",
        null=True,
        blank=True
    )
    
    # Order items (stored as JSON)
    items = models.JSONField(default=list)  # List of items with name, quantity, price
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Delivery information
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='home')
    address = models.JSONField(default=dict, null=True, blank=True)  # Store address as JSON
    
    # Payment information
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    
    # Customer information (stored for vendor reference)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Timestamps
    order_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Prescription requirement
    prescription_required = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.order_id} - {self.customer_name} - {self.status}"
