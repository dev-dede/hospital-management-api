from django.db import models
from users.models import (
    PatientProfile,
    DoctorProfile
)

class MedicalRecord(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name="medicalrecord")
    surgeries = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.patient.user.get_full_name()}"

class Diagnosis(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="patientdiagnosis")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctordiagnosis")
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    added_notes = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis for {self.patient.user.get_full_name()} by Dr. {self.doctor.user.get_full_name()}"

