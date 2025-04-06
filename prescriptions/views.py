from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Prescription
from .serializers import PrescriptionSerializer
from rest_framework.exceptions import PermissionDenied

class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing prescriptions.
    - Doctors: Can create & update all fields except status.
    - Pharmacists: Can only update the status field.
    - Patients: Can only read prescriptions assigned to them.
    """
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user

        if user.role == "Doctor":
            return Prescription.objects.all()

        if user.role == "Pharmacist":
            return Prescription.objects.all()

        if user.role == "Patient":
            return Prescription.objects.filter(patient=user)

        return Prescription.objects.none()  # No access
