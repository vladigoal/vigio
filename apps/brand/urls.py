from django.conf.urls import patterns, include, url
from apps.brand.views import BrandView

urlpatterns = patterns('django.contrib.flatpages.views',
    url(r'^about/', 'flatpage', {'url': '/brand/about/'}, name='about'),
    url(r'^creators/', 'flatpage', {'url': '/brand/creators/'}, name='creators'),
    url(r'^mission/', 'flatpage', {'url': '/brand/mission/'}, name='mission'),
)

urlpatterns += patterns('',
    (r'', BrandView.as_view()),
)