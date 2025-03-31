from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, role=None):
        if not first_name:
            raise ValueError("Please input your first name")
        if not last_name:
            raise ValueError("Please input you last name")
        if not email:
            raise ValueError("Please input your email")
        
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(first_name, last_name, email, password)

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
        return f"{self.email} - {self.role}"
