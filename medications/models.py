from django.db import models

class Medication(models.Model):
    UNIT_CHOICES = [
        ('mg',  'mg'),
        ('g', 'g'),
        ('ml', 'ml'),
        ('l', ' (l)'),
        ('%', '%'),
        ('mcg', 'mcg'),
    ]

    generic_name = models.CharField(max_length=255)  # Generic name of the medication
    brand_name = models.CharField(max_length=255, blank=True, null=True)  # Brand name (optional)
    dosage_form = models.CharField(max_length=100)  # Form of the medication (e.g., Tablet, Syrup)
    strength = models.DecimalField(max_digits=10, decimal_places=2)  # Strength with 2 decimal places
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)  # Unit selection

    def __str__(self):
        return f"{self.generic_name} ({self.strength} {self.unit}) - {self.dosage_form}"
