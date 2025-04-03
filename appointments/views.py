from .serializers import AppointmentSerialaizer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient, IsDoctor
from .models import Appointment

class AppointmentCreateView(generics.CreateAPIView):
    """
    Allows only patients to create appointments.
    """
    serializer_class = AppointmentSerialaizer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        # Assigns the logged-in patient to the appointment
        return serializer.save(patient=self.request.user.patientprofile)

class AppointmentUpdateView(generics.UpdateAPIView):
     """
    Allows only doctors to update appointment status.
    """
     queryset = Appointment.objects.all()
     serializer_class = AppointmentSerialaizer
     permission_classes = [IsAuthenticated, IsDoctor]

     def get_queryset(self):
         # Doctors can update their own appointments
        queryset = Appointment.objects.filter(doctor=self.request.user.doctorprofile)
        print(f"User: {self.request.user}, Queryset: {queryset}")  # Debugging
        return queryset
     
     def perform_update(self, serializer):
         # Allow only the status field to be updated by doctors
         status = serializer.validated_data.get("status", None)
         if status:
             serializer.instance.status = status
             serializer.instance.save()
