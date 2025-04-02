from django.db import models
from users.models import (
    DoctorProfile,
    PatientProfile,
)

class Appointment(models.ModelField):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    doctor = models.ForeignKeyField(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKeyField(PatientProfile, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
