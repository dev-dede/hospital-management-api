from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Medication
from .serializers import MedicationSerializer
from users.permissions import IsPharmacistOrReadOnly

class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing medications.
    - Pharmacists: Can create, update, and delete.
    - Doctors & Patients: Can only view.
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsPharmacistOrReadOnly]
