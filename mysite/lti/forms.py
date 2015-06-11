from django import forms

from lti.models import CourseRef


CHOICES = ((0, 'new'), (1, 'saved'))


class ChoiceCourseForm(forms.Form):
    """Form for choising source of new Course"""
    def __init__(self, user, *args, **kwargs):
        super(ChoiceCourseForm, self).__init__(*args, **kwargs)
        self.fields['source'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=[(i.id, str(i)) for i in CourseRef.objects.filter(instructors__in=[user])],
            label='Previous revisions', required=False
        )
