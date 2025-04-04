from django.contrib import admin
from .models import (
    MedicalRecord,
    Diagnosis,
    LabResult,
)

admin.site.register(MedicalRecord)
admin.site.register(Diagnosis)
admin.site.register(LabResult)
