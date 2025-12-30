from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny#this is used for the to send a medicine to the user dashbord 
from rest_framework.response import Response
from rest_framework import status
import time

from .models import VendorMedicine, Order
from .serializers import VendorMedicineSerializer, OrderSerializer
from accounts.models import UserProfile


# ==================================================
# ADD MEDICINE (POST)
# ==================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_vendor_medicine(request):
    """
    Add medicine for logged-in vendor
    """

    try:
        # 1️⃣ Get logged-in vendor using email
        vendor = UserProfile.objects.get(
            email=request.user.email,
            user_type="vendor"
        )

        # 2️⃣ Validate request data
        serializer = VendorMedicineSerializer(
    data=request.data,
    context={"request": request}
)

        if serializer.is_valid():
            # 3️⃣ Save medicine with vendor
            serializer.save(vendor=vendor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("❌ SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except UserProfile.DoesNotExist:
        return Response(
            {"error": "Vendor profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================================================
# LIST MEDICINES (GET)
# ==================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_medicine_list(request):
    """
    Get medicines for logged-in vendor only
    """

    try:
        # 1️⃣ Get logged-in vendor
        vendor = UserProfile.objects.get(
            email=request.user.email,
            user_type="vendor"
        )

        # 2️⃣ Fetch only this vendor medicines
        medicines = VendorMedicine.objects.filter(vendor=vendor)

        # 3️⃣ Serialize and return
        serializer = VendorMedicineSerializer(medicines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response(
            {"error": "Vendor profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )
# ==================================================
# GET / UPDATE / DELETE SINGLE MEDICINE
# ==================================================
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def vendor_medicine_detail(request, pk):
    """
    Get / Update / Delete a single medicine (vendor only)
    """

    try:
        # 1️⃣ Get logged-in vendor
        vendor = UserProfile.objects.get(
            email=request.user.email,
            user_type="vendor"
        )

        # 2️⃣ Get medicine that belongs to this vendor
        medicine = VendorMedicine.objects.get(id=pk, vendor=vendor)

    except UserProfile.DoesNotExist:
        return Response(
            {"error": "Vendor profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except VendorMedicine.DoesNotExist:
        return Response(
            {"error": "Medicine not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 🔹 UPDATE MEDICINE
    if request.method == "PATCH":
        serializer = VendorMedicineSerializer(
            medicine,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 GET SINGLE MEDICINE
    if request.method == "GET":
        serializer = VendorMedicineSerializer(medicine)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 DELETE MEDICINE
    if request.method == "DELETE":
        medicine.delete()
        return Response(
            {"message": "Medicine deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ==================================================
# PUBLIC MEDICINE LIST (USER) to see medicine inth euser side this is needed
# ==================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def public_medicine_list(request):
    """
    User can see all medicines added by vendors
    """
    medicines = VendorMedicine.objects.all()
    serializer = VendorMedicineSerializer(medicines, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ==================================================
# CREATE ORDER (POST) - User places order
# ==================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Create a new order (called by user after payment success)
    """
    try:
        # Get logged-in customer (user)
        customer = request.user
        
        # Determine vendor from order items (medicines)
        # Each medicine should belong to a vendor, so we find the vendor from the medicines
        vendor = None
        vendor_id = request.data.get('vendorId')
        items = request.data.get('items', [])
        
        # First, try to get vendor from vendorId if provided (highest priority)
        if vendor_id:
            try:
                vendor = UserProfile.objects.get(id=vendor_id, user_type='vendor')
            except UserProfile.DoesNotExist:
                vendor = None
        
        # If vendor not found, try to determine from order items
        if not vendor and items:
            # Priority 1: Try to get vendor from vendor_id in items
            for item in items:
                vendor_id_from_item = item.get('vendor_id')
                if vendor_id_from_item:
                    try:
                        vendor = UserProfile.objects.get(id=vendor_id_from_item, user_type='vendor')
                        if vendor:
                            break
                    except UserProfile.DoesNotExist:
                        continue
            
            # Priority 2: Try to find vendor from medicine_id
            if not vendor:
                for item in items:
                    medicine_id = item.get('medicine_id') or item.get('id')
                    if medicine_id:
                        try:
                            medicine = VendorMedicine.objects.filter(id=medicine_id).first()
                            if medicine and medicine.vendor:
                                vendor = medicine.vendor
                                break
                        except (VendorMedicine.DoesNotExist, ValueError):
                            pass
            
            # Priority 3: Try medicine names (less reliable)
            if not vendor:
                medicine_names = [item.get('name') for item in items if item.get('name')]
                if medicine_names:
                    first_medicine_name = medicine_names[0]
                    try:
                        medicine = VendorMedicine.objects.filter(medicine_name=first_medicine_name).first()
                        if medicine and medicine.vendor:
                            vendor = medicine.vendor
                    except VendorMedicine.DoesNotExist:
                        pass
        
        # Final fallback: Only use first vendor if we absolutely cannot determine vendor
        # This should rarely happen if items have proper vendor_id or medicine_id
        if not vendor:
            vendor = UserProfile.objects.filter(user_type='vendor').first()
            if vendor:
                print(f"Warning: Could not determine vendor from order items, using fallback vendor: {vendor.id}")
        
        if not vendor:
            return Response(
                {"error": "No vendor available. Could not determine vendor from order items."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate order_id if not provided
        order_id_input = request.data.get('orderId') or request.data.get('id')
        if not order_id_input:
            order_id_input = f"ORD{int(time.time() * 1000)}"
        elif not order_id_input.startswith('ORD'):
            order_id_input = f"ORD{order_id_input}"
        
        # Create order data
        order_data = {
            'order_id': order_id_input,
            'customer': customer.id,
            'vendor': vendor.id,
            'items': request.data.get('items', []),
            'subtotal': request.data.get('subtotal', 0),
            'tip': request.data.get('tip', 0),
            'total': request.data.get('total', 0),
            'status': 'pending',  # Orders start as pending for vendor
            'delivery_type': request.data.get('deliveryType', 'home'),
            'address': request.data.get('address'),
            'payment_id': request.data.get('paymentId'),
            'razorpay_order_id': request.data.get('razorpayOrderId'),
            'razorpay_signature': request.data.get('razorpaySignature'),
            'customer_name': request.data.get('customerName') or (customer.full_name if hasattr(customer, 'full_name') else None) or customer.email,
            'customer_phone': request.data.get('customerPhone') or (customer.phone if hasattr(customer, 'phone') else None),
            'prescription_required': request.data.get('prescriptionRequired', False),
        }
        
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Sync order to UserOrder model (user app) for user's order history
            try:
                from user.models import UserOrder
                from user.serializers import UserOrderSerializer
                
                user_order_data = {
                    'order_id': order.order_id,
                    'user': customer.id,
                    'vendor': vendor.id if vendor else None,
                    'items': order.items,
                    'subtotal': float(order.subtotal),
                    'tip': float(order.tip),
                    'total': float(order.total),
                    'status': order.status,
                    'delivery_type': order.delivery_type,
                    'address': order.address,
                    'payment_id': order.payment_id,
                    'razorpay_order_id': order.razorpay_order_id,
                    'razorpay_signature': order.razorpay_signature,
                    'payment_status': 'completed',
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'vendor_name': vendor.pharmacy_name if vendor and hasattr(vendor, 'pharmacy_name') else None,
                    'prescription_required': order.prescription_required,
                }
                
                user_order_serializer = UserOrderSerializer(data=user_order_data)
                if user_order_serializer.is_valid():
                    user_order_serializer.save()
                else:
                    # Log error but don't fail the main order creation
                    print(f"Warning: Failed to sync order to UserOrder: {user_order_serializer.errors}")
            except Exception as e:
                # Log error but don't fail the main order creation
                print(f"Warning: Failed to sync order to UserOrder: {str(e)}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================================================
# GET VENDOR ORDERS (GET) - Vendor fetches their orders
# ==================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_orders_list(request):
    """
    Get all orders for logged-in vendor, grouped by status
    """
    try:
        # Get logged-in vendor
        vendor = UserProfile.objects.get(
            email=request.user.email,
            user_type="vendor"
        )
        
        # Fetch all orders for this vendor
        orders = Order.objects.filter(vendor=vendor).order_by('-order_time')
        
        # Group orders by status
        orders_by_status = {
            'pending': [],
            'ready': [],
            'picked': [],
            'cancelled': [],
            'confirmed': [],
            'delivered': []
        }
        
        serializer = OrderSerializer(orders, many=True)
        
        for order_data in serializer.data:
            order_status = order_data.get('status', 'pending')
            if order_status in orders_by_status:
                # Format order data for frontend
                formatted_order = {
                    'id': order_data['order_id'],
                    'customerName': order_data.get('customer_name', ''),
                    'customerPhone': order_data.get('customer_phone', ''),
                    'items': order_data.get('items', []),
                    'total': float(order_data.get('total', 0)),
                    'orderTime': order_data.get('order_time', ''),
                    'deliveryType': order_data.get('delivery_type', 'home'),
                    'address': order_data.get('address'),
                    'prescriptionRequired': order_data.get('prescription_required', False),
                }
                orders_by_status[order_status].append(formatted_order)
        
        return Response(orders_by_status, status=status.HTTP_200_OK)
        
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "Vendor profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================================================
# UPDATE ORDER STATUS (PATCH) - Vendor updates order status
# ==================================================
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """
    Update order status (e.g., pending -> ready -> picked)
    """
    try:
        vendor = UserProfile.objects.get(
            email=request.user.email,
            user_type="vendor"
        )
        
        order = Order.objects.get(order_id=order_id, vendor=vendor)
        
        new_status = request.data.get('status')
        if new_status:
            order.status = new_status
            order.save()
            
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "Status is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "Vendor profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )