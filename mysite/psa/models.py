from uuid import uuid4
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in

from social.apps.django_app.default.models import UserSocialAuth


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


class SecondaryEmail(models.Model):
    """Model for storing secondary emails

    We can store emails here from social_auth
    or LTI login.
    """
    user = models.ForeignKey(User, related_name='secondary')
    provider = models.ForeignKey(UserSocialAuth)
    email = models.EmailField(verbose_name='Secondary Email')

    class Meta:
        unique_together = ('provider', 'email')


class UserSession(models.Model):
    """User<->Session model

    Model for linking user to session.
    Solution from http://gavinballard.com/associating-django-users-sessions/
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)


def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Create UserSession object to store User<=>Session relation.
    """
    if user.groups.filter(name='Temporary').exists():
        if not Session.objects.filter(session_key=request.session.session_key).exists():
            request.session.save()

        UserSession.objects.get_or_create(
            user=user,
            session_id=request.session.session_key
        )


user_logged_in.connect(user_logged_in_handler)


def create_token():
    return str(uuid4().get_hex())


class TokenForgotPassword(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(default=create_token, max_length=32)
    next_url = models.CharField(max_length=200)

    def get_absolute_url(self):

        return reverse('reset-password', kwargs={'reset_token': self.token})
