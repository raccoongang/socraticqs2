from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in

class AnonymEmail(models.Model):
    """Temporary anonymous user emails

    Model for temporary storing anonymous user emails
    to allow to restore anonymous sessions.
    """
    user = models.ForeignKey(User)
    email = models.CharField(max_length=64)
    date = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'email')
        ordering = ['-date']


class UserSession(models.Model):
    """User<->Session model

    Model for linking user to session.
    Solution from http://gavinballard.com/associating-django-users-sessions/
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)


def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key
    )


user_logged_in.connect(user_logged_in_handler)
