from rest_framework.viewsets import ModelViewSet
from .models import Project, Issue, Comment
from accounts.models import User

from .serializers import (
    UserSerializer,
    ProjectListSerializer,
    IssueListSerializer,
    CommentListSerializer,
    ProjectDetailSerializer,
    IssueDetailSerializer,
)


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
