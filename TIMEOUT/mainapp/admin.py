from django.contrib import admin
from .models import User_account, User_history
# Register your models here.

admin.site.register(User_account)
admin.site.register(User_history)