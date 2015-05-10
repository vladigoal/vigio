# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.utils import simplejson as json

class AdminFilterSize(View):

    def post(self, request, *args, **kwargs):
        print 'get get'
        return HttpResponse('ok', mimetype="application/json" )


class AdminFilter(View):

    def get(self, request, *args, **kwargs):

        get_dict = dict(request.GET.iterlists())
        key, value =  get_dict.popitem()
        path_bits = request.path.split('/')

        try:
            return_params =  path_bits[(len(path_bits) - 2)]
            filter_dict = {'%s__in'%key: request.GET[key]}
            print filter_dict

            # print Collection.objects.filter('gender__in'=request.GET['collection'])
            data = json.dumps(
                {
                    return_params: [{'id': item.id, 'name': item.name } for item in
                                 Category.objects.filter(**filter_dict)
                    ],
                }
            )
        except:
            data = {}

        print data

        return HttpResponse(data, mimetype="application/json" )
