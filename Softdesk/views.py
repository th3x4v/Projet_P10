from rest_framework.viewsets import ModelViewSet
from .models import Project, Issue, Comment, Contributor
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserSerializer,
    ProjectListSerializer,
    IssueListSerializer,
    CommentListSerializer,
    ContributorSerializer,
    ProjectDetailSerializer,
)


class MultipleSerializerMixin:
    """
    Get detail serializer class
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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        project = super(ProjectViewSet, self).create(request, *args, **kwargs)
        contributor = Contributor.objects.create(
            user=request.user,
            project=Project.objects.filter(id=project.data["id"]).first(),
        )
        contributor.save()

        return Response(project.data, status=status.HTTP_201_CREATED)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
