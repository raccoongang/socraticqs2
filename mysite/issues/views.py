from rest_framework import viewsets

from issues.models import Issue, IssueLabel, IssueComment
from issues.serializers import IssueSerializer, IssueLabelSerializer, IssueCommentSerializer


class IssuesView(viewsets.ModelViewSet):
    """
    Dummy ViewSet for testing frontend.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = super(IssuesView, self).get_queryset()
        if 'unit_lesson' in self.request.GET:
            queryset = queryset.filter(unit_lesson_id=self.request.GET['unit_lesson'])
        return queryset


class IssueLabelsView(viewsets.ModelViewSet):
    """
    Simple ViewsSet for retrive issueLabels
    """
    queryset = IssueLabel.objects.all()
    serializer_class = IssueLabelSerializer


class IssueCommentsView(viewsets.ModelViewSet):
    """
    Simple ViewsSet for retrive issueComment
    """
    queryset = IssueComment.objects.all()
    serializer_class = IssueCommentSerializer

    def get_queryset(self):
        queryset = super(IssueCommentsView, self).get_queryset()
        if 'issue_id' in self.request.GET:
            queryset = queryset.filter(issue_id=self.request.GET['issue_id'])
        return queryset