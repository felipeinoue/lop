from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    lop_username = models.CharField(max_length=50)


class Dateformat(models.Model):
    dateformat = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.id} | {self.dateformat}"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_project", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    project = models.CharField(max_length=100, null=True)
    dateformat = models.ForeignKey(Dateformat, on_delete=models.SET_NULL, related_name="dateformat_project", null=True)
    inactive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} | {self.user} | {self.timestamp} | {self.project} | {self.dateformat} | {self.inactive}"


class Role(models.Model):
    role = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.id} | {self.role}"


class Members(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_members")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name="role_members", null=True)

    def __str__(self):
        return f"{self.id} | {self.user} | {self.role}"


class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_tag")
    tag = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.id} | {self.project} | {self.tag}"


class Item(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="project_item", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_item", null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, related_name="tag_item", null=True)
    description = models.CharField(max_length=1000)
    dateopened = models.DateTimeField(auto_now_add=True)
    dateclosed = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    assignedto = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.project.project} | {self.user.username} | {self.tag.tag} | {self.description} | {self.dateopened} | {self.dateclosed} | {self.assignedto}"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_<project_id>/<filename>
    return 'project_{0}/{1}'.format(instance.item.project.id, filename)


class Archive(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, related_name="item_archive", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_archive", null=True)
    upload = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f"{self.id} | {self.item} | {self.user} | {self.upload}"


class Duedate(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_duedate")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_duedate", null=True)
    duedate = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"{self.id} | {self.item} | {self.user} | {self.duedate}"


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_comment")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_comment", null=True)
    comment = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.id} | {self.item} | {self.user} | {self.comment}"


class Notification(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_notification")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_notification")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_notification", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.project} | {self.item} | {self.user} | {self.timestamp}"


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_alert")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notification_alert")
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} | {self.user} | {self.notification} | {self.timestamp} | {self.seen}"
