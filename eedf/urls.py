from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from sejours.models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sejours.views',
	url(r'^$', 'index'),
	url(r'^(?P<user_id>\d+)/mafiche$','mafiche'),
	url(r'^saison/(?P<saison_id>\d+)$','saison'),
	url(r'^convoyage/(?P<convoyage_id>\d+)$','convoyage'),
)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'eedf.views.home', name='home'),
    # url(r'^eedf/', include('eedf.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

