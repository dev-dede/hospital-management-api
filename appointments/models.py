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

    def __str__(self):
        return f"Appointment({self.patient.user.get_full_name()} with Dr. {self.doctor.user.get_full_name()} on {self.date_time.strftime('%Y-%m-%d %H:%M')} - {self.status})"