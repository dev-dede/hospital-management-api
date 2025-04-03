from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
from .serializers import (
    MedicalRecordSerializer,
)
from users.permissions import (
    IsDoctor,
    IsPatient,
)
from .models import (
    MedicalRecord,
)

class MedicalRecordCreateView(CreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

