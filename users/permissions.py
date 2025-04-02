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
        return request.user.role == 'doctor'

class IsPharmacist(permissions.BasePermission):
    """
    Allows access only to pharmacists.
    """
    def has_permission(self, request, view):
        return request.user.role == 'pharmacist'

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admins.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'
