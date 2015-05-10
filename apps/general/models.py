# -*- coding: utf-8 -*-
from django.db import models

class MainPage(models.Model):
    name = models.CharField(null = True, blank = True, max_length = 100, verbose_name = u'Заголовок')
    link = models.CharField(max_length = 100, verbose_name = u'Ссылка')
    image = models.ImageField(upload_to = 'images/mainpage', verbose_name = u'Изображение')
    desc = models.TextField(null = True, blank = True, verbose_name = u'Описание')

    class Meta:
        verbose_name = u'Главная листалка'
        verbose_name_plural = u'Главная листалки'

    def __unicode__(self):
        return self.name
