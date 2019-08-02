from django.contrib import admin
from .models import User_account, User_history, Schedule, Group_account
# Register your models here.

admin.site.register(User_account)
admin.site.register(User_history)
admin.site.register(Schedule)
admin.site.register(Group_account)