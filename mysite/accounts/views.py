from functools import partial

from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView, CreateView
from social.utils import build_absolute_uri, setting_name
from django.conf import settings

from accounts.forms import (
    UserForm, InstructorForm, ChangePasswordForm,
    DeleteAccountForm, ChangeEmailForm
)
from accounts.models import Instructor
from mysite.mixins import LoginRequiredMixin, NotAnonymousRequiredMixin
from .forms import SocialForm
from psa.custom_django_storage import CustomCode\


class AccountSettingsView(NotAnonymousRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            'accounts/settings.html',
            dict(
                user_form=UserForm(instance=request.user),
                instructor_form=InstructorForm(instance=request.user.instructor),
                password_form=ChangePasswordForm(),
                delete_account_form=DeleteAccountForm(instance=request.user),
                email_form=ChangeEmailForm(initial={'email': request.user.email}),
                person=request.user
            )
        )

    def post(self, request):
        form_name = {
            'user_form': partial(UserForm, instance=request.user),
            'instructor_form': partial(InstructorForm, instance=request.user.instructor),
            'email_form': partial(ChangeEmailForm, initial={'email': request.user.email}),
            'password_form': partial(ChangePasswordForm, instance=request.user),
            'delete_account_form': partial(DeleteAccountForm, instance=request.user),
        }
        kwargs = {}
        has_errors = False

        for form_id, form_cls in form_name.items():
            if form_id in request.POST.getlist('form_id'):
                form = form_cls(data=request.POST)
                if form.is_valid():
                    if form_id == 'email_form':
                        resp = form.save(request, commit=False)
                    else:
                        form.save()
                else:
                    has_errors = True
                kwargs[form_id] = form
            else:
                kwargs[form_id] = form_cls()

        kwargs['person'] = request.user
        if not has_errors:
            return HttpResponseRedirect(reverse('accounts:settings'))
        return render(
            request,
            'accounts/settings.html',
            kwargs
        )


class DeleteAccountView(NotAnonymousRequiredMixin, View):
    def post(self, request):
        form = DeleteAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            new_user = form.save()
            logout(request)
            return HttpResponseRedirect(reverse('accounts:deleted'))
        return render(
            request,
            'accounts/settings.html',
            dict(
                user_form=UserForm(instance=request.user),
                instructor_form=InstructorForm(instance=request.user.instructor),
                password_form=ChangePasswordForm(),
                delete_account_form=form,
                person=request.user
            )
        )


class ProfileUpdateView(NotAnonymousRequiredMixin, CreateView):
    template_name = 'accounts/profile_edit.html'

    model = Instructor
    form_class = SocialForm
    def get_success_url(self):
        return reverse('ctms:my_courses')

    def get_initial(self):
        return {
           'user': self.request.user,
        }

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'instance': self.get_instance()
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_instance(self):
        try:
            instructor = self.request.user.instructor
        except self.request.user._meta.model.instructor.RelatedObjectDoesNotExist as e:
            instructor = None
        return instructor


    def get(self, request):
        instructor = self.get_instance()
        if instructor is not None and instructor.institution:
            return redirect(self.get_success_url())
        else:
            form = self.get_form()
            return render(
                request,
                'accounts/profile_edit.html',
                {'form': form}
            )

class InstructionsView(NotAnonymousRequiredMixin, View):
    def get(self, request):
        code = ''
        custom_code = CustomCode.objects.filter(user_id=self.request.user.id).first()
        if custom_code:
            code = custom_code.code
        return render(request, 'accounts/instruction.html', {'code': code})


class ResendEmailView(NotAnonymousRequiredMixin, View):
    def post(self, request):
        code = request.POST.get('code')
        custom_code = CustomCode.objects.filter(code=code, user_id=request.user.id).first()
        if not code or not custom_code:
            return render(
                request,
                'ctms/error.html',
                {'message': 'Not valid request'}
            )

        NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'
        path = reverse('{}:complete'.format(NAMESPACE), kwargs={'backend': 'email'}) + "?verification_code={}".format(custom_code.code)
        url= "{}://{}".format(request.scheme, request.get_host())
        uri = build_absolute_uri(url, path)

        send_mail(
            'Validate your account',
            'Validate your account {}'.format(uri),
            settings.EMAIL_FROM,
            [custom_code.email],
            fail_silently=False
        )
        return render(
            request,
            'psa/validation_sent.html',
            {'email': custom_code.email}
        )

