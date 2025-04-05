from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.routers import DefaultRouter
from .views import (
    Register,
    UserUpdateRetrieveView,
    UserListView,
    PatientProfileView,
    DoctorProfileView,
    PharmacistProfileView,
    LogoutAPIView,
)

router = DefaultRouter()
router.register(r'patient-profile', PatientProfileView, basename='patient-profile')
router.register(r'doctor-profile', DoctorProfileView, basename='doctor-profile')
router.register(r'pharmacist-profile', PharmacistProfileView, basename='pharmacist-profile')

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('me/', UserUpdateRetrieveView.as_view(), name='me'),
    path('all/',UserListView.as_view(), name='all_users'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Api endpoint for CRUD on userprofiles
    path('', include(router.urls)),
]