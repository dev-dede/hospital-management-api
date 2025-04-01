from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    CustomUser,
    PatientProfile,
    PharmacistProfile,
    DoctorProfile,
)

@receiver(post_save, sender=CustomUser)
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

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        """
        Ensures the profile is saved when the user is saved.
        This makes sure any updates are also reflected in the profile.
        """
        if instance.role == "Doctor":
            instance.doctorprofile.save()
        if instance.role == "Patient":
            instance.patientprofile.save()
        if instance.role == "Pharmacist":
            instance.pharmacistprofile.save()
