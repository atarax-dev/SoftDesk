from django.contrib import admin

from softapp.models import Project, Contributor, Issue, Comment
from user.models import User

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
