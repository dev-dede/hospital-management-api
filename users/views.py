from rest_framework import (
    generics,
    viewsets,
    permissions,
    views,
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
from rest_framework.response import Response

class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserUpdateRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LogoutAPIView(views.APIView):
    def post(self, request):
        try:
            # Delete the token to log the user out
            request.user.auth_token.delete()
            return Response({"message": "Logged out successfully!"}, status=200)
        except (AttributeError, KeyError):
            return Response({"error": "User not authenticated or token not found."}, status=400)

class PatientProfileView(viewsets.ModelViewSet):
    serializer_class = PatientProfileSerializer

    def get_queryset(self):
        # Only allow users to get their own profile (Logged in user profile)
        return PatientProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # When a patientprofile is created, link the profile to the current logged-in user
        return serializer.save(user=self.request.user)
    
class DoctorProfileView(viewsets.ModelViewSet):
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        return DoctorProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class PharmacistProfileView(viewsets.ModelViewSet):
    serializer_class = PharmacistProfileSerializer

    def get_queryset(self):
        return PharmacistProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)