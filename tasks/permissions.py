from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and request.user.role == "manager"
    

    def has_object_permissions(self,request,view,obj ):

        if request.user.role == "manager":
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.assigned_users.all()
        

        return False