import time
from functools import wraps
from datetime import datetime

from django.contrib.auth import login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group


DEFAULT_EXPIRY_INTERVAL = 31536000


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


def make_temporary(expiry_interval=DEFAULT_EXPIRY_INTERVAL):
    """
    Actual decorator for creating Temporary users.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated():
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
                request.session.set_expiry(expiry_interval)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def preview_access(function=None, expiry_interval=DEFAULT_EXPIRY_INTERVAL):
    """
    Decorator for views that creates Temporary user under the hood.
    """
    actual_decorator = make_temporary(expiry_interval=expiry_interval)
    if function:
        return actual_decorator(function)
    return actual_decorator
