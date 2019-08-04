from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_account(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_money = models.IntegerField()
    def __str__(self):
        return self.name.username


class User_history(models.Model):
    history_title = models.CharField(max_length=100)
    user_history_money = models.IntegerField()
    user_ac = models.ForeignKey(User_account, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.history_title


class Group_account(models.Model):
    title = models.CharField(max_length=100)
    group_money = models.IntegerField()
    members = models.ManyToManyField(User_account)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    group_ac = models.ForeignKey(Group_account, on_delete= models.CASCADE, null =True)
    title = models.CharField(max_length=100)
    date = models.DateTimeField('date published')
    penalty = models.IntegerField()
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title
