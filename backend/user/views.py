from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import time
from .models import UserOrder
from .serializers import UserOrderSerializer
from accounts.models import UserProfile


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_orders_list(request):
    """
    Get all orders for logged-in user
    """
    try:
        # Get logged-in user
        user = request.user
        
        # Fetch all orders for this user
        orders = UserOrder.objects.filter(user=user).order_by('-created_at')
        
        # Serialize and return
        serializer = UserOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_order_detail(request, order_id):
    """
    Get specific order details for logged-in user
    """
    try:
        # Get logged-in user
        user = request.user
        
        # Fetch order for this user
        try:
            order = UserOrder.objects.get(order_id=order_id, user=user)
        except UserOrder.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serialize and return
        serializer = UserOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user_order(request):
    """
    Create a new user order (called when user places order)
    This can be called from the frontend or synced from venderdashboard.Order
    """
    try:
        # Get logged-in user
        user = request.user
        
        # Get vendor if provided
        vendor = None
        vendor_id = request.data.get('vendorId') or request.data.get('vendor_id')
        if vendor_id:
            try:
                vendor = UserProfile.objects.get(id=vendor_id, user_type='vendor')
            except UserProfile.DoesNotExist:
                pass
        
        # Create order data
        order_data = {
            'order_id': request.data.get('orderId') or request.data.get('order_id') or f"ORD{int(time.time() * 1000)}",
            'user': user.id,
            'vendor': vendor.id if vendor else None,
            'items': request.data.get('items', []),
            'subtotal': request.data.get('subtotal', 0),
            'tip': request.data.get('tip', 0),
            'total': request.data.get('total', 0),
            'status': request.data.get('status', 'pending'),
            'delivery_type': request.data.get('deliveryType', 'home'),
            'address': request.data.get('address'),
            'payment_id': request.data.get('paymentId'),
            'razorpay_order_id': request.data.get('razorpayOrderId'),
            'razorpay_signature': request.data.get('razorpaySignature'),
            'payment_status': request.data.get('paymentStatus', 'completed'),
            'customer_name': request.data.get('customerName') or (user.full_name if hasattr(user, 'full_name') else None) or user.email,
            'customer_phone': request.data.get('customerPhone') or (user.phone if hasattr(user, 'phone') else None),
            'vendor_name': request.data.get('vendorName'),
            'prescription_required': request.data.get('prescriptionRequired', False),
        }
        
        serializer = UserOrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
