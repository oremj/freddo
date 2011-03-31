from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url('update/(\w+)/', views.update_preview, name='updater.update_preview'),
)
