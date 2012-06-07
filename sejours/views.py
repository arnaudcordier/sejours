# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from sejours.models import *
from sejours.forms import *
from django.template import RequestContext
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
		# Si c'est un directeur on montre le formulaire de création d'un animateur
		form_create_animateur = ''
		directeur = SejourAnimateur.objects.filter(sejour_id=sejour_id, animateur__personne__user__id=user_id)
		if (len(directeur)):
			role = directeur[0].role
			if (role == 'D'):
				form_create_animateur = createAnimateurForm(sejour_id)
				if request.method == 'POST':
					form_create_animateur = createAnimateurForm(sejour_id, request.POST)
					if form_create_animateur.is_valid():
						user = form_create_animateur.save(request)
						return redirect('/'+ user_id + '/sejour/' + sejour_id)

		return render_to_response('sejour.html',
			{'sejour': o, 'lessaisons': lessaisons(), 'form_create_animateur': form_create_animateur,},
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
		personne = Personne.objects.get(user__id=user_id)
		animateur = Animateur.objects.get(personne__id=personne.id)
		if request.method == 'POST':
			personneform = personneForm(request.POST, instance=personne)
			animateurform = animateurForm(request.POST, instance=animateur)
			if animateurform.is_valid() and personneform.is_valid():
				personneform.save()
				animateurform.save()
				return redirect('/'+ user_id + '/mafiche')
		else:
			personneform = personneForm(instance=personne)
			animateurform = animateurForm(instance=animateur)

		url_action = '/'+ user_id + '/mafiche'
		
		return render_to_response('mafiche.html',
			{'u': u, 'lessaisons': lessaisons(), 'personneform':personneform, 'animateurform':animateurform, 'action': url_action },
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
	if (user.is_superuser):
		return True
	if (int(user_id) == int(user.id)):
		return True
	else:
		logger.error('ca passe pas')
		return False

