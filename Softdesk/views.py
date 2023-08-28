from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User

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
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "update"
            and self.detail_serializer_class is not None
        ):
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        print(kwargs)
        # Make a mutable copy of the request data
        mutable_data = request.data.copy()

        # Include the authenticated user as the author in the copy
        mutable_data["author"] = request.user.pk

        # for Issue creation
        if self.kwargs["project_pk"] is not None:
            mutable_data["project"] = self.kwargs["project_pk"]

        # for Comment creation
        if self.kwargs["issue_pk"] is not None:
            mutable_data["issue"] = self.kwargs["issue_pk"]

        # Use the detail_serializer_class for creation
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)

        print(serializer)
        # Save the instance and return the response
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def perform_create(self, serializer):
        # Save the project instance and get the created object
        project = serializer.save()

        # Creation of contributor object using the related_name attribute contributors
        project.contributors.create(user=project.author)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
