# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from apps.product.models import Product


def cur_date():
    return datetime.datetime.now().replace(microsecond=0)


class Cart(models.Model):
    status_arr = [(1, "Новый заказ"), (2, "Выполняется"), (3, "Выполнен"), (4, "Отмена")]
    address = models.TextField(verbose_name='Адрес доставки')
    phone = models.CharField(max_length=128, verbose_name='Телефон')
    email = models.CharField(max_length=128, verbose_name='E-mail')
    name = models.CharField(max_length=128, verbose_name='ФИО')
    user = models.ForeignKey(User, null = True, blank = True, verbose_name='Пользователь')
    status = models.IntegerField(max_length=10, default=1,choices=status_arr, verbose_name='Статус Заказа')
    tm_created = models.DateTimeField(null = True, default = cur_date, verbose_name = u'Дата заказа')


class CartProducts(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар')
    cart = models.ForeignKey(Cart, verbose_name='id корзины')
    size = models.CharField(max_length=128, verbose_name='Размер')
    color = models.CharField(null = True, blank = True, max_length=128, verbose_name='Цвет')
    price = models.DecimalField(null = True, blank = True, max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.IntegerField(default=1, verbose_name='Кол-во')
