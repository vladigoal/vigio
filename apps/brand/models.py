# -*- coding: utf-8 -*-

from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')
    desc = models.TextField(null = True, blank = True, verbose_name = u'Описание')
    image = models.ImageField(upload_to = 'images/brand', verbose_name = u'Изображение')

    class Meta:
        verbose_name = u'Бренды'
        verbose_name_plural = u'Бренд'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Brand, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.name
