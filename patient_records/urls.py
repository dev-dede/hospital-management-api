from rest_framework.urls import path
from .views import (
    MedicalRecordCreateView, MedicalRecordListView, MedicalRecordDetailView, MedicalRecordUpdateView,
    DiagnosisCreateView, DiagnosisListView,
)

urlpatterns = [
    # Medical record urls
    path('medical-records/create/', MedicalRecordCreateView.as_view(), name='create-medical-record'),
    path('medical-records/', MedicalRecordListView.as_view(), name='list-medical-record'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='detail-medical-record'),
    path('medical-records/<int:pk>/update/', MedicalRecordUpdateView.as_view(), name='update-medical-record'),

    # Diagnosis uls
    path('diagnosis/create/', DiagnosisCreateView.as_view(), name='create-diagnosis'),
    path('diagnosis/', DiagnosisListView.as_view(), name='list-diagnosis'),
    
    
]