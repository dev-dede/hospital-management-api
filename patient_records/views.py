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
    LabResultsSerializer,
)
from users.permissions import (
    IsDoctor,
    IsPatient,
)
from .models import (
    MedicalRecord,
    Diagnosis,
    LabResults,
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
            return MedicalRecord.objects.filter(patient=user.patient_profile)
        
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
        serializer.save(doctor=self.request.user.doctor_profile)

# Patients can only view their own diagnosis, while doctors can view all
class DiagnosisListView(ListAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated, (IsDoctor | IsPatient)]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Doctor":
            return Diagnosis.objects.all()
        if user.role == "Patient":
            return Diagnosis.objects.filter(patient=user.patient_profile)

# Only doctors can update a diagnosis
class DiagnosisUpdateView(UpdateAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [IsDoctor]

class DiagnosisDetailView(RetrieveAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated , (IsPatient | IsDoctor)]

    def get_queryset(self):
        """
        Allow patients to view only their own diagnosis,
        while doctors can view all diagnoses.
        """
        user = self.request.user
        if user.role == 'Doctor':
            return Diagnosis.objects.all()
        elif user.role == 'Patient':
            return Diagnosis.objects.filter(patient=user.patient_profile)
        

class LabResultsCreateView(CreateAPIView):
    serializer_class = LabResultsSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

class LabResultsListView(ListAPIView):
    serializer_class = LabResultsSerializer
    permission_classes = [IsAuthenticated, (IsDoctor | IsPatient)]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Doctor":
            return LabResults.objects.all()
        if user.role == "Patient":
            return LabResults.objects.filter(patient=user.patient_profile)

class LabResultsUpdateView(UpdateAPIView):
    queryset = LabResults.objects.all()
    serializer_class = LabResultsSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

class LabResultsDetailView(RetrieveAPIView):
    serializer_class = LabResultsSerializer
    permission_classes = [IsAuthenticated , (IsPatient | IsDoctor)]

    def get_queryset(self):
        """
        Allow patients to view only their own diagnosis,
        while doctors can view all diagnoses.
        """
        user = self.request.user
        if user.role == 'Doctor':
            return LabResults.objects.all()
        elif user.role == 'Patient':
            return LabResults.objects.filter(patient=user.patient_profile)