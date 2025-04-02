from rest_framework import (
    generics,
    viewsets,
    permissions
)
from .serializers import (
    UserSerializer, 
    PatientProfileSerializer,
    DoctorProfileSerializer,
    PharmacistProfileSerializer,
)
from .models import (
    PatientProfile,
    DoctorProfile,
    PharmacistProfile,
)

class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserUpdateRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class PatientProfileView(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

    def get_queryset(self):
        # Only allow users to get their own profile (Logged in user profile)
        return PatientProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # When a patientprofile is created, link the profile to the current logged-in user
        return serializer.save(user=self.request.user)
    
class DoctorProfileView(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        return DoctorProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class PharmacistProfileView(viewsets.ModelViewSet):
    queryset = PharmacistProfile
    serializer_class = PharmacistProfileSerializer

    def get_queryset(self):
        return PharmacistProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)