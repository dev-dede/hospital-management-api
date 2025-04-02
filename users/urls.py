from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.routers import DefaultRouter
from .views import (
    Register,
    PatientProfileView,
    DoctorProfileView,
    PharmacistProfileView,
)

router = DefaultRouter()
router.register(r'patient-profile', PatientProfileView, basename='patient-profile')
router.register(r'doctor-profile', DoctorProfileView, basename='doctor-profile')
router.register(r'pharmacist-profile', PharmacistProfileView, basename='pharmacist-profile')

urlpatterns = [
    path('register/', Register.as_view(), name='register')
    
    # Api endpoint for CRUD on userprofiles
    path('', include(router.urls))

    # Api endpoint for token generation
    path('api-token-auth/', views.obtain_auth_token)
]