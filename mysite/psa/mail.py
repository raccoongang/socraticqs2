"""
Module defined send_validation function to verify emails.
And send email forgot password
"""
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse


def send_validation(strategy, backend, code):
    """
    Send email validation link.
    """
    # TODO add email validating regex [^@]+@[^@]+\.[^@]+
    url = (reverse('social:complete', args=(backend.name,)) +
           '?verification_code=' + code.code)
    url = strategy.request.build_absolute_uri(url)
    send_mail(
        'Validate your account',
        'Validate your account {0}'.format(url),
        settings.EMAIL_FROM,
        [code.email],
        fail_silently=False
    )


def send_forgot_password(user, url):
    """
    Send email with reset link to user
    :param user:
    :param url:
    :return:
    """
    msg = EmailMultiAlternatives(
        "Reset your password",
        "Click on link to reset password",
        settings.EMAIL_FROM,
        [user.email,],)
    msg.attach_alternative("<html><body><a href='{1}'>"
                           "Reset password</a></body></html>".format(user, url), "text/html")
    msg.send()
