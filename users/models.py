from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from datetime import date

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, role="Patient"):
        if not first_name:
            raise ValueError("Please input your first name")
        if not last_name:
            raise ValueError("Please input you last name")
        if not email:
            raise ValueError("Please input your email")
        
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, first_name, last_name, email, password=None, role="Admin"):
        user = self.create_user(first_name, last_name, email, password, role)

        user.is_staff = True
        user.is_superuser = True
        user.role = "Admin"

        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("Patient", "Patient"),
        ("Doctor", "Doctor"),
        ("Pharmacist", "Pharmacist"),
        ("Admin", "Admin"),
    ]
    username = None # Email is used as login field
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Patient")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name()} ({self.email}) - {self.role}"
    
class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    #emergency_contact = models.ForeignKey(EmergencyContactPerson, related_name='patient_profile', on_delete=models.SET_NULL, null=True)

    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None # Return None if date of birth is not set to calculate age
    
    
    def get_full_name(self):
        return self.user.get_full_name()
    
    def __str__(self):
        return f"Profile of {self.user.first_name} {self.user.last_name} ({self.id})"

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    def get_full_name(self):
        return self.user.get_full_name()
    
    def __str__(self):
        return f"Profile of Dr.{self.user.get_full_name()}"
class PharmacistProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pharmacist_profile')
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    def get_full_name(self):
        return self.user.get_full_name()
    
    def __str__(self):
        return f"Profile of Pharm.{self.user.get_full_name()}"