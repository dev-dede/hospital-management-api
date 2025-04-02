from rest_framework import serializers
from .models import Appointment

class AppointmentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['patient'] # Patient cannot change themselves neither can doctors change this field