# -*- coding: utf-8 -*-
import urllib
from django.utils import simplejson as json
from apps.product.models import Category, Product, Collection, Lookbook

def cart(request):
    ret = []
    cookie = request.COOKIES.get('cart')

    if cookie:
        cart = json.loads(urllib.unquote(cookie).decode('utf-8'))
        ids = []
        for prod in cart:
            ids.append(prod['id'])
        prods = Product.objects.filter(id__in=ids)
        for prod in prods:
            p = prod.toCart()
            for x in cart:
                if p['id'] == x['id']:
                    p['count'] = x['count']
                    try:
                        p['color'] = x['color']
                    except:
                        p['color'] = 'Нет'
                    try:
                        p['size'] = x['size']
                    except:
                        p['size'] = 'Нет'
            ret.append(p)
    return {
        'cart_data': json.dumps(ret)
    }

def filters(request):
    menu_categories = []
    menu_ca = Category.objects.filter(level=0)
    for menu in menu_ca:
        ca_dict = {
            'cat': menu,
            'sub_cat': Category.objects.filter(level=1, parent=menu.id)
        }
        menu_categories.append(ca_dict)
    return {
        "menu_categories": menu_categories,
    }


def menu(request):
    return {
        "menu_collections": Collection.objects.filter(show=True),
        "lookbook_menu": Lookbook.objects.all()
    }