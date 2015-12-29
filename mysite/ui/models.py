from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ct.models import Course, Unit, Concept, UnitLesson

ISSUE_STATUS = (('warning', 'warning'),
                ('propose', 'propose'),
                ('enhance', 'enhance'),
                ('off-target', 'off-target'),
                ('bug', 'bug'),
                ('diagnose', 'diagnose'),
                ('resolve', 'resolve'))


class IssueTag(models.Model):
    """
    Simple realization tagging
    """
    title = models.CharField(max_length=120)

    def __unicode__(self):
        return self.title


class Issue(models.Model):
    """
    Model provide issue functional aka github issue
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=120, choices=ISSUE_STATUS)
    author = models.ForeignKey(User, related_name='author')
    assignee = models.ForeignKey(User, related_name='assignee')
    tags = models.ManyToManyField(to=IssueTag, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    course = models.ForeignKey(Course, blank=True, null=True)
    unit = models.ForeignKey(Unit, blank=True, null=True)
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
        return "%s(%s) - %s" % (self.title, self.status, self.assignee)
