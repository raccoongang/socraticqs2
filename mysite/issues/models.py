from django.db.models import F

from django.contrib.auth.models import User
from django.db import models

from ct.models import Course, Unit, UnitLesson, CourseUnit


LABEL_COLORS = (
    ('label-default', 'Grey'),
    ('label-primary', 'Blue'),
    ('label-success', 'Green'),
    ('label-info', 'LightBlue'),
    ('label-warning', 'Yellow'),
    ('label-danger', 'Red')
)


class IssueLabel(models.Model):
    """
    Simple realization tagging
    """
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=20, default='Grey', choices=LABEL_COLORS)
    default = models.BooleanField(default=False)

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
    affected_count = models.PositiveIntegerField(default=1, blank=True)
    auto_issue = models.BooleanField(default=False, blank=True)

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

    def incr_affected(self):
        """
        Increment affected student counter.
        """
        self.affected_count = F('affected_count') + 1
        self.save()

    def __unicode__(self):
        return "%s(%s) - %s" % (self.title, self.is_open, self.assignee)


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    parent = models.ForeignKey('IssueComment', blank=True, null=True)
    author = models.ForeignKey(User)
    text = models.TextField(blank=True)
