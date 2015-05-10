from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from filebrowser.sites import site
from apps.general.views import IndexView, ContactsView
from apps.product import admin_urls
from apps.product import urls as shop_urls
from apps.brand import urls as brand_urls
from apps.cart.views import CartView, NewOrder
from apps.userprofile.views import LoginView, RegistrationView, Logout
from apps.product.views import LookbookView, IndividualSewing
from apps.news.views import NewsView


urlpatterns = patterns('',
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
    # (r'^admin', include(admin.site.urls)),
    # url(r'^admin_tools/', include('admin_tools.urls')),
    # (r'^admin/filebrowser/', include(site.urls)),
    (r'^$', IndexView.as_view()),
    (r'^admin-filter/', include(admin_urls)),
    (r'^shop/', include(shop_urls)),
    (r'^lookbook/', LookbookView.as_view()),
    (r'cart/', CartView.as_view()),
    (r'login/', LoginView.as_view()),
    (r'logout/', Logout.as_view()),
    (r'registration/', RegistrationView.as_view()),
    (r'^new_order/', NewOrder.as_view()),
    (r'^brand/', include(brand_urls)),
    (r'^news/', NewsView.as_view()),
    (r'^individual-sewing/', IndividualSewing.as_view()),
    (r'^contacts/', ContactsView.as_view()),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^reviews/$', 'flatpage', {'url': '/reviews/'}, name='reviews'),
    url(r'^info/$', 'flatpage', {'url': '/info/'}, name='info'),
    url(r'^delivery/$', 'flatpage', {'url': '/delivery/'}, name='delivery'),
    url(r'^payment/$', 'flatpage', {'url': '/payment/'}, name='payment'),
    url(r'^partners/$', 'flatpage', {'url': '/partners/'}, name='partners'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
