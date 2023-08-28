from django.db import models
from django.conf import settings
import uuid


class Contributor(models.Model):
    """Represents a user who contributes to a project"""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(
        to="Project", on_delete=models.CASCADE, related_name="contributors"
    )

    class Meta:
        unique_together = ("project", "user")


class Project(models.Model):
    """Represents a project in the SoftDesk Support system"""

    TYPES_CHOICES = (
        ("BACKEND", "Back-end"),
        ("FRONTEND", "Front-end"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=TYPES_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributors_id = models.ManyToManyField("Contributor", related_name="projects")

    def __str__(self):
        return self.name


class Issue(models.Model):
    """Represents an issue or problem within a project"""

    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    )
    TAG_CHOICES = (
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    )
    STATUS_CHOICES = (
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Finished", "Finished"),
    )

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=author,
        related_name="issue_assignee",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To Do")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Represents a comment made on an issue"""

    text = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField(auto_now_add=True)
