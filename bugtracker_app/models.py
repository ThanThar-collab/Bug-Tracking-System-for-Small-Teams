from django.db import models
from django.contrib.auth.models import User


class Bug(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Validated', 'Validated'),
        ('Invalid', 'Invalid'),
        ('Duplicate', 'Duplicate'),
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    VALIDITY_CHOICES = [
        ('Pending', 'Pending'),
        ('Valid', 'Valid'),
        ('Invalid', 'Invalid'),
        ('Duplicate', 'Duplicate'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='bug_attachments/', null=True, blank=True) #add new field
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reported_bugs')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validity = models.CharField(max_length=20, choices=VALIDITY_CHOICES, default='Pending')
    admin_comments = models.TextField(blank=True, null=True)
    desired_date = models.DateField(null=True, blank=True) 
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Medium')

    def __str__(self):
        return f"{self.title} ({self.status})"


class BugComment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.bug}"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        (1, 'Developer'),
        (2, 'Tester'),
        (3, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
