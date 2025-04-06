from rest_framework import serializers
from .models import (
    MedicalRecord,
    Diagnosis,
    LabResult,
)
from prescriptions.serializers import PrescriptionSerializer

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'
        # Once a diagnosis is made for a certain patient, the doctor nor patient can't be changed
        # For prove of diagnosis in case of doctor errors
        read_only_fields = ['doctor', 'patient']

    def validate(self, data):
        # Check if the diagnosis patient matches the patient in the medical record
        medical_record = data.get('medical_record')
        patient = data.get('patient')

        # For patch requests where medical_record would not be passed
        # Creation already validated patient matching
        if medical_record is None:
            return data

        # Ensure that the patient in the diagnosis matches the patient in the medical record
        if medical_record.patient != patient:
            raise serializers.ValidationError("The patient in the diagnosis must match the patient in the medical record.")
        return data

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'
        read_only_fields = ['patient']

    def validate(self, data):
        medical_record = data.get('medical_record')
        patient = data.get('patient')

        if medical_record is None:
            return data

        # Ensure that the patient in the diagnosis matches the patient in the medical record
        if medical_record.patient != patient:
            raise serializers.ValidationError("The patient in the labresults must match the patient in the medical record.")
        return data

class MedicalRecordSerializer(serializers.ModelSerializer):
    diagnoses = DiagnosisSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'surgeries', 'allergies', 'family_history', 'social_history', 
            'diagnoses', 'lab_results', 'prescriptions',
            'date_created', 'last_updated',
            ]

