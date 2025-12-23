

from rest_framework import serializers
from .models import DeliveryPartner
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class DeliveryPartnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = DeliveryPartner
        fields = [
            "id",
            "full_name",
            "email",                 # ✅ REQUIRED
            "phone",
            "password",              # ✅ ADDED for UserProfile creation
            "aadhar_number",
            "pan_number",
            "driving_license_number",
            "vehicle_number",
            "aadhar_front",
            "aadhar_back",
            "pan_card",
            "license_front",
            "license_back",
            "vehicle_rc",
            "live_photo",
            "status",
            "created_at",
        ]

class DeliveryPartnerProfileSerializer(serializers.ModelSerializer):
    """Serializer for delivery partner profile (read/update, no password)"""
    email = serializers.EmailField(read_only=True)  # Email cannot be changed
    current_location = serializers.SerializerMethodField()
    vehicle_type = serializers.SerializerMethodField()
    emergency_contact1_name = serializers.SerializerMethodField()
    emergency_contact1_phone = serializers.SerializerMethodField()
    emergency_contact1_relation = serializers.SerializerMethodField()
    emergency_contact2_name = serializers.SerializerMethodField()
    emergency_contact2_phone = serializers.SerializerMethodField()
    emergency_contact2_relation = serializers.SerializerMethodField()
    bank_account_number = serializers.SerializerMethodField()
    bank_account_holder = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()
    ifsc_code = serializers.SerializerMethodField()
    upi_id = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryPartner
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "vehicle_number",
            "vehicle_type",  # ✅ From UserProfile
            "current_location",  # ✅ From UserProfile.address
            "aadhar_number",
            "pan_number",
            "driving_license_number",
            "status",
            "created_at",
            # Emergency Contacts (stored in UserProfile fields)
            "emergency_contact1_name",
            "emergency_contact1_phone",
            "emergency_contact1_relation",
            "emergency_contact2_name",
            "emergency_contact2_phone",
            "emergency_contact2_relation",
            # Bank Details (stored in UserProfile fields)
            "bank_account_number",
            "bank_account_holder",
            "bank_name",
            "ifsc_code",
            "upi_id",
        ]
        read_only_fields = ["aadhar_number", "pan_number", "driving_license_number", "status", "created_at"]
    
    def get_current_location(self, obj):
        """Get current location from UserProfile.address"""
        if obj.user and obj.user.address:
            return obj.user.address
        return ''
    
    def get_vehicle_type(self, obj):
        """Get vehicle type from UserProfile"""
        if obj.user and obj.user.vehicle_type:
            return obj.user.vehicle_type
        return ''
    
    def get_emergency_contact1_name(self, obj):
        """Get emergency contact 1 name from UserProfile.apartment (stored as JSON)"""
        if obj.user and obj.user.apartment:
            try:
                import json
                data = json.loads(obj.user.apartment)
                return data.get('emergency_contact1_name', '')
            except:
                pass
        return ''
    
    def get_emergency_contact1_phone(self, obj):
        """Get emergency contact 1 phone"""
        if obj.user and obj.user.emergency_contact:
            return obj.user.emergency_contact
        if obj.user and obj.user.apartment:
            try:
                import json
                data = json.loads(obj.user.apartment)
                return data.get('emergency_contact1_phone', '')
            except:
                pass
        return ''
    
    def get_emergency_contact1_relation(self, obj):
        """Get emergency contact 1 relation"""
        if obj.user and obj.user.apartment:
            try:
                import json
                data = json.loads(obj.user.apartment)
                return data.get('emergency_contact1_relation', '')
            except:
                pass
        return ''
    
    def get_emergency_contact2_name(self, obj):
        """Get emergency contact 2 name"""
        if obj.user and obj.user.apartment:
            try:
                import json
                data = json.loads(obj.user.apartment)
                return data.get('emergency_contact2_name', '')
            except:
                pass
        return ''
    
    def get_emergency_contact2_phone(self, obj):
        """Get emergency contact 2 phone"""
        if obj.user and obj.user.apartment:
            try:
                import json
                data = json.loads(obj.user.apartment)
                return data.get('emergency_contact2_phone', '')
            except:
                pass
        return ''
    
    def get_emergency_contact2_relation(self, obj):
        """Get emergency contact 2 relation"""
        if obj.user and obj.user.apartment:
            try:
                import json
                data = json.loads(obj.user.apartment)
                return data.get('emergency_contact2_relation', '')
            except:
                pass
        return ''
    
    def get_bank_account_number(self, obj):
        """Get bank account number"""
        if obj.user and obj.user.delivery_address:
            try:
                import json
                data = json.loads(obj.user.delivery_address)
                return data.get('bank_account_number', '')
            except:
                pass
        return ''
    
    def get_bank_account_holder(self, obj):
        """Get bank account holder"""
        if obj.user and obj.user.delivery_address:
            try:
                import json
                data = json.loads(obj.user.delivery_address)
                return data.get('bank_account_holder', '')
            except:
                pass
        return ''
    
    def get_bank_name(self, obj):
        """Get bank name"""
        if obj.user and obj.user.delivery_address:
            try:
                import json
                data = json.loads(obj.user.delivery_address)
                return data.get('bank_name', '')
            except:
                pass
        return ''
    
    def get_ifsc_code(self, obj):
        """Get IFSC code"""
        if obj.user and obj.user.delivery_address:
            try:
                import json
                data = json.loads(obj.user.delivery_address)
                return data.get('ifsc_code', '')
            except:
                pass
        return ''
    
    def get_upi_id(self, obj):
        """Get UPI ID"""
        if obj.user and obj.user.delivery_address:
            try:
                import json
                data = json.loads(obj.user.delivery_address)
                return data.get('upi_id', '')
            except:
                pass
        return ''
    
    def update(self, instance, validated_data):
        """Update delivery partner and related UserProfile"""
        import json
        
        # Update DeliveryPartner fields
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.vehicle_number = validated_data.get('vehicle_number', instance.vehicle_number)
        instance.save()
        
        # Update UserProfile if linked
        if instance.user:
            # Update basic fields
            if 'phone' in validated_data:
                instance.user.phone = validated_data['phone']
            if 'full_name' in validated_data:
                instance.user.full_name = validated_data['full_name']
            if 'vehicle_number' in validated_data:
                instance.user.vehicle_number = validated_data['vehicle_number']
            
            # Get additional data from context (passed from view)
            request = self.context.get('request')
            if request:
                # Update current_location (stored in address)
                if 'current_location' in request.data:
                    instance.user.address = request.data['current_location']
                
                # Update vehicle_type
                if 'vehicle_type' in request.data:
                    instance.user.vehicle_type = request.data['vehicle_type']
                
                # Update emergency contacts (stored in apartment as JSON)
                emergency_data = {}
                if instance.user.apartment:
                    try:
                        emergency_data = json.loads(instance.user.apartment)
                    except:
                        pass
                
                if 'emergency_contact1_name' in request.data:
                    emergency_data['emergency_contact1_name'] = request.data['emergency_contact1_name']
                if 'emergency_contact1_phone' in request.data:
                    emergency_data['emergency_contact1_phone'] = request.data['emergency_contact1_phone']
                    instance.user.emergency_contact = request.data['emergency_contact1_phone']  # Also store in main field
                if 'emergency_contact1_relation' in request.data:
                    emergency_data['emergency_contact1_relation'] = request.data['emergency_contact1_relation']
                if 'emergency_contact2_name' in request.data:
                    emergency_data['emergency_contact2_name'] = request.data['emergency_contact2_name']
                if 'emergency_contact2_phone' in request.data:
                    emergency_data['emergency_contact2_phone'] = request.data['emergency_contact2_phone']
                if 'emergency_contact2_relation' in request.data:
                    emergency_data['emergency_contact2_relation'] = request.data['emergency_contact2_relation']
                
                if emergency_data:
                    instance.user.apartment = json.dumps(emergency_data)
                
                # Update bank details (stored in delivery_address as JSON)
                bank_data = {}
                if instance.user.delivery_address:
                    try:
                        bank_data = json.loads(instance.user.delivery_address)
                    except:
                        pass
                
                if 'bank_account_number' in request.data:
                    bank_data['bank_account_number'] = request.data['bank_account_number']
                if 'bank_account_holder' in request.data:
                    bank_data['bank_account_holder'] = request.data['bank_account_holder']
                if 'bank_name' in request.data:
                    bank_data['bank_name'] = request.data['bank_name']
                if 'ifsc_code' in request.data:
                    bank_data['ifsc_code'] = request.data['ifsc_code']
                if 'upi_id' in request.data:
                    bank_data['upi_id'] = request.data['upi_id']
                
                if bank_data:
                    instance.user.delivery_address = json.dumps(bank_data)
            
            instance.user.save()
        
        return instance
    
    def create(self, validated_data):
        # Extract password
        password = validated_data.pop('password')
        
        # Get email and other user data
        email = validated_data.get('email')
        full_name = validated_data.get('full_name')
        phone = validated_data.get('phone')
        
        if not email:
            raise serializers.ValidationError({"email": "Email is required."})
        
        # Check if UserProfile already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        # Check if DeliveryPartner with this email already exists (but no UserProfile)
        existing_delivery = DeliveryPartner.objects.filter(email=email).first()
        if existing_delivery:
            # If DeliveryPartner exists but has no UserProfile, create one and link it
            if not existing_delivery.user:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    full_name=full_name or existing_delivery.full_name,
                    phone=phone or existing_delivery.phone,
                    user_type='delivery'
                )
                existing_delivery.user = user
                existing_delivery.save()
                return existing_delivery
            else:
                raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        # Create UserProfile for authentication
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                phone=phone,
                user_type='delivery'
            )
        except Exception as e:
            raise serializers.ValidationError({"error": f"Failed to create user account: {str(e)}"})
        
        # Create DeliveryPartner and link to UserProfile
        try:
            delivery_partner = DeliveryPartner.objects.create(
                user=user,
                **validated_data
            )
        except Exception as e:
            # Rollback: delete the user if DeliveryPartner creation fails
            user.delete()
            raise serializers.ValidationError({"error": f"Failed to create delivery partner: {str(e)}"})
        
        return delivery_partner
