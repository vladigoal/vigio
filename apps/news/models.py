# -*- coding: utf-8 -*-
from django.db import models
from sorl.thumbnail import ImageField
import datetime
from unidecode import unidecode
from django.template.defaultfilters import slugify
from utils.slug import unique_slugify

def cur_date():
    return datetime.datetime.now().replace(microsecond=0)


class News(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Заголовок')
    description = models.TextField(verbose_name = u'Описание')
    date = models.DateField(null = True, default = cur_date, verbose_name = u'Дата')
    image = models.ImageField(upload_to = 'images/news', verbose_name = u'Изображение')
    slug = models.CharField(null=True, blank=True, max_length=50,
                            verbose_name=u'Url (автозаполнение)')
    meta_title = models.CharField(max_length=150, blank=True,
                             verbose_name=u'SEO Title')
    meta_keywords = models.CharField(max_length=150, blank=True,
                                     verbose_name=u'SEO Keywords')
    meta_desc = models.CharField(max_length=150, blank=True,
                                 verbose_name=u'SEO Description')

    class Meta:
        verbose_name = u'Новости'
        verbose_name_plural = u'Новость'

    def save(self, **kwargs):
        self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
        unique_slugify(self, self.slug)
        super(News, self).save()

    def __unicode__(self):
        return self.name
