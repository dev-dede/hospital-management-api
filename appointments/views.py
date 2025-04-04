from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Project based imports
from .serializers import AppointmentSerializer
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
        return serializer.save(patient=self.request.user.patient_profile)

class AppointmentUpdateView(generics.UpdateAPIView):
     """
    Allows only doctors to update appointment status.
    """
     serializer_class = AppointmentSerializer
     permission_classes = [IsAuthenticated, IsDoctor]

     def get_queryset(self):
         # Doctors can update their own appointments
        return Appointment.objects.filter(doctor=self.request.user.doctor_profile)
     
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
            return Appointment.objects.filter(patient=user.patient_profile)
        if user.role == "Doctor":
            return Appointment.objects.filter(doctor=user.doctor_profile)
        return Appointment.objects.none() # Return none if neither doctor or patient
    
class AppointmentDeleteView(generics.DestroyAPIView):
    """
    Allows only patients to delete their appointments.
    """
    serializer_class = AppointmentSerializer 
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
         """Patients can delete only their own appointments"""
         return Appointment.objects.filter(patient=self.request.user.patient_profile)
    
    # def destroy(self, request, *args, **kwargs):
    #     """Send a success message after deleting an appointment"""
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({"message": "Appointment deleted successfully."}, status=status.HTTP_200_OK)
