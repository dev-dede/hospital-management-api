from django.db import models
from users.models import (
    DoctorProfile,
    PatientProfile,
)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="doctorappointments")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="patientappointments")
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
