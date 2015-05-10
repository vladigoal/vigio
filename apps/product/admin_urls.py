from django.conf.urls import patterns, include, url
from admin_views import AdminFilterSize, AdminFilter

urlpatterns = patterns('',
    # (r'^size/', AdminFilterSize.as_view()),
    (r'^', AdminFilter.as_view()),

)