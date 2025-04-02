from rest_framework import serializers
from .models import (
    CustomUser,
    PatientProfile,
    DoctorProfile,
    PharmacistProfile,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class PatientProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField
    full_name = serializers.SerializerMethodField

    class Meta:
        model = PatientProfile
        fields = ['user', 'date_of_birth', 'sex', 'address', 'phone_number', 'full_name', 'age']

    def get_full_name(self, obj): 
        # Return full name of user associated with the current patient profile
        return obj.user.get_full_name()
    
    def get_age(self, obj):
        # Calculates age of user based on user date of birth using function in patient profile model
        return obj.user.calculate_age()

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'

class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = '__all__'