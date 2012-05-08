from django.shortcuts import render_to_response, get_object_or_404
from sejours.models import *
from django.template import RequestContext

def saison(request, saison_id):
	o = get_object_or_404(Saison, pk=saison_id)
	convoyages = Convoyage.objects.filter(saison_id = saison_id)
	return render_to_response('saison.html',
	{'lasaison': o, 'convoyages': convoyages, 'lessaisons': lessaisons()},
			context_instance=RequestContext(request)
		)

def convoyage(request, user_id, convoyage_id):
	o = get_object_or_404(Convoyage, pk=convoyage_id)
	return render_to_response('convoyage.html',
		{'convoyage': o, 'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

def index(request):
	return render_to_response('index.html',
		{'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

def mafiche(request, user_id):
	u = get_object_or_404(User, pk=user_id)
	return render_to_response('mafiche.html',
		{'u': u, 'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

# Fonctions utilitaires

def lessaisons(): # TODO: devrait ne renvoyer que les saisons en cours
	s = Saison.objects.all()
	return s