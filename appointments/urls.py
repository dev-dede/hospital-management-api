from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentListView,
)

urlpatterns = [
    path('appointments/create/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('my/appointments/<int:pk>/update-status/', AppointmentUpdateView.as_view(), name='update-appointment'),
    path('my/appointments/', AppointmentListView.as_view(), name='my-appointment')
]