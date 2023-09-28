from rest_framework import serializers
from Softdesk.models import Project, Issue, Comment, Contributor

from accounts.models import User
from accounts.serializers import UserListSerializer


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for Contributor model.
    Attributes:
        - Meta:
            model (Contributor): The Contributor model class to serialize.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that should be read-only.

    Methods:
        - get_user(self, instance): Retrieves user data associated with the Contributor.

    """

    class Meta:
        model = Contributor
        fields = ["user", "project"]
        read_only_fields = ["project"]

    def get_user(self, instance):
        queryset = User.objects.filter(id=instance.user_id)
        return UserListSerializer(queryset, many=True).data


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model used in list views.

    Attributes:
        - Meta:
            model (Project): The Project model class to serialize.
            fields (list): The fields to include in the serialized data.

    """

    class Meta:
        model = Project
        fields = ["id", "name", "project_type", "author"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model used in detail views.

    Attributes:
        - Meta:
            model (Project): The Project model class to serialize.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that should be read-only.

    Methods:
        - get_issues(self, instance): Retrieves and serializes associated issues.

    """

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
        read_only_fields = ["author"]

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project=instance.id)
        return IssueListSerializer(queryset, many=True).data

    def validate_author(self, value):
        return value  # Bypass the validation for author field


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue model used in list views.

    Attributes:
        - Meta:
            model (Issue): The Issue model class to serialize.
            fields (list): The fields to include in the serialized data.

    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "priority",
            "project",
            "assigned_to",
            "status",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue model used in detail views.

    Attributes:
        - Meta:
            model (Issue): The Issue model class to serialize.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that should be read-only.

    Methods:
        - get_comments(self, instance): Retrieves and serializes associated comments.

    """

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
        read_only_fields = ["author", "project"]

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue=instance.id)
        return CommentListSerializer(queryset, many=True).data


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model used in list views.

    Attributes:
        - Meta:
            model (Comment): The Comment model class to serialize.
            fields (list): The fields to include in the serialized data.

    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "unique_identifier",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model used in detail views.

    Attributes:
        - Meta:
            model (Comment): The Comment model class to serialize.
            fields (list): The fields to include in the serialized data.

    """

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "time_created", "unique_identifier", "issue"]
        read_only_fields = ["author", "issue"]
