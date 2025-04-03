from rest_framework.urls import path
from .views import (
    MedicalRecordCreateView,
)

urlpatterns = [
    path('create/', MedicalRecordCreateView.as_view(), name='create-medical-record')
]