# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from sejours.models import *
from sejours.forms import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordResetForm
from userena import views as userena_views
from django.http import HttpResponse
from django.db.models import Q
from time import gmtime, strftime
from django.contrib import messages

import simplejson
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
			messages.success(request, u'Votre fiche a bien été mise à jour. Merci.')
			return redirect('/mafiche')
	else:
		personneform = personneForm(instance=personne)
		animateurform = animateurForm(instance=animateur)

	return render_to_response('mafiche.html',
		{'u': u, 'menu':menu(request), 'personneform':personneform, 'animateurform':animateurform},
		context_instance=RequestContext(request)
	)

@login_required
def animateur(request, animateur_id):
	user = getCurrentUser(request)
	animateur = get_object_or_404(Animateur, pk=animateur_id)
	if (not peut_editer_animateur(animateur, user)):
		logger.error("tentative de voir "+str(animateur.id)+" par "+user.email)
		return redirect('/')
	personne = Personne.objects.get(animateur__id=animateur_id)
	if request.method == 'POST':
		personneform = personneForm(request.POST, instance=personne)
		animateurform = animateurForm(request.POST, instance=animateur)
		if animateurform.is_valid() and personneform.is_valid():
			personneform.save()
			animateurform.save()
			messages.success(request, u'La fiche a bien été mise à jour. Merci.')
			return redirect('/animateur/'+animateur_id)
	else:
		personneform = personneForm(instance=personne)
		animateurform = animateurForm(instance=animateur)

	aujourdhui = strftime("%Y-%m-%d", gmtime())

	sejours = Sejour.objects.filter(animateurs__id=animateur.id, date_fin__gte=aujourdhui).order_by('date_debut')
	convoyages = Convoyage.objects.filter(convoyageanimateur__animateur__id=animateur.id, etape__date_arrivee__gte=aujourdhui)

	return render_to_response('animateur.html',
	{'personne':personne, 'menu':menu(request), 'animateur':animateur, 'personneform':personneform, 'animateurform':animateurform, 'sejours':sejours, 'convoyages':convoyages},
	context_instance=RequestContext(request)
	)

@login_required
def saison(request, saison_id):
	saison = get_object_or_404(Saison, pk=saison_id)
	user = getCurrentUser(request)
	if (not peut_voir_saison(saison_id, user)):
		logger.error(u"tentative de voir la saison "+unicode(saison)+" par "+user.email)
		return redirect('/')

	convoyages = Convoyage.objects.filter(saison_id = saison_id)
	sejoursImport = ''
	convoyagesImport = ''
	if (user.is_superuser):
		# Import de séjour, tsv : id	lieu	nom	date_debut	date_fin (date = YYYY-MM-JJ)
		sejoursImport = csvSejoursImport()
		if (request.method == 'POST' and 'siForm' in request.POST):
			sejoursImport = csvSejoursImport(request.POST, request.FILES)
			if sejoursImport.is_valid():
				m = sejoursImport.save(request.FILES, saison_id)
				messages.success(request, m)
				return  redirect('/saison/'+saison_id)
		# Import de convoyage, tsv : cf forms
		convoyagesImport = csvConvoyagesImport()
		if (request.method == 'POST' and 'convForm' in request.POST):
			convoyagesImport = csvConvoyagesImport(request.POST, request.FILES)
			if convoyagesImport.is_valid():
				m = convoyagesImport.save(request.FILES, saison_id)
				messages.success(request, m)
				return  redirect('/saison/'+saison_id)

	return render_to_response('saison.html',
		{'lasaison':saison, 'convoyages':convoyages, 'menu':menu(request), 'sejoursImport':sejoursImport, 'convoyagesImport':convoyagesImport},
		context_instance=RequestContext(request),
	)

@login_required
def convoyage(request, convoyage_id):
	user = getCurrentUser(request)
	convoyage = get_object_or_404(Convoyage, pk=convoyage_id)
	# être admin ou être lié à ce séjour
	if (peut_voir_convoyage(convoyage, user)):
		caForm = ''
		eFormSet = ''
		eForm = ''
		if (user.is_superuser):
			if request.method == 'POST':
				redir = False
				if ('caForm' in request.POST):
					caForm = convoyageAnimateurForm(request.POST)
					if caForm.is_valid():
						caForm.save()
						messages.success(request, u'Animateur ajouté au convoyage.')
						redir = True
				elif ('eFormSet' in request.POST):
					eFormSet = etapeFormSet(request.POST, queryset=Etape.objects.filter(convoyage_id=convoyage.id).order_by('date_arrivee'))
					if eFormSet.is_valid():
						eFormSet.save()
						messages.success(request, u'Étapes mises à jour. Merci.')
						redir = True
				elif ('eForm' in request.POST):
					eForm = etapeForm(request.POST)
					if eForm.is_valid():
						eForm.save()
						redir = True
						messages.success(request, u'Nouvelle étape créée.')
				if redir:
					return redirect('/convoyage/'+convoyage_id)
			else:
				caForm = convoyageAnimateurForm()
				eFormSet = etapeFormSet(queryset=Etape.objects.filter(convoyage_id=convoyage.id).order_by('date_arrivee'))
				eForm = etapeForm()
		return render_to_response('convoyage.html',
		{'convoyage':convoyage, 'menu':menu(request), 'caForm':caForm, 'eFormSet':eFormSet, 'eForm':eForm},
			context_instance=RequestContext(request)
		)
	else:
		return redirect('/')

