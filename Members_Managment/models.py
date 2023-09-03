from django.db import models

# Create your models here.

class Member(models.Model):

    tag = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=40, default="")
    clan = models.CharField(max_length=25, default="")
    role = models.CharField(max_length=10, default="")
    cel = models.CharField(max_length=20, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    current_member = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)