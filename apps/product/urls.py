from django.conf.urls import patterns, include, url
from views import CatalogView, ProductView


urlpatterns = patterns('',
    # (r'^size/', AdminFilterSize.as_view()),
    url(r'^product/', ProductView.as_view()),
    (r'', CatalogView.as_view()),
)