import time
from functools import wraps
from datetime import datetime

from django.contrib.auth import login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs) or {}
            if isinstance(out, dict):
                out['request'] = request
                out = render_to_response(tpl, out, RequestContext(request))
            return out
        return wrapper
    return decorator


def make_temporary(request, expiry_interval=None):
    """
    Creates Temporary user and return one.
    """
    _id = int(time.mktime(datetime.now().timetuple()))
    user = request.user
    user, user_created = User.objects.get_or_create(
        username='anonymous' + str(_id),
        first_name='Temporary User'
    )
    temporary_group, group_created = Group.objects.get_or_create(name='Temporary')
    user.groups.add(temporary_group)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    # Set expiry time to year in future
    if not expiry_interval:
        expiry_interval = 31536000
    request.session.set_expiry(expiry_interval)
    return user
