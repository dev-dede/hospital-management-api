from rest_framework.urls import path
from .views import (
    MedicalRecordCreateView,
    MedicalRecordListView,
    MedicalRecordDetailView
)

urlpatterns = [
    path('create/', MedicalRecordCreateView.as_view(), name='create-medical-record'),
    path('', MedicalRecordListView.as_view(), name='list-medical-record'),
    path('<int:pk>/', MedicalRecordDetailView.as_view(), name='detail-medical-record')
]