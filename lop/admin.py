from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Dateformat)
admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Member)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Archive)
admin.site.register(Duedate)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Alert)