# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import MainPage
from django.contrib.flatpages.models import FlatPage

class MainPageAdmin(admin.ModelAdmin):
    list_display = ['link', 'name', ]

    class Media:

        js = [
             '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
             '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class FlatPageAdmin(admin.ModelAdmin):

    class Media:

        js = [
             '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
             '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(MainPage, MainPageAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