@login_required
def sejour(request, sejour_id):
	sejour = get_object_or_404(Sejour, pk=sejour_id)
	sejours = Sejour.objects.filter(saison__id=sejour.saison_id).order_by('numero','nom')
	user = getCurrentUser(request)
	peut_creer_sa = False
	form_sa = ''
	form_create_animateur = ''
	
	# être admin ou être lié à ce séjour
	if (peut_voir_sejour(sejour, user)):
		# admin ou directeur
		if (peut_creer_sejour_animateur(sejour, user)):
			peut_creer_sa = True
			sans_directeur = not user.is_superuser
			# formulaire pour créer un animateur
			form_create_animateur = createAnimateurForm(sejour_id, sans_directeur=sans_directeur)
			if request.method == 'POST':
				# délier un animateur au séjour
				if ('sa_id' in request.POST):
					sa_id = request.POST['sa_id']
					sa = SejourAnimateur.objects.get(pk= sa_id)
					if (int(sa.sejour_id) != int(sejour_id)):
						logger.error('Tentative d effacer SA ' + str(sa_id) + ' par ' + str(user.id))
						return redirect('/sejour/' + sejour_id)
					user_anim = User.objects.get(personne__animateur__id = sa.animateur_id)
					if (user_anim.id == user.id):
						logger.error('Tentative d effacer SA ' + str(sa_id) + ' par lui même ' + str(user.id))
						return redirect('/sejour/' + sejour_id)
					logger.error('efface sejouranimateur n°' + str(sa_id))
					sa.delete()
					messages.success(request, u'Animateur effacé de ce séjour.')
					return redirect('/sejour/' + sejour_id)
				# lier un animateur au séjour
				elif ('sa_form' in request.POST and user.is_superuser):
					animateurId = request.POST['animateurId']
					animateur = Animateur.objects.get(pk = animateurId)
					form_create_animateur = ''
					form_sa = sejourAnimateurForm(animateur, sejour, request.POST)
					if (form_sa.is_valid()):
						form_sa.save(request)
						messages.success(request, u'Animateur lié à ce séjour.')
						return redirect('/sejour/' + sejour_id)
				else:
					# créer un animateur
					form_create_animateur = createAnimateurForm(sejour_id, request.POST, sans_directeur=sans_directeur)
					if (form_create_animateur.is_valid()):
						user = form_create_animateur.save(request)
						messages.success(request, u'Animateur créé, il va recevoir un email de notification.')
						return redirect('/sejour/' + sejour_id)
					elif (user.is_superuser):
						email = request.POST['email']
						sa_user = User.objects.filter(email__iexact=email)
						# si l'animateur existe déjà, proposer de le lier à ce séjour
						if (sa_user):
							animateur = Animateur.objects.filter(personne__user__id=sa_user[0].pk)
							if (animateur):
								animateur = animateur[0]
								sa = SejourAnimateur.objects.filter(animateur_id=animateur.id, sejour_id=sejour.id)
								if (not sa):
									form_create_animateur = ''
									form_sa = sejourAnimateurForm(animateur, sejour, request.POST)
	else:
		return redirect('/')

	return render_to_response('sejour.html',
		{'sejour':sejour, 'sejours':sejours, 'form_create_animateur':form_create_animateur, 'peut_creer_sa':peut_creer_sa, 'sejourAnimateurForm':form_sa, 'menu':menu(request)},
		context_instance=RequestContext(request)
	)

@permission_required('user.is_superuser')
def sejours(request, saison_id):
	saison = get_object_or_404(Saison, pk=saison_id)
	sejours = Sejour.objects.filter(saison__id=saison_id).order_by('numero','nom')
	return render_to_response('sejours.html',
		{'sejours':sejours, 'menu':menu(request)},
		context_instance=RequestContext(request)
	)

