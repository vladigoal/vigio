# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.utils import simplejson as json
from .models import Product, ProductImage, Color, Size, Category, \
    LookbookImage, Collection
from utils.image import get_resized_thumb
from django.core.mail import send_mail


def build_product_json(product, products_images, img_size):
    image = None
    for im in products_images:
        if im.product_id == product.id and im.catalog == True:
            image = im
    return json.dumps({
            'id': product.id,
            'name': product.name,
            'image': get_resized_thumb(image, img_size),
            'price': str(product.price),
            'count': 1
        })


class CatalogView(TemplateView):
    template_name = "catalog.html"

    def get_context_data(self, **kwargs):

        context = super(CatalogView, self).get_context_data(**kwargs)
        context['products'] = self.get_products()
        context['filter_size'] = Size.objects.all()
        return context

    def get_products(self, **kwargs):
        if self.request.GET:
            products = self.filter()
        else:
            products = Product.objects.all()[:30]
        images_ids = [p.id for p in products]
        products_images = ProductImage.objects.filter(product_id__in=images_ids)
        products_fin = []
        for p in products:
            prod_dict ={
                'product': p,
            }
            for im in products_images:
                if im.product_id == p.id:
                    if im.catalog:
                        prod_dict['img_first'] = im.image
                    else:
                        prod_dict['img_second'] = im.image
            products_fin.append(prod_dict)
        return products_fin

    def get_categories(self, parent_id):
        return [item.id for item in Category.objects.filter(parent=parent_id)]

    def filter(self, **kwargs):
        filter_dict = {}
        keys_list = ['start_price', 'fin_price', 'sizes', 'category', 'collection', 'lookbook', 'searchword']

        for key, val in self.request.GET.iteritems():
            if key in keys_list:
                if key == 'start_price':
                    filter_dict['price__gte'] = unicode.encode(val)
                elif key == 'fin_price':
                    filter_dict['price__lte'] = unicode.encode(val)
                elif key == 'sizes':
                    sizes =[int(unicode.encode(s)) for s in val.split(',')]
                    filter_dict['size__in'] = sizes
                elif key == 'category':
                    try:
                        filter_dict['category'] = val
                    except:
                        pass
                elif key == 'collection':
                    try:
                        filter_dict['collection'] = val
                    except:
                        pass
                elif key == 'lookbook':
                    prod_ids =[l.id for l in LookbookImage.objects.filter(id=val)[0].product.select_related()]
                    filter_dict['id__in'] = prod_ids
                elif key == 'searchword':
                    filter_dict['name__icontains'] = self.request.GET['searchword']
        return Product.objects.filter(**filter_dict)


class ProductView(TemplateView):
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        path = self.request.path.split('/')
        if len(path) > 3:
            slug = path[3]
        else:
            slug = None
        product = Product.objects.filter(slug=slug)
        context = super(ProductView, self).get_context_data(**kwargs)
        if product:
            product = product.get()
            context['crumbs'] = self.get_bread_crumbs(product.category, [])
            relative_products = Product.objects.filter(parent=product.id)
            context['relative_products'] = self.get_relative_products(relative_products)
            products_images = ProductImage.objects.filter(product_id=product.id)
            context['products_images'] = products_images
            products_images_ids = []
            product_colors = []
            for pi in products_images:
                if pi.color_id not in products_images_ids:
                    products_images_ids.append(pi.color_id)
                    product_colors.append(pi)
            context['product_colors'] = product_colors
            context['product'] = product


            context['product_json'] = build_product_json(product, products_images, '260')
        return context

    def get_relative_products(self, products):
        images_ids = [p.id for p in products]
        products_images = ProductImage.objects.filter(product_id__in=images_ids)
        products_fin = []
        for p in products:
            prod_dict ={
                'product': p,
            }
            for im in products_images:
                if im.product_id == p.id:
                    if im.catalog:
                        prod_dict['img_first'] = im.image
            products_fin.append(prod_dict)
        return products_fin

    def get_bread_crumbs(self, item, crumbs):
        crumbs.append(item.name)
        if item.level > 0:
            return self.get_bread_crumbs(item.parent, crumbs)
        else:
            res_str = ''
            for i in reversed(crumbs):
                if crumbs.index(i) == 0:
                    res_str += ' / <span>' + i + '</span>'
                else:
                    res_str += ' / ' + i
            return res_str

class LookbookView(TemplateView):
    template_name = "lookbook.html"

    def get_context_data(self, **kwargs):
        context = super(LookbookView, self).get_context_data(**kwargs)
        try:
            lb = LookbookImage.objects.filter(lookbook=self.request.GET['id'])
        except:
            lb = LookbookImage.objects.all()
        lookbook = []
        slice = []
        counter = 0
        for l in lb:
            if counter < 3:
                counter += 1
            else:
                lookbook.append({'slice': slice})
                slice = []
                counter = 0
            slice.append(l)
        if slice:
            lookbook.append({'slice': slice})
        context['lookbook'] = lookbook
        return context


class IndividualSewing(View):

    def post(self, request, *args, **kwargs):
        msg = u'Новый заказ на пошив от %s \n'%self.request.POST.get('fio')
        msg = msg + u'Название товара: %s \n'%self.request.POST['product_name']
        msg = msg + u'Размер: %s \n'%self.request.POST['size']
        msg = msg + u'Цвет: %s \n'%self.request.POST['color']
        msg = msg + u'Телефон: %s \n'%self.request.POST['phone']
        try:
            msg = msg + u'Email: %s \n'%self.request.POST['email']
        except:
            pass
        send_mail('Vigio - Индивидульный пошив', msg, 'office@vigio.com.ua', ['vladigoal@gmail.com', 'vigio.ukrinfo@gmail.com'], fail_silently=False)
        return HttpResponse(json.dumps({'status': 'ok'}), mimetype="application/json" )
