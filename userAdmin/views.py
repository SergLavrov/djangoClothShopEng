from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .models import Profile


def register_user(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        about = request.POST['about']

        group_user = Group.objects.get(name='customers')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.groups.add(group_user)
        user.save()

        profile = Profile(user=user, about=about)
        profile.save()

        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'userAdmin/register.html')



def login_user(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('get-products'))
        else:
            return render(request, 'userAdmin/login.html')
    else:
        return render(request, 'userAdmin/login.html')



def logout_user(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse('get-products'))
