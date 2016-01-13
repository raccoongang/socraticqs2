from django.contrib import admin
from issues.models import Issue, IssueLabel, IssueComment


admin.site.register(Issue)
admin.site.register(IssueLabel)
admin.site.register(IssueComment)