@permission_required('user.is_superuser')
def rechercheanimateur(request, recherche):
	#logger.error(recherche)
	animateurs = Animateur.objects.select_related().filter(Q(personne__nom__icontains=recherche) | Q(personne__prenom__icontains=recherche) | Q(personne__user__email__icontains=recherche) | Q(personne__cp__startswith=recherche))
	if animateurs:
		json = simplejson.dumps([({'id':animateur.id, 'nom':animateur.personne.nom, 'prenom':animateur.personne.prenom, 'email':animateur.personne.user.email, 'cp':animateur.personne.cp}) for animateur in animateurs])
	else:
		json = simplejson.dumps([])
	return HttpResponse(json)

@login_required
def index(request):
	return render_to_response('index.html',
		{'menu':menu(request)},
		context_instance=RequestContext(request)
	)

# Fonctions utilitaires

# Droit de lier un animateur à un séjour
# Si l'utilisateur est directeur du séjour
def peut_creer_sejour_animateur(sejour, user):
	if (user.is_superuser):
		return True
	sa = SejourAnimateur.objects.filter(sejour_id=sejour.id, animateur__personne__user__id=user.id)
	if (len(sa)):
		role = sa[0].role
		if (role == 'D'):
			return True
	return False

# Droit de voir un séjour
# Si l'utilisateur fait parti de ce séjour
def peut_voir_sejour(sejour, user):
	if (user.is_superuser):
		return True
	saisonsids = getCurrentSaisonsIds()
	sa = SejourAnimateur.objects.filter(sejour_id=sejour.id, animateur__personne__user__id=user.id, sejour__saison__id__in=saisonsids).count()
	if (sa > 0):
		return True
	logger.error(user.email + u' (n°' +str(user.id) + u') à tenté de voir le séjour n°' + str(sejour.id))
	return False

# Droit de voir un convoyage
# Si l'utilisateur fait parti de ce séjour
# Si le convoyage n'est pas encore passé
def peut_voir_convoyage(convoyage, user):
	if (user.is_superuser):
		return True
	aujourdhui = strftime("%Y-%m-%d", gmtime())
	saisonsids = getCurrentSaisonsIds()
	ca = ConvoyageAnimateur.objects.filter(convoyage_id=convoyage.id, animateur__personne__user__id=user.id, convoyage__saison__id__in=saisonsids).count()
	if (ca > 0):
		return True
	logger.error(user.email + u' (n°' +str(user.id) + u') à tenté de voir le convoyage n°' + str(convoyage.id))
	return False

# Droit de modifier la fiche d'un animateur
# Être directeur du séjour non fini de l'animateur
def peut_editer_animateur(animateur, user):
	if (user.is_superuser):
		return True
	anim_user = Animateur.objects.filter(personne__animateur__id=animateur.id)
	if anim_user and anim_user[0].id == user.id:
		return True
	aujourdhui = strftime("%Y-%m-%d", gmtime())
	sejours = Sejour.objects.filter(date_fin__gte = aujourdhui, animateurs__id=animateur.id)
	if sejours:
		for sejour in sejours:
			if peut_creer_sejour_animateur(sejour, user):
				return True
	return False

# Droit de voir une saison
# Si celle-ci n'est pas encore terminé
def peut_voir_saison(saison_id, user):
	if (user.is_superuser):
		return True
	aujourdhui = strftime("%Y-%m-%d", gmtime())
	nb_sejours = Sejour.objects.filter(date_fin__gte=aujourdhui, saison__id=saison_id).count()
	if (nb_sejours > 0):
		return True;
	return False

# renvoie l'utilisateur courant
def getCurrentUser(request):
	context=RequestContext(request)
	return context.get('user')

# Construction du menu selon l'utilisateur
def menu(request):
	user = getCurrentUser(request)
	saisonsids = getCurrentSaisonsIds()

	saisons = Saison.objects.filter(pk__in=saisonsids)
	sejours = Sejour.objects.filter(animateurs__personne__user__id=user.id, saison__id__in=saisonsids).order_by('date_debut')
	convoyages = Convoyage.objects.filter(convoyageanimateur__animateur__personne__user__id=user.id, saison__id__in=saisonsids)

	menu = {'saisons':saisons, 'sejours':sejours, 'convoyages':convoyages}
	return menu

# renvoie un tableau d'id des saisons non finies
def getCurrentSaisonsIds():
	aujourdhui = strftime("%Y-%m-%d", gmtime())
	saisons = Saison.objects.filter(sejour__date_fin__gte=aujourdhui).distinct()
	saisonsids = [saison.id for saison in saisons]
	return saisonsids
