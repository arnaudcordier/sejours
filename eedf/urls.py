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
	url(r'^(?P<user_id>\d+)/convoyage/(?P<convoyage_id>\d+)$','convoyage'),
	url(r'^(?P<user_id>\d+)/sejour/(?P<sejour_id>\d+)$','sejour'),
	)

urlpatterns += patterns('',
	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^admin/', include(admin.site.urls)),
)

