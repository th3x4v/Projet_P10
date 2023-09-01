from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("object")
        print(view.kwargs)
        project_pk = view.kwargs.get("project_pk")
        pk = view.kwargs.get("pk")
        user = request.user
        print("user")
        print(user)
        print("request")
        print(request)
        print("project_pk")
        print(project_pk)
        print("pk")
        print(pk)
        if project_pk is None:
            if pk is None:
                print("true")
                return True
            else:
                project_id = pk
        else:
            project_id = project_pk

        if request.method in SAFE_METHODS:
            print("safe_method")
            user.contributor_set.filter(
                project_id=project_id
            ).exists() or request.user.is_superuser
            return (
                user.contributor_set.filter(project_id=project_id).exists()
                or request.user.is_superuser
            )
        else:
            print("no safe_method")
            if obj.author == request.user:
                print("author")
                return True
            return False


class IsContributor(BasePermission):
    """
    Allows access only to contributors to a project.
    """

    def has_permission(self, request, view):
        print("is contibutor permission")
        print(view.kwargs)
        project_pk = view.kwargs.get("project_pk")
        pk = view.kwargs.get("pk")
        user = request.user
        print("user")
        print(user)
        print("request")
        print(request)
        print("project_pk")
        print(project_pk)
        print("pk")
        print(pk)
        if project_pk is None:
            if pk is None:
                return True
            else:
                project_id = pk
        else:
            project_id = project_pk
        print("project_id")
        print(project_id)
        return user.is_authenticated and (
            user.contributor_set.filter(project_id=project_id).exists()
            or request.user.is_superuser
        )


"""
Create Project: Everyone connected can create a Project.
Permission: IsAuthenticated
List Projects: Everyone connected can see the list of Projects.
Permission: IsAuthenticated
Retrieve Project Details: Only contributors of a project can see information about that project, including contributors, issues, and comments related to the project.
Permission: IsContributor
Create Contributor: Contributors of a project can create a contributor for that project.
Permission: IsContributor
List Contributors: Contributors of a project can see the list of contributors for that project.
Permission: IsContributor
Retrieve Contributor Details: Contributors of a project can see details of other contributors in the same project.
Permission: IsContributor
Create Issue: Contributors of a project can create an issue for that project.
Permission: IsContributor
List Issues: Contributors of a project can see the list of issues for that project.
Permission: IsContributor
Retrieve Issue Details: Contributors of a project can see details of an issue in the same project.
Permission: IsContributor
Create Comment: Contributors of a project can create a comment on an issue in that project.
Permission: IsContributor
List Comments: Contributors of a project can see the list of comments for issues in that project.
Permission: IsContributor
Retrieve Comment Details: Contributors of a project can see details of a comment on an issue in the same project.
Permission: IsContributor"""
