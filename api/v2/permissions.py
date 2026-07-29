from rest_framework import permissions

from accounts.models import Role


class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to Administrator users.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, "profile")
            and request.user.profile.role == Role.ADMINISTRATOR
        )


class IsSOCManager(permissions.BasePermission):
    """
    Allows access to SOC Managers (and Administrators, usually used in combination).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, "profile")
            and request.user.profile.role == Role.SOC_MANAGER
        )


class IsSOCAnalyst(permissions.BasePermission):
    """
    Allows access to SOC Analysts.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, "profile")
            and request.user.profile.role == Role.SOC_ANALYST
        )


class IsReadOnly(permissions.BasePermission):
    """
    Allows access only for safe methods (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsReadOnlyAnalyst(permissions.BasePermission):
    """
    Specifically for the Read Only Analyst role.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, "profile")
            and request.user.profile.role == Role.READ_ONLY_ANALYST
        )


class IsOwnerOrAssignedAnalyst(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or assigned analysts to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (if combined with other perms in view)
        # So we only check write permissions here.
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = False
        is_assigned = False

        if (
            hasattr(obj, "created_by")
            and obj.created_by == request.user
            or hasattr(obj, "user")
            and obj.user == request.user
        ):
            is_owner = True

        if hasattr(obj, "assigned_to") and obj.assigned_to == request.user:
            is_assigned = True

        return is_owner or is_assigned


class IsAdminOrManagerOrAssignedAnalyst(permissions.BasePermission):
    """
    Composite permission for Incidents:
    Admins and Managers can do anything.
    Analysts can only update if assigned.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not hasattr(request.user, "profile"):
            return False

        role = request.user.profile.role

        # Read operations allowed for all roles (Read Only analyst will be handled by a separate class or at view level)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins and Managers have global write permissions
        if role in [Role.ADMINISTRATOR, Role.SOC_MANAGER]:
            return True

        # SOC Analysts can write (will be checked by object permission)
        if role == Role.SOC_ANALYST:
            # We don't allow DELETE for Analysts at all
            if request.method == "DELETE":
                return False
            return True

        # Read Only Analyst
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        role = request.user.profile.role
        if role in [Role.ADMINISTRATOR, Role.SOC_MANAGER]:
            return True

        if role == Role.SOC_ANALYST:
            # Analyst can only update if they are assigned
            return getattr(obj, "assigned_to", None) == request.user

        return False


class IsAdminOrManager(permissions.BasePermission):
    """
    Allows access to Admins or Managers.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not hasattr(request.user, "profile"):
            return False

        return request.user.profile.role in [Role.ADMINISTRATOR, Role.SOC_MANAGER]


class IsAdmin(permissions.BasePermission):
    """
    Global admin permission.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, "profile")
            and request.user.profile.role == Role.ADMINISTRATOR
        )
