from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import render

from .models import Profile


# <!-- With using try / except -->

def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        try:
            if not username or not password or not email:
                raise ValidationError('All fields are required!')

            if User.objects.filter(username=username).exists():
                raise ValidationError('Username already exists!')

            if User.objects.filter(email=email).exists():
                raise ValidationError('Email already exists!')

            if len(password) < 8:
                raise ValidationError('The password cannot be less than 8 characters')

            if password != request.POST['confirm_password']:
                raise ValidationError('Password do not match!')

            group_user = Group.objects.get(name='customers')

            user = User.objects.create_user(username=username, password=password, email=email)

            user.groups.add(group_user)
            user.save()

            return HttpResponseRedirect(reverse('login'))

        except ValidationError as e:
            error = str(e)
            return render(request, 'userAdmin/register.html', {'error': error})

    else:
        return render(request, 'userAdmin/register.html')


# def register_user(request: HttpRequest):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']
#         # first_name = request.POST['first_name']
#         # last_name = request.POST['last_name']
#         # about = request.POST['about']
#
#         group_user = Group.objects.get(name='customers')
#
#         user = User.objects.create_user(username=username, password=password, email=email)
#         # user.first_name = first_name
#         # user.last_name = last_name
#         user.groups.add(group_user)
#         user.save()
#
#         # profile = Profile(user=user, about=about)
#         # profile.save()
#
#         return HttpResponseRedirect(reverse('get-products'))
#     else:
#         return render(request, 'userAdmin/register.html')



def login_user(request: HttpRequest) -> HttpResponse:
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
