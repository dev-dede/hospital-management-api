from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['patient'] # Patient cannot change themselves neither can doctors change this field

        # This is already handled in the view
        # def update(self, instance, validated_data):
        #     # Allow only the status field to be updated"
        #     if "status" in validated_data:
        #         instance.status = validated_data["status"]
        #     instance.save()
        #     return instance