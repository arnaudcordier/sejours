from django.shortcuts import render_to_response, get_object_or_404
from sejours.models import *
from django.template import RequestContext

def saison(request, saison_id):
	o = get_object_or_404(Saison, pk=saison_id)
	convoyages = Convoyage.objects.filter(saison_id = saison_id)
	return render_to_response('saison.html',
			{'saison': o, 'convoyages': convoyages},
			context_instance=RequestContext(request)
		)

def convoyage(request, convoyage_id):
	o = get_object_or_404(Convoyage, pk=convoyage_id)
	return render_to_response('convoyage.html',
		{'convoyage': o},
		context_instance=RequestContext(request)
	)

def index(request):
	return render_to_response('index.html',
		context_instance=RequestContext(request)
	)
	