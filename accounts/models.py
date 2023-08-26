from django.contrib.auth.models import AbstractUser
from django.db import models

# https://docs.djangoproject.com/fr/4.0/topics/auth/customizing/
# using-a-custom-user-model-when-starting-a-project


class User(AbstractUser):
    """Represent a Custom user"""

    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField()
    can_data_be_shared = models.BooleanField()


