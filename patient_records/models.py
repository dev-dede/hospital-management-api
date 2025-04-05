from django.db import models
from users.models import (
    PatientProfile,
    DoctorProfile
)

class MedicalRecord(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name="medical_record")
    surgeries = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.patient.user.get_full_name()}"

class Diagnosis(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="patient_diagnosis")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor_diagnosis")
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='diagnoses')
    added_notes = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis for {self.patient.user.get_full_name()} by Dr. {self.doctor.user.get_full_name()}"
    
class LabResult(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='patient_lab_results')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_results')
    xray = models.FileField(upload_to='xrays/', blank=True, null=True) 
    vitalsigns = models.JSONField(blank=True, null=True) 
    blood_test_results = models.JSONField(blank=True, null=True)  # Store results as JSON "hemoglobin": "13.5 g/dL", "wbc_count": "5,000 cells/mcL"}
    urinalysis_results = models.JSONField(blank=True, null=True) 
    date_created = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Lab Results for {self.patient.user.get_full_name()} on {self.date_created}"

