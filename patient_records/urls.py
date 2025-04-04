from rest_framework.urls import path
from .views import (
    MedicalRecordCreateView, MedicalRecordListView, MedicalRecordDetailView, MedicalRecordUpdateView,
    DiagnosisCreateView, DiagnosisListView, DiagnosisUpdateView, DiagnosisDetailView,
)

urlpatterns = [
    # Medical record urls
    path('medical-records/create/', MedicalRecordCreateView.as_view(), name='create-medical-record'),
    path('medical-records/', MedicalRecordListView.as_view(), name='list-medical-record'),
    path('medical-records/<int:pk>/detail/', MedicalRecordDetailView.as_view(), name='detail-medical-record'),
    path('medical-records/<int:pk>/update/', MedicalRecordUpdateView.as_view(), name='update-medical-record'),

    # Diagnosis uls
    path('diagnoses/create/', DiagnosisCreateView.as_view(), name='create-diagnosis'),
    path('diagnoses/', DiagnosisListView.as_view(), name='list-diagnosis'),
    path("diagnoses/<int:pk>/update/", DiagnosisUpdateView.as_view(), name="diagnosis-update"),
    path("diagnoses/<int:pk>/detail/", DiagnosisDetailView.as_view(), name="diagnosis-detail"),

]
