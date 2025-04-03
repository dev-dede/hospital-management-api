from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentUpdateView,
)

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('my/<int:pk>/update-status/', AppointmentUpdateView.as_view(), name='update-appointment')
]