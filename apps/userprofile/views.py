# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, check_password
from django.contrib.auth.models import User
from .models import ShopUser
import slugify


class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):

        email = request.POST['email2']
        password = request.POST['pass']

        try:
            user = User.objects.get(email=email)
        except:
            user = None

        if user :
            if user.check_password(password):
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponse( json.dumps({'status': 'ok', 'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'phone': user.shopuser.phone
                }}), mimetype="application/json" )
            else:
                return HttpResponse( json.dumps({'status': 'fail'}), mimetype="application/json" )
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), mimetype="application/json" )

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context


class Logout(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class RegistrationView(TemplateView):
    template_name = "registration.html"

    def post(self, request, *args, **kwargs):

        email = request.POST['email']
        password = request.POST['pass']
        phone = request.POST['phone']
        fio = request.POST['fio']

        split_fio = fio.split(' ')
        last_name = split_fio[0]
        first_name = ''
        if len(split_fio) > 1:
            first_name = split_fio[1]
            if len(split_fio) > 2:
                first_name += " " + split_fio[2]

        user = User(email=email, username=slugify.slugify_ru(fio), last_name=last_name, first_name=first_name)
        user.set_password(password)
        user.save()
        shop_user = ShopUser(phone=phone, user=user)
        shop_user.save()
        if user :
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponse(json.dumps({'status': 'ok'}), mimetype="application/json" )
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), mimetype="application/json" )

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        return context
