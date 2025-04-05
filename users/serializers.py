from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import (
    CustomUser,
    PatientProfile,
    DoctorProfile,
    PharmacistProfile,
)


class UserSerializer(serializers.ModelSerializer):
    #token = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'role'] #token
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
    
class PatientProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ['user', 'date_of_birth', 'sex', 'address', 'phone_number', 'full_name', 'age']

    def get_full_name(self, obj): 
        # Return full name of user associated with the current patient profile
        return obj.get_full_name()
    
    def get_age(self, obj):
        # Calculates age of user based on user date of birth using function in patient profile model
        return obj.calculate_age()

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = ['user', 'license_number', 'specialization', 'years_of_experience', 'certifications']

class PharmacistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PharmacistProfile
        fields = ['user', 'license_number', 'specialization', 'years_of_experience', 'certifications']