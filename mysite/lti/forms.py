from django import forms

from lti.models import CourseRef


CHOICES = ((0, 'new'), (1, 'saved'))


class ChoiceCourseForm(forms.Form):
    """Form for choising source of new Course"""
    def __init__(self, user, *args, **kwargs):
        super(ChoiceCourseForm, self).__init__(*args, **kwargs)
        self.fields['source'] = forms.ChoiceField(
            choices=[(i.id, str(i)) for i in CourseRef.objects.filter(instructors__in=[user])],
            label='Previous revisions'
        )

    choice = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'id': 'choice'}),
        choices=CHOICES, initial=0, label='Choice creation metod'
    )
