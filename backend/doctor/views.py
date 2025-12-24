from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserProfile
from .models import TimeSlot
from .serializers import TimeSlotSerializer

#doctor time slot
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def doctor_timeslots(request):
    doctor = request.user  # logged-in doctor

    # 🔹 GET: fetch only this doctor's slots
    if request.method == "GET":
        slots = TimeSlot.objects.filter(doctor=doctor).order_by("date", "start_time")
        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)

    # 🔹 POST: create new slot for this doctor
    if request.method == "POST":
        try:
            serializer = TimeSlotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(doctor=doctor)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(f"Error creating timeslot: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {"error": str(e), "detail": "An error occurred while creating the time slot"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#doctor time slot
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_slot_availability(request, slot_id):
    doctor = request.user

    try:
        slot = TimeSlot.objects.get(id=slot_id, doctor=doctor)
    except TimeSlot.DoesNotExist:
        return Response(
            {"message": "Slot not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if slot.is_booked:
        return Response(
            {"message": "Booked slot cannot be modified"},
            status=status.HTTP_400_BAD_REQUEST
        )

    slot.is_available = not slot.is_available
    slot.save()

    serializer = TimeSlotSerializer(slot)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_slot(request, slot_id):
    doctor = request.user

    try:
        slot = TimeSlot.objects.get(id=slot_id, doctor=doctor)
    except TimeSlot.DoesNotExist:
        return Response(
            {"message": "Slot not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if slot.is_booked:
        return Response(
            {"message": "Booked slot cannot be deleted"},
            status=status.HTTP_400_BAD_REQUEST
        )

    slot.delete()
    return Response({"message": "Slot deleted successfully"})


def doctor_list(request):
    doctors = UserProfile.objects.filter(user_type="doctor")

    data = []
    for d in doctors:
        data.append({
            "id": d.id,
            "name": d.full_name,
            "specialty": d.specialization,
            "experience": d.years_of_experience,   # ✅ FIXED
            "hospital": d.clinic_address,          # or hospital name if you add later
            "consultationFee": float(d.consultation_fee) if d.consultation_fee else 0,
        })

    return JsonResponse(data, safe=False)
