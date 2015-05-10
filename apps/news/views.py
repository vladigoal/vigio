# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from models import News


class NewsView(TemplateView):
    template_name = "news.html"

    def get_context_data(self, **kwargs):

        news = ""
        slug = None
        path_bits = self.request.path.split("/")
        try:
            slug = path_bits[2]
        except:
            slug = None

        if slug:
            news =  News.objects.filter(slug=slug)
        else:
            news =  News.objects.all()

        context = super(NewsView, self).get_context_data(**kwargs)
        context['news'] = news
        context['slug'] = slug
        return context
