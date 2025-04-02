from .serializers import AppointmentSerilaizer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient, IsDoctor
from .models import Appointment

class AppointmentCreateView(generics.CreateAPIView):
    """
    Allows only patients to create appointments.
    """
    serializer_class = AppointmentSerilaizer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        # Assigns the logged-in patient to the appointment
        return serializer.save(patient=self.request.user.patientprofile)
