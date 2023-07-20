from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    '''Only staff users can access'''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Only author of the content or staff has access'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool((request.user and obj.author == request.user) or request.user.is_staff)
        
class IsUserOrReadOnly(permissions.BasePermission):
    '''Only user(personal access) and staff have permissions'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool((request.user and obj.user == request.user) or request.user.is_staff)