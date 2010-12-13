from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from labs_example import views

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', views.index),
    (r'^features/', include('featurelabs.urls')),
)
