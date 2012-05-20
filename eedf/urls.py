from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from sejours.models import *
from django.contrib import admin
from django.contrib.auth.forms import PasswordResetForm
admin.autodiscover()

urlpatterns = patterns('sejours.views',
	url(r'^$', 'index'),
	url(r'^(?P<user_id>\d+)/mafiche$','mafiche'),
	url(r'^saison/(?P<saison_id>\d+)$','saison'),
	url(r'^(?P<user_id>\d+)/convoyage/(?P<convoyage_id>\d+)$','convoyage'),
	url(r'^(?P<user_id>\d+)/sejour/(?P<sejour_id>\d+)$','sejour'),
	)

urlpatterns += patterns('',
	(r'^accounts/login/$',
		'django.contrib.auth.views.login',
		{'template_name': 'login.html'}
	),
	(r'^accounts/reset/$',
		'django.contrib.auth.views.password_reset',
		{'template_name': 'reset.html','email_template_name': 'reset_email.html',}
	),
	(r'^accounts/reset_done/$',
		'django.contrib.auth.views.password_reset_done',
		{'template_name': 'reset_done.html',}
	),
	(r'^accounts/reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
		'django.contrib.auth.views.password_reset_confirm',
		{'template_name': 'reset_confirm.html'}
	),
	(r'^accounts/reset_complete/$',
		'django.contrib.auth.views.password_reset_complete',
		{'template_name': 'reset_complete.html'}
	),
	url(r'^admin/', include(admin.site.urls)),
)
