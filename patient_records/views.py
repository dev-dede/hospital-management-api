from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
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

# Only doctors can create medical records
class MedicalRecordListView(ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, (IsDoctor | IsPatient)]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Doctor":
            return MedicalRecord.objects.all()
        if user.role == "Patient":
            return MedicalRecord.objects.filter(patient=user.patientprofile)
        
class MedicalRecordDetailView(RetrieveAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    # Patient get only their medical record with list hence no need for detailview for patients
    permission_classes = [IsAuthenticated, IsDoctor]