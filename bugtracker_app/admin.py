from django.contrib import admin
from .models import  Bug, BugComment, UserProfile

class BugAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'validity', 'reported_by', 'assigned_to')
    list_filter = ('status', 'validity')
    search_fields = ('title', 'description', 'reported_by__username')
    actions = ['mark_as_valid', 'mark_as_invalid', 'mark_as_duplicate']

    def mark_as_valid(self, queryset):
        queryset.update(validity='Valid', status='Open')

    def mark_as_invalid(self, queryset):
        queryset.update(validity='Invalid', status='Invalid')

    def mark_as_duplicate(self, queryset):
        queryset.update(validity='Duplicate', status='Duplicate')
    
admin.site.register(Bug)
admin.site.register(BugComment)
admin.site.register(UserProfile)