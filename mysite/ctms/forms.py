from django import forms
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from ct.models import Course, CourseUnit, Unit, Lesson, UnitLesson
from ctms.models import SharedCourse, Invite
from django.contrib.auth.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'addedBy')
        widgets = {
            'addedBy': forms.HiddenInput
        }


class CreateUnitForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title',)


class EditUnitForm(forms.ModelForm):
    KIND_CHOICES = (
        (Lesson.EXPLANATION, 'long explanation'),
        (Lesson.ORCT_QUESTION, 'Open Response Concept Test question'),
    )
    unit_type = forms.ChoiceField(choices=KIND_CHOICES)

    class Meta:
        model = Lesson
        fields = ('text', 'unit_type')

    def save(self, commit=True):
        self.instance.kind = self.cleaned_data['unit_type']
        return super(EditUnitForm, self).save(commit)


class CreateCourseletForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('title',)

# class CreateSharedCourseForm(forms.ModelForm):
#     def __init__(self, user=None, *args, **kwargs):
#         self.user = user
#         super(CreateSharedCourseForm, self).__init__(*args, **kwargs)
#
#         self.fields['to_user'] = forms.ModelChoiceField(
#             queryset=User.objects.all().exclude(id=user.id)
#         )
#         self.fields['course'] = forms.ModelChoiceField(
#             required=False,
#             queryset=user.course_set.all(),
#         )
#
#     def to_user_clean(self):
#         return User.objects.filter(id=self.cleaned_data['to_user']).first()
#
#     class Meta:
#         model = SharedCourse
#         fields = ('to_user', 'course')


class InviteForm(forms.ModelForm):
    def __init__(self, course=None, instructor=None, *args, **kwargs):
        self.course = course
        self.instructor = instructor
        super(InviteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Invite
        fields = ('email', 'type', 'course')
        widgets = {
            'type': forms.HiddenInput,
            'course': forms.HiddenInput,

        }

    def save(self, commit=True):
        invite = Invite.create_new(
            commit=False,
            instructor=self.instructor,
            course=self.course,
            email=self.cleaned_data['email'],
            invite_type=self.cleaned_data['type'],
        )
        self.instance = invite
        return super(InviteForm, self).save(commit=commit)



