from .serializers import AppointmentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient, IsDoctor
from .models import Appointment

class AppointmentCreateView(generics.CreateAPIView):
    """
    Allows only patients to create appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        # Assigns the logged-in patient to the appointment
        return serializer.save(patient=self.request.user.patientprofile)

class AppointmentUpdateView(generics.UpdateAPIView):
     """
    Allows only doctors to update appointment status.
    """
     serializer_class = AppointmentSerializer
     permission_classes = [IsAuthenticated, IsDoctor]

     def get_queryset(self):
         # Doctors can update their own appointments
        return Appointment.objects.filter(doctor=self.request.user.doctorprofile)
     
     def perform_update(self, serializer):
         # Allow only the status field to be updated by doctors
         status = serializer.validated_data.get("status", None)
         if status:
             serializer.instance.status = status
             serializer.instance.save()

class AppointmentListView(generics.ListAPIView):
    """
    Returns appointments based on user role.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, (IsDoctor | IsPatient)]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Patient":
            return Appointment.objects.filter(patient=user.patientprofile)
        if user.role == "Doctor":
            return Appointment.objects.filter(doctor=user.doctorprofile)
        return Appointment.objects.none() # Return none if neither doctor or patient
    
class AppointmentDeleteView(generics.DestroyAPIView):
    """
    Allows only patients to delete their appointments.
    """
    serializer_class = AppointmentSerializer 
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
         """Patients can delete only their own appointments"""
         return Appointment.objects.filter(patient=self.request.user.patientprofile)
