# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.utils import simplejson as json
import urllib
from apps.product.models import Product, ProductImage, Color
from .models import Cart, CartProducts
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail


class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated and not self.request.user.is_anonymous():
            try:
                phone = self.request.user.shopuser.phone
            except:
                phone = ''
            context['user_data'] = json.dumps({
                'name': self.request.user.last_name + " " + self.request.user.first_name,
                'email': self.request.user.email,
                'phone': phone
            })
        return context


class NewOrder(View):

    def post(self, request, *args, **kwargs):
        user = None
        if 'user_id' in self.request.POST:
            user = User.objects.get(id=int(self.request.POST['user_id']))

        new_order = Cart(
            address = self.request.POST['adress'],
            phone = self.request.POST['phone'],
            email = self.request.POST['email'],
            user = user,
            name = self.request.POST['fio']
        )
        new_order.save()

        sum = 0
        prod = ''
        for p in self.request.POST['prod'].rsplit(','):
            if len(p):
                t = p.rsplit(':')
                product = Product.objects.filter(id=int(t[0]))
                try:
                    col = Color.objects.filter(name=t[3])
                    prod_img = ProductImage.objects.filter(product=int(product[0].id), color=int(col[0].id))
                    color_link = 'http://vigio.com.ua' + prod_img[0].image.url
                except:
                    color_link = ''
                if product:
                    add_prod = CartProducts(
                        product = product[0],
                        cart = new_order,
                        price = product[0].price,
                        size = t[2],
                        color = t[3],
                        count = int(t[1])
                    )
                    prod = prod + u'%s: %s грн. x %s шт - %s грн., цвет(%s) - %s, размер - %s, артикул - %s \n'%(product[0].name, product[0].price, t[1], (product[0].price *  int(t[1])), color_link, t[3], t[2], product[0].code)
                    sum = sum + (product[0].price *  int(t[1]))
                    add_prod.save()

        # msg = u'Здравствуйте! \n'
        # msg = msg + u'В магазине "Vigio" Вы заказали \n'
        # msg = msg + prod + '\n'
        # msg = msg + u'На сумму: %s грн \n \n'%sum
        # msg = msg + u'Для подтверждения заказа наш менеджер свяжется с Вами в ближайшее время! \n'
        # msg = msg + u'До новых встреч в нашем магазине!'

        # send_mail('Vigio', msg, 'office@vigio.com.ua', [self.request.POST['email']], fail_silently=False)

        msg = u'Новый заказ №%s, от %s \n'%(new_order.id, self.request.POST.get('fio'))
        msg = msg + u'Телефон: %s \n'%self.request.POST['phone']
        msg = msg + u'Email: %s \n'%self.request.POST['email']
        msg = msg + u'Адрес доставки: %s \n'%self.request.POST['adress']
        msg = msg + prod + '\n'
        msg = msg + u'На сумму: %s грн. \n \n'%sum
        send_mail('Vigio - Новый заказ', msg, 'office@vigio.com.ua', ['vladigoal@gmail.com', 'vigio.ukrinfo@gmail.com'], fail_silently=False)

        return HttpResponse(
            json.dumps({'res': 'ok'}),
            mimetype="application/json" )
