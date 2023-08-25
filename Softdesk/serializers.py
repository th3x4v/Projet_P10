from rest_framework import serializers
from Softdesk.models import Project, Issue, Comment, Contributor
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user_id"]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "project_type", "author_user_id"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "project_type",
            "author_user_id",
            "contributors_id",
            "issues",
        ]

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "priority",
            "project_id",
            "assigned_to_user_id",
            "status",
            "time_created",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "tag",
            "project_id",
            "assigned_to_user_id",
            "status",
            "time_created",
            "comments",
        ]

    def get_comments(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "author_user_id",
            "time_created",
            "unique_identifier",
        ]
