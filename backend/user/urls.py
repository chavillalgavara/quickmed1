from django.urls import path
from .views import (
    user_orders_list,
    user_order_detail,
    create_user_order,
)

urlpatterns = [
    path("orders/", user_orders_list),  # GET - User fetches their orders
    path("orders/<str:order_id>/", user_order_detail),  # GET - User fetches specific order
    path("orders/create/", create_user_order),  # POST - Create user order
]

