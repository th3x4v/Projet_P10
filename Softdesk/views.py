from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Softdesk.permissions import IsContributor, AuthorOrReadOnly
from rest_framework.exceptions import PermissionDenied

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
    Get the right serializer for the current action
    """

    def get_serializer_class(self):
        print(self.action)
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "partial_update"
            or self.action == "update"
            and self.detail_serializer_class is not None
        ):
            return self.detail_serializer_class
        return self.serializer_class

    # def create(self, request, *args, **kwargs):
    #     # Make a mutable copy of the request data
    #     mutable_data = request.data.copy()
    #     print(self.kwargs)

    #     # Include the authenticated user as the author in the copy
    #     mutable_data["author"] = request.user.pk

    #     # Identify the project id for Issue or Contributor creation
    #     try:
    #         mutable_data["project"] = self.kwargs["project_pk"]
    #     except:
    #         pass

    #     # Identify the issue id for Comment creation
    #     try:
    #         mutable_data["issue"] = self.kwargs["issue_pk"]
    #     except:
    #         pass

    #     # Use the detail_serializer_class for creation
    #     serializer = self.get_serializer(data=mutable_data)
    #     serializer.is_valid(raise_exception=True)
    #     # Save the instance and return the response
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)

    #     return Response(
    #         serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    permission_classes = [AuthorOrReadOnly, IsContributor, IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    # def perform_create(self, serializer):
    #     # Save the project instance and get the created object
    #     project = serializer.save()

    #     # Creation of contributor object using the related_name attribute contributors
    #     project.contributors.create(user=project.author)

    def get_queryset(self):
        """Return a queryset only of the project the user is contributor to"""
        user = self.request.user
        return Project.objects.filter(contributors__user=user)

    def perform_create(self, serializer):
        # Save the project instance and get the created object
        project = serializer.save(author=self.request.user)

        # Creation of contributor object using the related_name attribute contributors
        project.contributors.create(user=project.author)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
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
        issue = serializer.save(author=self.request.user, project=project)


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
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
        contributor = serializer.save(project=project)
