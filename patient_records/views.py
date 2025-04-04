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
    DiagnosisSerializer,
)
from users.permissions import (
    IsDoctor,
    IsPatient,
)
from .models import (
    MedicalRecord,
    Diagnosis,
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

class MedicalRecordUpdateView(UpdateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

# Only doctors can create a diagnosis
class DiagnosisCreateView(CreateAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)

# Patients can only view their own diagnosis, while doctors can view all
class DiagnosisListView(ListAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated, (IsDoctor | IsPatient)]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Doctor":
            return Diagnosis.objects.all()
        if user.role == "Patient":
            return Diagnosis.objects.filter(patient=user.patientprofile)
        
