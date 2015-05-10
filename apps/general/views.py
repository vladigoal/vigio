# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from .models import MainPage
from apps.news.models import News
from django.http import HttpResponse
from django.utils import simplejson as json
from django.core.mail import send_mail

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['links'] = MainPage.objects.all()
        context['news'] = News.objects.all()[:5]
        return context


class ContactsView(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        msg = u'Сообщение от %s \n'%self.request.POST.get('fio')
        msg = msg + u'Email: %s \n'%self.request.POST['email']
        msg = msg + u'Сообщение: %s \n'%self.request.POST['message']
        send_mail('Vigio - Контакты', msg, 'office@vigio.com.ua', ['vladigoal@gmail.com', 'vigio.ukrinfo@gmail.com'], fail_silently=False)
        return HttpResponse(json.dumps({'status': 'ok'}), mimetype="application/json" )