from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    """
    Custom permission class for controlling object-level permissions related to authors and read-only access.

    This permission class checks if the user has the necessary permissions to perform actions on objects
    based on whether they are the author of the object or have read-only access. It also allows superusers
    unrestricted access.

    Attributes:
        None

    Methods:
        - has_object_permission(self, request, view, obj): Checks if the user has permission to perform the
          specified action on the given object.

    """

    def has_object_permission(self, request, view, obj):
        project_pk = view.kwargs.get("project_pk")
        pk = view.kwargs.get("pk")
        user = request.user
        if project_pk is None:
            if pk is None:
                return True
            else:
                project_id = pk
        else:
            project_id = project_pk

        if request.method in SAFE_METHODS:
            user.contributor_set.filter(
                project_id=project_id
            ).exists() or request.user.is_superuser
            return (
                user.contributor_set.filter(project_id=project_id).exists()
                or request.user.is_superuser
            )
        else:
            if obj.author == request.user:
                print("author")
                return True
            return False


class IsContributor(BasePermission):
    """
    Custom permission class for allowing access only to contributors of a project.

    This permission class checks if the user is a contributor to a specific project or if they are a superuser.
    It is designed to restrict access to certain views based on project-related permissions.

    Attributes:
        None

    Methods:
        - has_permission(self, request, view): Checks if the user has permission to access a view based on
          their contributor status or superuser status.

    """

    def has_permission(self, request, view):
        project_pk = view.kwargs.get("project_pk")
        pk = view.kwargs.get("pk")
        user = request.user
        if project_pk is None:
            if pk is None:
                return True
            else:
                project_id = pk
        else:
            project_id = project_pk
        return user.is_authenticated and (
            user.contributor_set.filter(project_id=project_id).exists()
            or request.user.is_superuser
        )
