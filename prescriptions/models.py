from django.db import models
from users.models import PatientProfile, DoctorProfile
from patient_records.models import MedicalRecord

class Prescription(models.Model):
    """
    Model representing a prescription for a patient.
    """
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Dispensed", "Dispensed"),
        ("Cancelled", "Cancelled"),
    ]
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="prescriptions")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="patient_prescriptions")  
    frequency = models.CharField(max_length=100, help_text="E.g., Twice a day, Every 6 hours")
    quantity = models.PositiveIntegerField(help_text="Total quantity prescribed")
    duration = models.PositiveIntegerField(help_text="Duration in days")
    instructions = models.TextField(blank=True, null=True, help_text="Additional instructions for the patient")
    prescribed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES, 
        default="pending",
        help_text="Current status of the prescription"
    )

    def __str__(self):
        return f"Prescription for {self.patient} by {self.doctor}"