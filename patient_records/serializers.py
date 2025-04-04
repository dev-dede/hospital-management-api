from rest_framework import serializers
from .models import (
    MedicalRecord,
    Diagnosis,
)

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

    def validate(self, data):
        # Check if the diagnosis patient matches the patient in the medical record
        medical_record = data.get('medical_record')
        patient = data.get('patient')

        # Ensure that the patient in the diagnosis matches the patient in the medical record
        if medical_record.patient != patient:
            raise serializers.ValidationError("The patient in the diagnosis must match the patient in the medical record.")

        return data