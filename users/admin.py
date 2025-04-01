from django.contrib import admin
from .models import (
    CustomUser,
    PatientProfile,
    PharmacistProfile,
    DoctorProfile
)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PatientProfile)
admin.site.register(PharmacistProfile)
admin.site.register(DoctorProfile)
