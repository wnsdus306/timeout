from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    auth.logout(request)
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')