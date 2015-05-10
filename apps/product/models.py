# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField
from unidecode import unidecode

from django.template.defaultfilters import slugify
from utils.slug import unique_slugify
from sorl.thumbnail import ImageField
from utils.image import get_resized_thumb
from sorl.thumbnail.shortcuts import get_thumbnail


class Collection(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')
    show = models.BooleanField(default=True,
                                     verbose_name = u'Отображать на сайте')
    sort = models.IntegerField(default=0,
                                     verbose_name = u'Порядок показа')
    image = models.ImageField(upload_to = 'images/collection', verbose_name = u'Изображение')

    class Meta:
        verbose_name = u'Коллекция'
        verbose_name_plural = u'Коллекции'

    def __unicode__(self):
        return self.name


@python_2_unicode_compatible
class Category(MPTTModel):
    name = models.CharField(
        pgettext_lazy('Category field', 'name'), max_length=128)
    slug = models.SlugField(
        pgettext_lazy('Category field', 'slug'), max_length=50, null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        verbose_name=pgettext_lazy('Category field', 'parent'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:category', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        if not self.slug:
            self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
            unique_slugify(self, self.slug)
        super(Category, self).save()

    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        app_label = 'product'


class Size(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')
    category = models.ManyToManyField(Category, verbose_name = u'Доступен для категорий')

    class Meta:
        verbose_name = u'Размер'
        verbose_name_plural = u'Размеры'

    def __unicode__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')

    class Meta:
        verbose_name = u'Цвет'
        verbose_name_plural = u'Цвета'

    def __unicode__(self):
        return self.name


class Care(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')
    category = models.ManyToManyField(Category, verbose_name = u'Доступен для категории')
    image = models.ImageField(upload_to = 'images/care', null = True, blank = True, verbose_name = u'Изображение')

    class Meta:
        verbose_name = u'Уход за вещью'
        verbose_name_plural = u'Уход за вещами'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Care, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')

    class Meta:
        verbose_name = u'Статус товара'
        verbose_name_plural = u'Статус товара'

    def __unicode__(self):
        return self.name


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Заголовок')
    slug = models.SlugField(
        pgettext_lazy('Category field', 'slug'), max_length=50, null=True, blank=True)
    parent = models.ManyToManyField('self', null=True, blank=True, verbose_name='Сочетание с')
    collection = models.ForeignKey(Collection, verbose_name = u'Коллекция')
    status = models.ForeignKey(Status, verbose_name = u'Статус товара')
    category = models.ForeignKey(Category, blank = True, null=True, verbose_name = u'Категория', default=1)
    desc = models.TextField(null = True, blank = True, verbose_name = u'Описание')
    fabric = models.TextField(null = True, blank = True, verbose_name = u'Состав')
    care = models.ManyToManyField(Care, null = True, blank = True, verbose_name = u'Уход')
    size = models.ManyToManyField(Size, null = True, blank = True, verbose_name = u'Размеры')
    code = models.CharField(max_length = 50, verbose_name = u'Артикул')
    price = models.IntegerField(default = 0, verbose_name = u'Цена')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        if not self.slug:
            self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
            unique_slugify(self, self.slug)
        super(Product, self).save()

    class Meta:
        verbose_name = u'Продукция'
        verbose_name_plural = u'Продукция'

    def toCart(self):
        prod_image = ProductImage.objects.filter(product_id=self.id, catalog=True)
        try:
            color = prod_image[0].color
        except:
            color = ''

        try:
            image = prod_image[0].image
        except:
            image = ''
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'image': get_resized_thumb(image, '36x48'),
            'count': 1,
            'color': color,
            'size': self.size,
        }


class ProductImage(models.Model):
    image = models.ImageField(upload_to = 'images/products', verbose_name = u'Изображение')
    product = models.ForeignKey(Product, related_name='images')
    color = models.ForeignKey(Color, null = True, blank = True, verbose_name = u'Цвет')
    catalog = models.BooleanField(default=False,
                                     verbose_name = u'В каталоге товаров')

    class Meta:
        verbose_name = u'Картинка продукта'
        verbose_name_plural = u'Картинки продукта'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(ProductImage, self).delete(*args, **kwargs)

    def __unicode__(self):
        html = '<img width="100" src="%s" alt="">' % (self.image.url,)
        return mark_safe(html)


class Lookbook(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'Название')

    def __unicode__(self):
        return self.name


class LookbookImage(models.Model):
    lookbook = models.ForeignKey(Lookbook, related_name='Lookbook')
    image = models.ImageField(upload_to = 'images/lookbook', verbose_name = u'Изображение')
    product = models.ManyToManyField(Product, null = True, blank = True, verbose_name = u'Продукт')

    class Meta:
        verbose_name = u'Картинка Lookbook'
        verbose_name_plural = u'Картинки Lookbook'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(LookbookImage, self).delete(*args, **kwargs)

    def get_thumbnail_html(self):
        img = self.image
        img_resize_url = unicode(get_thumbnail(img, '200x150').url)
        html = '<img src="%s" alt="%s"/>'
        return html % (img_resize_url, self.image)

    get_thumbnail_html.short_description = u'Превью'
    get_thumbnail_html.allow_tags = True

    def __unicode__(self):
        html = '<img height="70" src="%s" alt="">' % (self.image.url,)
        return mark_safe(html)
