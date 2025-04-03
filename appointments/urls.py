from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentListView,
    AppointmentDeleteView
)

urlpatterns = [
    path('appointments/create/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('my/appointments/<int:pk>/update-status/', AppointmentUpdateView.as_view(), name='update-appointment'),
    path('my/appointments/', AppointmentListView.as_view(), name='my-appointment'),
    path('my/appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='delete-appointment')
]