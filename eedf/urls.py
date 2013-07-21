from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from sejours.models import *
from django.contrib import admin
from django.contrib.auth.forms import PasswordResetForm
from userena import views as userena_views
from userena import settings as userena_settings
admin.autodiscover()

urlpatterns = patterns('sejours.views',
	url(r'^$', 'index'),
	url(r'^mafiche$','mafiche', name='mafiche'),
	url(r'^saison/(?P<saison_id>\d+)$','saison', name='saison'),
	url(r'^convoyage/(?P<convoyage_id>\d+)$','convoyage', name='convoyage'),
	url(r'^sejour/(?P<sejour_id>\d+)$','sejour', name='sejour'),
	url(r'^structure/(?P<structure_id>\d+)$','structure', name='structure'),
	url(r'^structures$','structures', name='structures'),
	url(r'^(?P<saison_id>\d+)/sejours$','sejours', name='sejours'),
	url(r'^animateur/(?P<animateur_id>\d+)$','animateur', name='animateur'),
	url(r'^rechercheanimateur/(?P<recherche>.+)$','rechercheanimateur', name='rechercheanimateur'),
	)

urlpatterns += patterns('',
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
	url(r'^accounts/signout/$',
		userena_views.signout,{'next_page':'/','template_name':'userena/signout.html'},
		name='userena_signout'
	),
	url(r'^accounts/signup/$',
		userena_views.signup,{'template_name':'signup.html'},
		name='userena_signup'
	),
	url(r'^accounts/(?P<username>[\.\w]+)/signup/complete/$',
		userena_views.direct_to_user_template,
		{'template_name': 'signup_complete.html',
		'extra_context': {'userena_activation_required': userena_settings.USERENA_ACTIVATION_REQUIRED,
		'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS}},
		name='userena_signup_complete'
	),
	url(r'^accounts/(?P<username>[\.\w]+)/activate/(?P<activation_key>\w+)/$',
		userena_views.activate,{'success_url':'/','template_name':'activate_fail.html',},
		name='userena_activate'
	),
	url(r'^accounts/signin/$',
		userena_views.signin,{'template_name':'login.html'},
		name='userena_signin'
	),
	url(r'^admin/', include(admin.site.urls)),
)
