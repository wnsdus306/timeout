from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_history(models.Model):
    history_title = models.CharField(max_length=100)
    user_history_money = models.IntegerField()

    def __str__(self):
        return self.history_title

class User_account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_money = models.IntegerField()
    history = models.ForeignKey(User_history, on_delete=models.CASCADE, null = True)
    
    def __str__(self):
        return self.user.username

