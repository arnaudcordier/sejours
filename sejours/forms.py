# -*- coding: utf-8 -*-
from django.forms import ModelForm
from sejours.models import *
from django import forms
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from userena.models import UserenaSignup
from django.template import loader
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.forms.models import modelformset_factory

import random

import logging
logger = logging.getLogger('eedf')

# Les formulaires
class personneForm(ModelForm):
	class Meta:
		model = Personne
		exclude = ('user','email')

class animateurForm(ModelForm):
	class Meta:
		model = Animateur
		exclude = ('personne')

class convoyageAnimateurForm(ModelForm):
	class Meta:
		model = ConvoyageAnimateur

class etapeForm(ModelForm):
	class Meta:
		model = Etape

class structureForm(ModelForm):
	class Meta:
		model = Structure
		exclude = ('proprietaire')

etapeFormSet = modelformset_factory(Etape, extra=0)

#Lier un animateur à un séjour
class sejourAnimateurForm(ModelForm):
	class Meta:
		model = SejourAnimateur
		exclude = ('sejour','animateur','date_debut','date_fin')
	
	def __init__(self, animateur, sejour, *args, **kwargs):
		super(sejourAnimateurForm, self).__init__(*args, **kwargs)
		self.animateur = animateur
		self.sejour = sejour

	def save(self, request):
		role = self.cleaned_data['role']
		sa = SejourAnimateur(sejour_id=self.sejour.id, animateur_id=self.animateur.id, role=role)
		sa.save()
		return sa

class createAnimateurForm(forms.Form):
	nom = forms.CharField(label=u'Nom', max_length=30, required=False)
	prenom = forms.CharField(label=u'Prénom', max_length=30, required=False)
	email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'required'}, maxlength=75)))
	role = forms.ChoiceField(label=u'Rôle', choices=SejourAnimateur.ANIMATEUR_ROLE)

	def __init__(self, sejour_id, *args, **kwargs):
		sans_directeur = kwargs.pop('sans_directeur', True)
		super(createAnimateurForm, self).__init__(*args, **kwargs)

		if (sans_directeur):
			choixsansdirecteur = SejourAnimateur.ANIMATEUR_ROLE[:]
			choixsansdirecteur.remove((u'D', u'Directeur'))
			self.fields['role'].choices = choixsansdirecteur
		
		self.sejour_id = sejour_id
		
	def clean_email(self):
		""" Validate that the e-mail address is unique. """
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError('Cet email existe déjà. Veuillez en choisir un autre')
		return self.cleaned_data['email']

	def save(self, request):
		""" Generate a random username before falling back to parent signup form """
		while True:
			username = sha_constructor(str(random.random())).hexdigest()[:5]
			try:
				User.objects.get(username__iexact=username)
			except User.DoesNotExist: break
		password = sha_constructor(str(random.random())).hexdigest()[:6]
		nom = self.cleaned_data['nom']
		prenom = self.cleaned_data['prenom']
		email = self.cleaned_data['email']
		role = self.cleaned_data['role']
		new_user = UserenaSignup.objects.create_user(username, email, password, True, False) # activé, pas de mail
		animateur_id = createAnimateur(nom, prenom, email, new_user.id)
		sejour = SejourAnimateur(sejour_id=self.sejour_id, animateur_id=animateur_id, role=role)
		sejour.save()
		# envoi d'un mail d'invite à choisir un mot de passe
		from django.core.mail import send_mail
		from django.conf import settings
		current_site = get_current_site(request)
		site_name = current_site.name
		domain = current_site.domain
		c = {
			'email': email,
			'domain': domain,
			'site_name': site_name,
			'uid': int_to_base36(new_user.id),
			'user': new_user,
			'token': default_token_generator.make_token(new_user),
			'protocol': 'http',
			}
		subject = loader.render_to_string('animcreation_sujet.html', c)
		subject = ''.join(subject.splitlines())
		email = loader.render_to_string('animcreation_body.html', c)
		send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [new_user.email])
				
		return new_user

class csvSejoursImport(forms.Form):
	fichier = forms.FileField()

	# Import de séjour, tsv : id	lieu	nom	date_debut	date_fin (date = YYYY-MM-JJ)
	def save(self, tsv, saison_id):
		imported = 0;
		total = 0;
		for line in tsv['fichier']:
			fields = line.strip().split("\t")
			total += 1
			if len(fields) == 5:
				try:
					sej = Sejour.objects.get(saison_id=saison_id, numero=fields[0])
				except Sejour.DoesNotExist:
					imported += 1
					sej = Sejour.objects.create(saison_id=saison_id, numero=fields[0], nom=fields[2], date_debut=fields[3], date_fin=fields[4])
		return str(imported) + u' séjours importés sur ' + str(total)

class csvConvoyagesImport(forms.Form):
	fichier = forms.FileField()
	
	# Import de convoyage
	# bus	ville étape	date arrivé	date départ	entrée	sortie
	def save(self, tsv, saison_id):
		imported = 0
		total = 0
		for line in tsv['fichier']:
			fields = line.strip().split("\t")
			total += 1
			if len(fields) == 6:
				# trouver le convoyage, sinon créer le bus et le convoyage
				try:
					conv = Convoyage.objects.get(saison_id=saison_id, bus__numero=fields[0])
				except Convoyage.DoesNotExist:
					bus = Bus.objects.create(numero=fields[0])
					conv = Convoyage.objects.create(saison_id=saison_id, bus_id=bus.id)
				# créer l'étape
				etape = Etape.objects.create(convoyage_id=conv.id, ville=fields[1], date_arrivee=fields[2], date_depart=fields[3], entree=fields[4], sortie=fields[5])
				imported += 1
		return str(imported) + u' étapes importés sur ' + str(total)
