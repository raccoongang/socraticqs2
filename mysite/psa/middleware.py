from social_django.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from social_core import exceptions as social_exceptions
from django.contrib import messages


class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    """Handler for Social exceptions such as AuthAlreadyAssociated"""
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            user_id = request.user.id
            messages.add_message(request, messages.INFO, exception)
            if user_id:
                return HttpResponseRedirect(reverse('accounts:settings'))
            else:
                return HttpResponseRedirect(reverse('ctms:my_courses'))
        else:
            return
