from django.urls import path
from .views import (
    add_vendor_medicine, 
    vendor_medicine_list,
    vendor_medicine_detail, 
    public_medicine_list,
    create_order,
    vendor_orders_list,
    update_order_status
) 

urlpatterns = [
    path("medicines/", vendor_medicine_list),
    path("medicines/add/", add_vendor_medicine),
    path("medicines/<int:pk>/", vendor_medicine_detail),
     # user
    path("medicines/public/", public_medicine_list),  # ✅ ADD THIS #vender to user connection
    # Orders
    path("orders/create/", create_order),  # POST - User creates order
    path("orders/", vendor_orders_list),  # GET - Vendor fetches orders
    path("orders/<str:order_id>/status/", update_order_status),  # PATCH - Update order status
]
