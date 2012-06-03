# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from sejours.models import *
from django.template import RequestContext
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from userena import views as userena_views

import logging
logger = logging.getLogger('eedf')

@login_required
def saison(request, saison_id):
	o = get_object_or_404(Saison, pk=saison_id)
	convoyages = Convoyage.objects.filter(saison_id = saison_id)
	return render_to_response('saison.html',
	{'lasaison': o, 'convoyages': convoyages, 'lessaisons': lessaisons(), 'a': PasswordResetForm()},
			context_instance=RequestContext(request),
		)

@login_required
def convoyage(request, user_id, convoyage_id):
	o = get_object_or_404(Convoyage, pk=convoyage_id)
	if (peut_voir_animateur(user_id, request)):
		return render_to_response('convoyage.html',
			{'convoyage': o, 'lessaisons': lessaisons()},
			context_instance=RequestContext(request)
		)
	else:
		return redirect('/')

@login_required
def sejour(request, user_id, sejour_id):
	o = get_object_or_404(Sejour, pk=sejour_id)
	if (peut_voir_animateur(user_id, request)):
		return render_to_response('sejour.html',
			{'sejour': o, 'lessaisons': lessaisons()},
			context_instance=RequestContext(request)
		)
	else:
		return redirect('/')

@login_required
def index(request):
	return render_to_response('index.html',
		{'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

@login_required
def mafiche(request, user_id):
	u = get_object_or_404(User, pk=user_id)
	if (peut_voir_animateur(user_id, request)):
		userform = userForm()
		personneform = personneForm()
		animateurform = animateurForm()
		url_action = '/'+ user_id + '/mafiche'
		
		return render_to_response('mafiche.html',
			{'u': u, 'lessaisons': lessaisons(), 'userform':userform, 'personneform':personneform, 'animateurform':animateurform, 'action': url_action },
			context_instance=RequestContext(request)
		)
	else:
		return redirect('/')


# Fonctions utilitaires
def lessaisons(): # TODO: devrait ne renvoyer que les saisons en cours
	s = Saison.objects.all()
	return s

def peut_voir_animateur(user_id, request):
	req = RequestContext(request)
	user = req.get('user')
	if (int(user_id) == int(user.id)):
		return True
	else:
		logger.error('ca passe pas')
		return False

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
		
