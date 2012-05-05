from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from sejours.models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^$', 'index'),
	url(r'^convoyage/$',
		ListView.as_view(
			queryset=Convoyage.objects.all()[:5],
			template_name='sejours/tpl/convoyages.html')),
	url(r'^convoyage/(?P<pk>\d+)\.html$',
		DetailView.as_view(
			model=Convoyage,
			template_name='sejours/tpl/convoyage.html')),
	url(r'^sejour/(?P<pk>\d+)\.html$',
		DetailView.as_view(
			model=Sejour,
			template_name='tpl/sejour.html')),
	url(r'^animateur/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Animateur,
			template_name='tpl/animateur.html')),
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

