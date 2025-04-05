from rest_framework import (
    generics,
    viewsets,
    views,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    CustomUser,
)
from users.permissions import (
    IsAdmin,
)
from rest_framework.response import Response
from django.http import JsonResponse

class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserUpdateRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

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
    permission_classes = []

    def get_queryset(self):
        return PharmacistProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

#Information printed when one goes to the deployed link
def api_root(request):
    data = {
        "message": "Welcome to the Hospital Management System API 👩‍⚕️🏥",
        "status": "running",
        "endpoints": {
            "authentication": {
                "register": "/api/users/register/",
                "login": "/api/users/login/",
                "logout": "/api/users/logout/",
                "profile": "/api/users/profile/"
            },
            "appointments": "/api/appointments/",
            "prescriptions": "/api/prescriptions/",
            "patient_records": "/api/patient-records/",
            "medications": "/api/medications/",
            "api_docs": "/api/docs/"
        },
        "note": "All endpoints are token-authenticated unless stated otherwise."
    }
    return JsonResponse(data, json_dumps_params={'indent': 4})