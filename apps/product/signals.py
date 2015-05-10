# -*- coding: utf-8 -*-

from registration.signals import user_registered, user_activated
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth


def user_created(sender, user, request, **kwargs):
    form = UserCreationForm(request.POST)
    # profile = User(user=user, country_id=int(form.data['country']),
    #                fname=form.data['fname'], lname=form.data['lname'],
    #                patronymic=form.data['patronymic'],
    #                zipcode=form.data['zipcode'], city=form.data['city'],
    #                street=form.data['street'], phone=form.data['phone'])
    profile = User(form)
    profile.save()


def login_on_activation(sender, user, request, **kwargs):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)

user_activated.connect(login_on_activation)
user_registered.connect(user_created)
