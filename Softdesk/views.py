from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from Softdesk.permissions import IsContributor, AuthorOrReadOnly


from .models import Project, Issue, Comment, Contributor

from .serializers import (
    ProjectListSerializer,
    IssueListSerializer,
    CommentListSerializer,
    ContributorSerializer,
    ProjectDetailSerializer,
    IssueDetailSerializer,
    CommentDetailSerializer,
)


class MultipleSerializerMixin:
    """
    A mixin class that provides dynamic serializer selection based on the view action.

    This mixin is designed to be used with Django Rest Framework's ModelViewSet classes
    to automatically choose the appropriate serializer class based on the action
    (create, retrieve, update, partial_update).

    Attributes:
        detail_serializer_class (serializer): The serializer class to use for detail actions (retrieve).
        serializer_class (serializer): The serializer class to use for non-detail actions (create, update).

    Methods:
        get_serializer_class(): Returns the appropriate serializer class based on the view action.
    """

    def get_serializer_class(self):
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "partial_update"
            or self.action == "update"
            and self.detail_serializer_class is not None
        ):
            return self.detail_serializer_class
        return self.serializer_class


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    A viewset for managing Project instances.

    This viewset provides CRUD (Create, Retrieve, Update, Delete) operations for Project instances.
    It also customizes the queryset to only include projects where the user is a contributor.

    Attributes:
        permission_classes (list): The permission classes required for accessing this viewset.
        queryset (queryset): The initial queryset for retrieving projects.
        serializer_class (serializer): The serializer class for listing projects.
        detail_serializer_class (serializer): The serializer class for detailed project views.

    Methods:
        get_queryset(): Returns a queryset filtered to include projects where the user is a contributor.
        perform_create(serializer): Customizes project creation to include the project's author as a contributor.
    """

    permission_classes = [AuthorOrReadOnly, IsContributor, IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            project_list = Project.objects.all()
        else:
            project_list = Project.objects.filter(contributors__user=user)
        return project_list

    def perform_create(self, serializer):
        # Save the project instance and get the created object
        project = serializer.save(author=self.request.user)

        # Creation of contributor object using the related_name attribute contributors
        project.contributors.create(user=project.author)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    A viewset for managing Issue instances within a Project.

    This viewset provides CRUD (Create, Retrieve, Update, Delete) operations for Issue instances
    that are associated with a specific Project.

    Attributes:
        permission_classes (list): The permission classes required for accessing this viewset.
        queryset (queryset): The initial queryset for retrieving issues.
        serializer_class (serializer): The serializer class for listing issues.
        detail_serializer_class (serializer): The serializer class for detailed issue views.

    Methods:
        get_queryset(): Returns a queryset filtered to include issues within the specified project.
        perform_create(serializer): Customizes issue creation to associate it with the project and set the author.
    """

    permission_classes = [AuthorOrReadOnly, IsContributor, IsAuthenticated]
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project_id = self.kwargs["project_pk"]
        project = Project.objects.get(id=project_id)
        # Save the project instance and get the created object
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    A viewset for managing Comment instances within an Issue.

    This viewset provides CRUD (Create, Retrieve, Update, Delete) operations for Comment instances
    that are associated with a specific Issue.

    Attributes:
        permission_classes (list): The permission classes required for accessing this viewset.
        queryset (queryset): The initial queryset for retrieving comments.
        serializer_class (serializer): The serializer class for listing comments.
        detail_serializer_class (serializer): The serializer class for detailed comment views.

    Methods:
        get_queryset(): Returns a queryset filtered to include comments within the specified issue.
        perform_create(serializer): Customizes comment creation to associate it with the issue and set the author.
    """

    permission_classes = [AuthorOrReadOnly, IsContributor, IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        issue_id = self.kwargs["issue_pk"]
        issue = Issue.objects.get(id=issue_id)
        # Save the project instance and get the created object
        issue = serializer.save(author=self.request.user, issue=issue)


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    A viewset for managing Contributor instances within a Project.

    This viewset provides CRUD (Create, Retrieve, Update, Delete) operations for Contributor instances
    that are associated with a specific Project.

    Attributes:
        permission_classes (list): The permission classes required for accessing this viewset.
        queryset (queryset): The initial queryset for retrieving contributors.
        serializer_class (serializer): The serializer class for listing contributors.
        detail_serializer_class (serializer): The serializer class for detailed contributor views.

    Methods:
        get_queryset(): Returns a queryset filtered to include contributors within the specified project.
        perform_create(serializer): Customizes contributor creation to associate it with the project.
    """

    permission_classes = [IsContributor, IsAuthenticated]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorSerializer

    def get_queryset(self):
        # getting the current project
        project_id = self.kwargs["project_pk"]
        queryset = Contributor.objects.filter(project=project_id)
        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs["project_pk"]
        project = Project.objects.get(id=project_id)
        # Save the project instance and get the created object
        serializer.save(project=project)
