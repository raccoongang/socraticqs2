from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
    """
    Dummy model for testing.
    """
    title = models.CharField(max_length=32)
    description = models.TextField()
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
