import re

from django import template
from django.conf import settings

from social.backends.utils import load_backends
from social.backends.oauth import OAuthAuth

from psa.models import SecondaryEmail

from collections import defaultdict

register = template.Library()

name_re = re.compile(r'([^O])Auth')


@register.filter
def backend_name(backend):
    name = backend.__class__.__name__
    name = name.replace('OAuth', ' OAuth')
    name = name.replace('OpenId', ' OpenId')
    name = name.replace('Sandbox', '')
    name = name_re.sub(r'\1 Auth', name)
    return name


@register.filter
def backend_class(backend):
    return backend.name.replace('-', ' ')


@register.filter
def icon_name(name):
    return {
        'stackoverflow': 'stack-overflow',
        'google-oauth': 'google',
        'google-oauth2': 'google',
        'google-openidconnect': 'google',
        'yahoo-oauth': 'yahoo',
        'facebook-app': 'facebook',
        'email': 'envelope',
        'vimeo': 'vimeo-square',
        'linkedin-oauth2': 'linkedin',
        'vk-oauth2': 'vk',
        'live': 'windows',
        'username': 'user',
    }.get(name, name)


@register.filter
def social_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if name not in ['username', 'email']]
    backends.sort(key=lambda b: b[0])

    return [backends[n:n + 10] for n in range(0, len(backends), 10)]


@register.filter
def legacy_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if name in ['username', 'email']]
    backends.sort(key=lambda b: b[0])

    return [backends[n:n + 10] for n in range(0, len(backends), 10)]


@register.filter
def all_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()]
    backends.sort(key=lambda b: b[0])

    return [backends[n:n + 10] for n in range(0, len(backends), 10)]


@register.filter
def oauth_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if issubclass(backend, OAuthAuth)]
    backends.sort(key=lambda b: b[0])
    return backends


@register.simple_tag(takes_context=True)
def associated(context, backend):
    user = context.get('user')
    context['association'] = None
    if user and user.is_authenticated():
        try:
            context['association'] = user.social_auth.filter(
                provider=backend.name
            )[0]
        except IndexError:
            pass
    return ''


@register.simple_tag(takes_context=True)
def anonym_email(context):
    email = context['user'].anonymemail_set.all()
    if email:
        context['a_email'] = email[0].email
    return ''


@register.simple_tag(takes_context=True)
def similar_backends(context):
    backends = load_backends(settings.AUTHENTICATION_BACKENDS)
    user = context.get('user')

    secondary_users = SecondaryEmail.objects.filter(email=user.email)
    similar_users = defaultdict(list)

    for secondary in secondary_users:
        similar_users[secondary.user].append(backends.get(secondary.provider.provider))

    similar_users = dict(similar_users)
    # for k, v in similar_users.iteritems():
    #     print(v)
    #     v.sort(key=lambda b: b[0])
    #     similar_users[k] = [v[n:n + 10] for n in range(0, len(v), 10)]

    context['similar_users'] = similar_users
    return ''
