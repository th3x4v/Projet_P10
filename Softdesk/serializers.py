from rest_framework import serializers
from Softdesk.models import Project, Issue, Comment, Contributor


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project"]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "project_type", "author"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "project_type",
            "author",
            "issues",
        ]

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project=instance.id)
        return IssueListSerializer(queryset, many=True).data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "priority",
            "project",
            "assigned_to",
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
            "project",
            "assigned_to",
            "status",
            "time_created",
            "comments",
            "author",
        ]

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue=instance.id)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "unique_identifier",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "author", "time_created", "unique_identifier", "issue"]
