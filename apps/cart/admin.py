# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import CartProducts, Cart


class CartProductsInline(admin.StackedInline):
    model = CartProducts
    fieldsets = (
        (None, {
            'fields': ('cart', ('product', 'price', 'count', 'size', 'color'))
        }),
    )
    verbose_name_plural = 'Товары'
    verbose_name = 'Продукт'
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = (CartProductsInline, )
    readonly_fields = ('total', 'total_price')
    list_filter = ('status', 'tm_created')
    list_display = ('name', 'phone', 'email', 'address', 'status', 'tm_created', 'total', 'total_price')

    def total(self, item):
        count = 0
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            count = count+prod.count
        return count

    total.short_description = u'Кол-во'

    def total_price(self, item):
        price = 0
        prods = CartProducts.objects.filter(cart=item.id)
        for prod in prods:
            price = price+(prod.price * prod.count)
        return price
    total_price.short_description = u'На сумму'

admin.site.register(Cart, CartAdmin)
# admin.site.register(CartProducts)
