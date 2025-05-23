from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
#from rest_framework.authtoken.models import Token
from .models import (
    PatientProfile,
    PharmacistProfile,
    DoctorProfile,
)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a profile when a new user is created.
    The profile type depends on the user's role.
    """
    if created:
        if instance.role == "Doctor":
            DoctorProfile.objects.create(user=instance)
        elif instance.role == "Patient":
            PatientProfile.objects.create(user=instance)
        elif instance.role == "Pharmacist":
            PharmacistProfile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        """
        Ensures the profile is saved when the user is saved.
        This makes sure any updates are also reflected in the profile.
        """
        if instance.role == "Doctor":
            instance.doctor_profile.save()
        if instance.role == "Patient":
            instance.patient_profile.save()
        if instance.role == "Pharmacist":
            instance.pharmacist_profile.save()

# Token is created in serializer instead of using postsave signals per the drf documentation
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)