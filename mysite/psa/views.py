from json import dumps

from django.db.models import Q
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.http import JsonResponse
from django.template import RequestContext

from social.backends.utils import load_backends

from psa.utils import render_to
from psa.models import SecondaryEmail, TokenForgotPassword
from psa.pipeline import union_merge
from psa.mail import send_forgot_password


def context(**extra):
    """
    Adding default context to rendered page.
    """
    return dict({
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS),
    }, **extra)


@render_to('psa/custom_login.html')
def validation_sent(request):
    """
    View to handle validation_send action.
    """
    user = request.user
    social_list = []
    email = request.session.get('email_validation_address')
    if user and user.is_anonymous():
        by_secondary = [i.provider.provider for i in
                        SecondaryEmail.objects.filter(email=email)
                        if not i.provider.provider == u'email']
        social_list.extend(by_secondary)

        users_by_email = User.objects.filter(email=email)
        for user_by_email in users_by_email:
            by_primary = [i.provider for i in
                          user_by_email.social_auth.all()
                          if not i.provider == u'email' and
                          not SecondaryEmail.objects.filter(
                              ~Q(email=email), provider=i, user=user_by_email
                          ).exists()]
            social_list.extend(by_primary)

    return context(
        validation_sent=True,
        email=email,
        social_propose=bool(social_list),
        social_list=social_list
    )


def custom_login(request):
    """
    Custom login to integrate social auth and default login.
    """
    username = password = ''
    tmp_user = request.user
    user_is_temporary = tmp_user.groups.filter(name='Temporary').exists()
    if not user_is_temporary:
        logout(request)

    kwargs = dict(available_backends=load_backends(settings.AUTHENTICATION_BACKENDS))
    if request.POST:
        params = request.POST
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user_is_temporary:
                    union_merge(tmp_user, user)
                login(request, user)
                return redirect(request.POST.get('next', '/ct/'))
    else:
        params = request.GET
    if 'next' in params:  # must pass through for both GET or POST
        kwargs['next'] = params['next']

    if user_is_temporary:
        kwargs['temporary_user_message'] = '''You have accessed to a Courses without signing in.
                                              You can login using following methods and your progress
                                              will be saved.'''
    return render_to_response(
        'psa/custom_login.html', context_instance=RequestContext(request, kwargs)
    )


def custom_add_user(request):
    """
    Create new django user
    """
    name = request.POST.get('name')
    password = request.POST.get('password')
    next = request.POST.get('next')
    (user, create) = User.objects.get_or_create(username=name)
    if not create:
        return HttpResponse(dumps({'message':'Such user is already exist'}),
                            status = 400)
    if len(password) == 0:
        return HttpResponse(dumps({'message':'Password field required'}),
                            status = 400)
    user.password = password
    user.save()
    authenticate(username=user.username, password=user.password)
    return redirect(next)


@login_required
@render_to('ct/person.html')
def done(request):
    """
    Login complete view, displays user data.
    """
    return context(person=request.user)


@login_required
@render_to('ct/index.html')
def ask_stranger(request):
    """
    View to handle stranger whend asking email.
    """
    return context(tmp_email_ask=True)


@login_required
@render_to('ct/person.html')
def set_pass(request):
    """
    View to handle password set / change action.
    """
    changed = False
    user = request.user
    if user.is_authenticated():
        if request.POST:
            password = request.POST['pass']
            confirm = request.POST['confirm']
            if password == confirm:
                user.set_password(password)
                user.save()
                changed = True
    if changed:
        return context(changed=True, person=user)
    else:
        return context(exception='Something goes wrong...', person=user)


def forgot_pass(request):
    email = request.POST['username']
    next_url = request.POST.get('next', '/')
    user = User.objects.filter(email=email).first()
    if user:
        token = TokenForgotPassword(
            user=user,
            next_url=next_url,
        )
        token.save()
        url = request.build_absolute_uri(token.get_absolute_url())
        send_forgot_password(user, url)
        response = {
            "success": True,
            "msg": "Password reset link has been sent for you"
        }
    else:
        response = {
            "success": False,
            "msg": 'User with email {0} was not found'.format(email)
        }

    if request.is_ajax():
        return JsonResponse(response)
    else:
        cntx = RequestContext(request)
        cntx.update(response)
        return render_to_response('psa/reset_password.html', cntx)


@render_to('psa/reset_password.html')
def reset_pass(request, reset_token):
    token = TokenForgotPassword.objects.filter(token=reset_token).first()
    if request.method == 'GET':
        if token:
            return context(reset_token=reset_token)
        else:
            return context(msg="Token has expired")
    elif request.method == 'POST':
        password = request.POST['password']
        if password == request.POST['password1']:
            if token:
                next_url = token.next_url
                user = token.user
                user.set_password(password)
                token.delete()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return context(next_url=next_url)
            else:
                return context(msg="Token has expired")
        else:
            return context(reset_token=reset_token, msg="Password mismatch, enter again")
