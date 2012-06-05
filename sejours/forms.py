# -*- coding: utf-8 -*-
from django.forms import ModelForm
from sejours.models import *
from django import forms
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from userena.models import UserenaSignup

import random

import logging
logger = logging.getLogger('eedf')

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

class createAnimateurForm(forms.Form):
	nom = forms.CharField(label=u'Nom', max_length=30, required=False)
	prenom = forms.CharField(label=u'Prénom', max_length=30, required=False)
	email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'required'}, maxlength=75)))

	def __init__(self, sejour_id, *args, **kwargs):
		super(createAnimateurForm, self).__init__(*args, **kwargs)
		logger.error(sejour_id)
		self.sejour_id = sejour_id
		
	def clean_email(self):
		""" Validate that the e-mail address is unique. """
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError('Cet email existe déjà. Veuillez en choisir un autre')
		return self.cleaned_data['email']

	def save(self):
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
		new_user = UserenaSignup.objects.create_user(username, email, password, True, False) # activé, pas de mail
		personne = Personne(user_id = new_user.id, nom=nom, prenom=prenom)
		personne.save()
		animateur = Animateur(personne_id = personne.pk)
		animateur.save()
		sejour = SejourAnimateur(sejour_id=self.sejour_id, animateur_id=animateur.pk, role='A')
		sejour.save()
		return new_user
