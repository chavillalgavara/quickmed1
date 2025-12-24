from django.urls import path
from .views import (
    doctor_timeslots,
    toggle_slot_availability,
    delete_slot,
    doctor_list,
)

app_name = "doctor"

urlpatterns = [
    path("timeslots/", doctor_timeslots),  # GET, POST
    path("timeslots/<int:slot_id>/toggle/", toggle_slot_availability),
    path("timeslots/<int:slot_id>/delete/", delete_slot),
    path("list/", doctor_list),  # all doctors
]