from rest_framework import serializers
from .models import Prescription
from medications.models import Medication
from medications.serializers import MedicationSerializer
from users.models import PatientProfile

class PrescriptionSerializer(serializers.ModelSerializer):
    # Details of medications added by id is displayed
    medications = MedicationSerializer(many=True, read_only=True) 

    #Pharmacist can add medications by their ids
    medication_ids = serializers.PrimaryKeyRelatedField(
        queryset = Medication.objects.all(),
        many = True,
        write_only = True,
    ) 
    class Meta:
        model = Prescription
        fields = [
                'id', 'doctor', 'medical_record', 'patient', 
                'frequency','quantity', 'duration', 'instructions', 
                'prescribed_at','status', 'medications', 'medication_ids'
            ]
        read_only_fields = ["patient", "prescribed_at"]

    def validate_medications_id(self, value):
        if not value:
            raise serializers.ValidationError("At least one medication is required.")
        return value
    
    def validate(self, data):
        medical_record = data.get('medical_record')
        patient = data.get('patient')

        if medical_record is None:
            return data

        # Ensure that the patient in the prescripnioj matches the patient in the medical record
        if medical_record.patient != patient:
            raise serializers.ValidationError("The patient in the prescription must match the patient in the medical record.")
        return data

    
    def create(self, validated_data):
        medication_ids = validated_data.pop('medication_ids', [])
        
        request = self.context.get("request")
        patient_id = request.data.get("patient")
        patient = PatientProfile.objects.get(id=patient_id)  # Convert patient_id to Patientprofile instance

        # Now add patient to validated_data
        validated_data["patient"] = patient

        prescription = Prescription.objects.create(**validated_data)

        for med in medication_ids:
            med.prescription = prescription
            med.save()
        return prescription


    def update(self, instance, validated_data):
        user = self.context["request"].user

        # Doctors cannot update status
        if user.role == "doctor" and "status" in validated_data:
            raise serializers.ValidationError({"status": "Doctors cannot change the status."})

        # Pharmacists can only update the status field
        if user.role == "pharmacist" and set(validated_data.keys()) - {"status"}:
            raise serializers.ValidationError("Pharmacists can only update the status field.")

        return super().update(instance, validated_data)
