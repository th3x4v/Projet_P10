from django.db import models
from django.conf import settings


class Contributor(models.Model):
    """Represents a user who contributes to a project"""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to="Project", on_delete=models.CASCADE)


class Project(models.Model):
    """Represents a project in the SoftDesk Support system"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=20)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(through="Contributor")

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """Represents a user who contributes to a project"""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to="Project", on_delete=models.CASCADE)


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
    assigned_to = models.ForeignKey(
        Contributor, on_delete=models.CASCADE, related_name="assigned_issues"
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
        related_name="authored_comments",
    )
    unique_identifier = models.UUIDField()
    time_created = models.DateTimeField(auto_now_add=True)
