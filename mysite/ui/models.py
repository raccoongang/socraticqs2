from django.contrib.auth.models import User
from django.db import models
from ct.models import Course, Unit, UnitLesson, CourseUnit

ISSUE_STATUS = (('warning', 'warning'),
                ('propose', 'propose'),
                ('enhance', 'enhance'),
                ('off-target', 'off-target'),
                ('bug', 'bug'),
                ('diagnose', 'diagnose'),
                ('resolve', 'resolve'))


class IssueLabel(models.Model):
    """
    Simple realization tagging
    """
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=6, default='ffffff')

    def __unicode__(self):
        return self.title


class Issue(models.Model):
    """
    Model provide issue functional aka github issue
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_open = models.BooleanField(default=True)
    author = models.ForeignKey(User, related_name='author')
    assignee = models.ForeignKey(User, related_name='assignee', blank=True, null=True)
    labels = models.ManyToManyField(to=IssueLabel, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    unit = models.ForeignKey(CourseUnit, blank=True, null=True)
    unit_lesson = models.ForeignKey(UnitLesson, blank=True, null=True)

    @property
    def related(self):
        return self.unit_lesson or self.unit or self.course

    @related.setter
    def related(self, obj):
        self.course = None
        self.unit = None
        self.unit_lesson = None
        if type(obj) == Course:
            self.course = obj
        elif type(obj) == Unit:
            self.unit_lesson = obj
        elif type(obj) == UnitLesson:
            self.unit_lesson = obj

    def __unicode__(self):
        return "%s(%s) - %s" % (self.title, self.is_open, self.assignee)
