from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


class Dateformat(models.Model):
    dateformat = models.CharField(max_length=50, null=True)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_project", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True)
    dateformat = models.ForeignKey(Dateformat, on_delete=models.SET_NULL, related_name="dateformat_project", null=True)
    inactive = models.BooleanField(default=False)


class Role(models.Model):
    role = models.CharField(max_length=50, null=True)


class Members(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_members")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name="role_members", null=True)


class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_tag")
    name = models.CharField(max_length=50, null=True)


class Item(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="project_item", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_item", null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, related_name="tag_item", null=True)
    description = models.CharField(max_length=1000, null=True)
    dateopened = models.DateTimeField(auto_now_add=True)
    dateclosed = models.DateTimeField(auto_now_add=False)
    assignedto = models.CharField(max_length=100, null=True)


class Archive(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, related_name="item_archive", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_archive", null=True)
    upload = models.FileField(upload_to='uploads/', null=True)


class Duedate(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_duedate")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_duedate", null=True)
    duedate = models.DateTimeField(auto_now_add=False)


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_comment")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_comment", null=True)
    comment = models.CharField(max_length=1000, null=True)


class Notification(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_notification")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_notification")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_notification")
    timestamp = models.DateTimeField(auto_now_add=True)


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_alert")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notification_alert")
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

