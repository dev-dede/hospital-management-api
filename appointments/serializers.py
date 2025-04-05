from rest_framework import serializers
from .models import Appointment
from users.serializers import (
    PatientProfileSerializer,
    DoctorProfileSerializer,
)

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = ['id', 'date_time', 'status', 'doctor', 'patient']
        read_only_fields = ['patient', 'doctor'] # Patient cannot change themselves neither can doctors change this field

        # This is already handled in the view
        # def update(self, instance, validated_data):
        #     # Allow only the status field to be updated"
        #     if "status" in validated_data:
        #         instance.status = validated_data["status"]
        #     instance.save()
        #     return instance