from django.contrib import admin
from .models import Project, Bug, BugComment, UserProfile

admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(BugComment)
admin.site.register(UserProfile)