from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet

router = DefaultRouter()
router.register(r'medications', MedicationViewSet, basename='medication')

urlpatterns = [
    path('', include(router.urls)), 
]