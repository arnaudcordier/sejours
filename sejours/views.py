# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from sejours.models import *
from sejours.forms import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordResetForm
from userena import views as userena_views

import logging
logger = logging.getLogger('eedf')

@login_required
def mafiche(request):
	user = getCurrentUser(request)
	u = get_object_or_404(User, pk=user.id)
	personne = Personne.objects.get(user__id=user.id)
	animateur = Animateur.objects.get(personne__id=personne.id)
	if request.method == 'POST':
		personneform = personneForm(request.POST, instance=personne)
		animateurform = animateurForm(request.POST, instance=animateur)
		if animateurform.is_valid() and personneform.is_valid():
			personneform.save()
			animateurform.save()
			return redirect('/mafiche')
	else:
		personneform = personneForm(instance=personne)
		animateurform = animateurForm(instance=animateur)

	return render_to_response('mafiche.html',
		{'u': u, 'lessaisons': lessaisons(), 'personneform':personneform, 'animateurform':animateurform },
		context_instance=RequestContext(request)
	)

@login_required
def saison(request, saison_id):
	saison = get_object_or_404(Saison, pk=saison_id)
	convoyages = Convoyage.objects.filter(saison_id = saison_id)
	return render_to_response('saison.html',
		{'lasaison': saison, 'convoyages': convoyages, 'lessaisons': lessaisons(), 'a': PasswordResetForm()},
		context_instance=RequestContext(request),
	)

@login_required
def convoyage(request, convoyage_id):
	user = getCurrentUser(request)
	convoyage = get_object_or_404(Convoyage, pk=convoyage_id)
	return render_to_response('convoyage.html',
		{'convoyage': convoyage, 'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

@login_required
def sejour(request, sejour_id):
	sejour = get_object_or_404(Sejour, pk=sejour_id)
	sejours = Sejour.objects.filter(saison__id=sejour.saison_id).order_by('nom')
	user = getCurrentUser(request)
	# Si c'est un directeur on montre le formulaire de création d'un animateur
	form_create_animateur = ''
	directeur = SejourAnimateur.objects.filter(sejour_id=sejour_id, animateur__personne__user__id=user.id)
	if (len(directeur)):
		role = directeur[0].role
		if (role == 'D'):
			form_create_animateur = createAnimateurForm(sejour_id)
			if request.method == 'POST':
				form_create_animateur = createAnimateurForm(sejour_id, request.POST)
				if form_create_animateur.is_valid():
					user = form_create_animateur.save(request)
					return redirect('/sejour/' + sejour_id)

	return render_to_response('sejour.html',
		{'sejour': sejour, 'sejours': sejours, 'lessaisons': lessaisons(), 'form_create_animateur': form_create_animateur,},
		context_instance=RequestContext(request)
	)

@permission_required('user.is_superuser')
def sejours(request, saison_id):
	saison = get_object_or_404(Saison, pk=saison_id)
	sejours = Sejour.objects.filter(saison__id=saison_id).order_by('nom')
	return render_to_response('sejours.html',
		{'sejours': sejours, 'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

@login_required
def index(request):
	return render_to_response('index.html',
		{'lessaisons': lessaisons()},
		context_instance=RequestContext(request)
	)

# Fonctions utilitaires
def lessaisons(): # TODO: devrait ne renvoyer que les saisons en cours
	saison = Saison.objects.all()
	return saison

def peut_voir_animateur(user, request):
	req = RequestContext(request)
	if (user.is_superuser):
		return True
	else:
		logger.error(user.email + 'à tenté de se connecter')
		return False

# renvoie l'utilisateur courant
def getCurrentUser(request):
	context=RequestContext(request)
	return context.get('user')
