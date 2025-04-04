from rest_framework import permissions

class IsPatient(permissions.BasePermission):
     """
    Allows access only to patients.
    """
     def has_permission(self, request, view):
          return request.user.role == "Patient"
     
class IsDoctor(permissions.BasePermission):
    """
    Allows access only to doctors.
    """
    def has_permission(self, request, view):
        return request.user.role == 'Doctor'

class IsPharmacist(permissions.BasePermission):
    """
    Allows access only to pharmacists.
    """
    def has_permission(self, request, view):
        return request.user.role == 'Pharmacist'

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admins.
    """
    def has_permission(self, request, view):
        return request.user.role == 'Admin'
    
class IsPharmacistOrReadOnly(permissions.BasePermission):
    """
    Custom permission: 
    - Pharmacists can CREATE, UPDATE, DELETE medications.
    - Doctors & Patients can only READ.
    """

    def has_permission(self, request, view):
        # Allow read-only access for GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow Pharmacists to modify data
        return request.user.role == 'Pharmacist'
