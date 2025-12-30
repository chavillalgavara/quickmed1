from django.db import models
from accounts.models import UserProfile


class UserOrder(models.Model):
    """
    User Order Model - Stores orders from user's perspective
    This is separate from venderdashboard.Order which is vendor-focused
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ready', 'Ready'),
        ('picked', 'Picked'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    DELIVERY_TYPE_CHOICES = [
        ('home', 'Home Delivery'),
        ('pickup', 'Store Pickup'),
    ]
    
    # Order identification
    order_id = models.CharField(max_length=100, unique=True, db_index=True)
    
    # User (customer) who placed the order
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="user_orders"
    )
    
    # Vendor (pharmacy/vendor fulfilling this order)
    vendor = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        related_name="user_orders_vendor",
        null=True,
        blank=True
    )
    
    # Order items (stored as JSON)
    items = models.JSONField(default=list)  # List of items with name, quantity, price, medicine_id
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order status (from user's perspective)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Delivery information
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='home')
    address = models.JSONField(default=dict, null=True, blank=True)  # Store address as JSON
    
    # Payment information
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='completed')
    
    # Customer information (stored for reference)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Vendor information (stored for user reference)
    vendor_name = models.CharField(max_length=200, null=True, blank=True)
    vendor_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Prescription requirement
    prescription_required = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional metadata
    notes = models.TextField(blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)  # User's rating for the order
    review = models.TextField(blank=True, null=True)  # User's review
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['vendor', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.order_id} - {self.customer_name} - {self.status}"
