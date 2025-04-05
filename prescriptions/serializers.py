from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"
        read_only_fields = ["patient", "prescribed_at"]  # Patients and timestamp should be immutable

    def update(self, instance, validated_data):
        user = self.context["request"].user

        # Doctors cannot update status
        if user.role == "doctor" and "status" in validated_data:
            raise serializers.ValidationError({"status": "Doctors cannot change the status."})

        # Pharmacists can only update the status field
        if user.role == "pharmacist" and set(validated_data.keys()) - {"status"}:
            raise serializers.ValidationError("Pharmacists can only update the status field.")

        return super().update(instance, validated_data)
