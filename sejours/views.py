from django.shortcuts import render_to_response, get_object_or_404
from sejours.models import *
from django.template import RequestContext
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

@login_required
def saison(request, saison_id):
	o = get_object_or_404(Saison, pk=saison_id)
	convoyages = Convoyage.objects.filter(saison_id = saison_id)
	return render_to_response('saison.html',
	{'lasaison': o, 'convoyages': convoyages, 'lessaisons': lessaisons()},
			context_instance=RequestContext(request)
		)

@login_required
def convoyage(request, user_id, convoyage_id):
	o = get_object_or_404(Convoyage, pk=convoyage_id)
	return render_to_response('convoyage.html',
		{'convoyage': o, 'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

@login_required
def sejour(request, user_id, sejour_id):
	o = get_object_or_404(Sejour, pk=sejour_id)
	return render_to_response('sejour.html',
		{'sejour': o, 'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

@login_required
def index(request):
	return render_to_response('index.html',
		{'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

@login_required
def mafiche(request, user_id):
	u = get_object_or_404(User, pk=user_id)
	userform = userForm()
	personneform = personneForm()
	animateurform = animateurForm()
	url_action = '/'+ user_id + '/mafiche'
	
	return render_to_response('mafiche.html',
		{'u': u, 'lessaisons': lessaisons(), 'userform':userform, 'personneform':personneform, 'animateurform':animateurform, 'action': url_action },
		context_instance=RequestContext(request)
	)

# Fonctions utilitaires

def lessaisons(): # TODO: devrait ne renvoyer que les saisons en cours
	s = Saison.objects.all()
	return s

# Les formulaires
class userForm(ModelForm):
	class Meta:
		model = User
class personneForm(ModelForm):
	class Meta:
		model = Personne
class animateurForm(ModelForm):
	class Meta:
		model = Animateur
		
