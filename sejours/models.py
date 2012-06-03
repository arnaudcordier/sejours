# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile
from django.dispatch import receiver
from userena.signals import *

# signals
@receiver(activation_complete)
def creation_animateur(sender, **kwargs):
	return True

# Create your models here.
class EedfProfile(UserenaBaseProfile):
	user = models.OneToOneField(User,
		unique=True,
		verbose_name=u'Utilisateur',
		related_name='my_profile') 

class Personne(models.Model):
	user = models.OneToOneField(User, verbose_name=u'Utilisateur', blank=True, null=True)
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	prenom = models.CharField(verbose_name=u'Prénom', max_length=50, blank=True)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200, blank=True)
	ville = models.CharField(verbose_name=u'Ville', max_length=50, blank=True)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10, blank=True)
	pays = models.CharField(verbose_name=u'Pays', max_length=50, blank=True)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20, blank=True)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20, blank=True)
	fax = models.CharField(verbose_name=u'Fax', max_length=20, blank=True)
	email = models.EmailField(verbose_name=u'E-mail', blank=True)
	SEXE_CHOIX = ((u'M', u'Masculin'),(u'F', u'Féminin'))
	sexe = models.CharField(verbose_name=u'Sexe', max_length=1, choices=SEXE_CHOIX, blank=True)
	nationalite = models.CharField(verbose_name=u'Nationalité', max_length=50, blank=True)
	naissance_date = models.DateField(verbose_name=u'Date de naissance', blank=True, null=True)
	naissance_ville = models.CharField(verbose_name=u'Ville de naissance', max_length=50, blank=True)
	naissance_departement = models.CharField(verbose_name=u'Département de naissance', max_length=50, blank=True)
	def __unicode__(self):
		return self.nom + ' ' + self.prenom

class Foyer(models.Model):
	responsable = models.ForeignKey(Personne, verbose_name=u'Responsable', blank=True, null=True)
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200, blank=True)
	ville = models.CharField(verbose_name=u'Ville', max_length=50, blank=True)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10, blank=True)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20, blank=True)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20, blank=True)
	fax = models.CharField(verbose_name=u'Fax', max_length=20, blank=True)
	email = models.EmailField(verbose_name=u'E-mail', blank=True)
	FOYER_TYPE = ((u'F', u'Foyer'),(u'P', u'Particuluer'))
	type = models.CharField(verbose_name=u'Type', max_length=1, choices=FOYER_TYPE, blank=True)
	def __unicode__(self):
		return self.nom

class Animateur(models.Model):
	personne = models.OneToOneField(Personne)
	secu_num = models.CharField(verbose_name=u'Numéro de sécu', max_length=50, blank=True)
	bafa = models.BooleanField(verbose_name=u'BAFA')
	afps = models.BooleanField(verbose_name=u'AFPS')
	psc1 = models.BooleanField(verbose_name=u'PSC1')
	psc2 = models.BooleanField(verbose_name=u'PSC2')
	bafd = models.BooleanField(verbose_name=u'BAFD')
	bnssa = models.BooleanField(verbose_name=u'BNSSA')
	sb = models.BooleanField(verbose_name=u'Surveillant de Baignade')
	expe_handicap = models.BooleanField(verbose_name=u'Expériences dans le handicap')
	expe_sejour = models.BooleanField(verbose_name=u'Expériences en séjour')
	texte = models.TextField(verbose_name=u'Informations', blank=True)
	permis_num = models.CharField(verbose_name=u'Numéro de permis', max_length=50, blank=True)
	permis_date = models.DateField(verbose_name=u'Date du permis', blank=True, null=True)
	carte_sejour_num = models.CharField(verbose_name=u'Numéro de carte de séjour', max_length=50, blank=True)
	def __unicode__(self):
		return self.personne.__unicode__()

class Vacancier(models.Model):
	personne = models.OneToOneField(Personne)
	maison = models.ForeignKey(Foyer, verbose_name=u'Lieu d\'habitation', blank=True, null=True, related_name='+')
	foyer = models.ForeignKey(Foyer, verbose_name=u'Foyer fréquenté', blank=True, null=True, related_name='+')
	AUTONOMIE_CHOIX = ((u'B', u'Bonne'),(u'M', u'Moyenne'),(u'R', u'Réduite'))
	autonomie = models.CharField(verbose_name=u'Autonomie', max_length=1, choices=AUTONOMIE_CHOIX, blank=True)
	traitement = models.BooleanField(verbose_name=u'Traitement')
	tuteurs = models.ManyToManyField(Personne, through='Tuteur', related_name='tuteurs')
	def __unicode__(self):
		return self.personne.__unicode__()

class Tuteur(models.Model):
	TUTEUR_ROLE = ((u'1', u'Inscripteur'),(u'2', u'Payeur'),(u'3', u'Consigne'),(u'4', u'Respônsable'),(u'5', u'Contact d\'urgence'))
	vacancier = models.ForeignKey(Vacancier)
	personne = models.ForeignKey(Personne)
	role = models.CharField(verbose_name=u'Rôle', max_length=1, choices=TUTEUR_ROLE, blank=True)
	def __unicode__(self):
		return self.role

class Saison(models.Model):
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	def __unicode__(self):
		return self.nom

class Structure(models.Model):
	proprietaire = models.ForeignKey(Personne, verbose_name=u'Propriétaire', blank=True, null=True)
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200, blank=True)
	ville = models.CharField(verbose_name=u'Ville', max_length=50, blank=True)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10, blank=True)
	pays = models.CharField(verbose_name=u'Pays', max_length=50, blank=True)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20, blank=True)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20, blank=True)
	fax = models.CharField(verbose_name=u'Fax', max_length=20, blank=True)
	email = models.EmailField(verbose_name=u'E-mail', blank=True)
	type_hebergement = models.CharField(verbose_name=u'Type', max_length=50, blank=True)
	nb_place = models.SmallIntegerField(verbose_name=u'Nombre de place', blank=True)
	nb_lit_superpose = models.SmallIntegerField(verbose_name=u'Nombre de lit supperposés', blank=True)
	texte = models.TextField(verbose_name=u'Présentation', blank=True)
	info = models.TextField(verbose_name=u'Informations', blank=True)
	infirmerie = models.BooleanField(verbose_name=u'Infirmerie', blank=True)
	bureau = models.BooleanField(verbose_name=u'Bureau', blank=True)
	internet = models.BooleanField(verbose_name=u'Internet', blank=True)
	wifi = models.BooleanField(verbose_name=u'Wifi', blank=True)
	agreement_js = models.CharField(verbose_name=u'Agréement JS', max_length=50, blank=True)
	dass = models.CharField(verbose_name=u'Numéro DASS', max_length=50, blank=True)
	def __unicode__(self):
		return self.nom

class Sejour(models.Model):
	structure = models.ForeignKey(Structure, verbose_name=u'Structure', blank=True, null=True)
	saison = models.ForeignKey(Saison, verbose_name=u'Saison')
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	numero = models.CharField(verbose_name=u'Numéro', max_length=50)
	date_debut = models.DateField(verbose_name=u'Date de début')
	date_fin = models.DateField(verbose_name=u'Date de fin')
	AUTONOMIE_CHOIX = ((u'B', u'Bonne'),(u'M', u'Moyenne'),(u'R', u'Réduite'))
	autonomie = models.CharField(verbose_name=u'Autonomie', max_length=1, choices=AUTONOMIE_CHOIX, blank=True)
	texte = models.TextField(verbose_name=u'Présentation', blank=True)
	info = models.TextField(verbose_name=u'Informations', blank=True)
	descriptif = models.TextField(verbose_name=u'Descriptif du catalogue', blank=True)
	prix = models.SmallIntegerField(verbose_name=u'Prix', blank=True)
	date_visite = models.DateField(verbose_name=u'Date de la visite', blank=True)
	date_reunion = models.DateField(verbose_name=u'Date de la réunion', blank=True)
	vacanciers = models.ManyToManyField(Vacancier, through='SejourVacancier', related_name='vacanciers')
	animateurs = models.ManyToManyField(Animateur, through='SejourAnimateur', related_name='animateurs')
	def __unicode__(self):
		return self.nom

class SejourVacancier(models.Model):
	sejour = models.ForeignKey(Sejour, verbose_name=u'Séjour')
	vacancier = models.ForeignKey(Vacancier, verbose_name=u'Vacancier')
	ville_depart = models.CharField(verbose_name=u'Ville de départ', max_length=50, blank=True)
	ville_arrivee = models.CharField(verbose_name=u'Ville d\'arrivée', max_length=50, blank=True)
	date_debut = models.DateField(verbose_name=u'Date début', blank=True, null=True)
	date_fin = models.DateField(verbose_name=u'Date fin', blank=True, null=True)
	def __unicode__(self):
		return self.vacancier.__unicode__() + u' à ' + self.sejour.__unicode__()

class SejourAnimateur(models.Model):
	ANIMATEUR_ROLE = ((u'D', u'Directeur'),(u'A', u'Animateur'),(u'S', u'Personne de service'),(u'B', u'Bénévole'))
	sejour = models.ForeignKey(Sejour, verbose_name=u'Séjour')
	animateur = models.ForeignKey(Animateur, verbose_name=u'Animateur')
	date_debut = models.DateField(verbose_name=u'Date début', blank=True, null=True)
	date_fin = models.DateField(verbose_name=u'Date fin', blank=True, null=True)
	role = models.CharField(verbose_name=u'Rôle', max_length=1, choices=ANIMATEUR_ROLE)
	def __unicode__(self):
		return self.animateur.__unicode__() + ' comme ' + self.get_role_display() + u' à ' + self.sejour.__unicode__()

class Bus(models.Model):
	chauffeur = models.ForeignKey(Personne, verbose_name=u'Chauffeur', blank=True, null=True)
	numero = models.CharField(verbose_name=u'Numéro', max_length=50)
	info = models.TextField(verbose_name=u'Informations', blank=True)
	couleur = models.CharField(verbose_name=u'Couleur', max_length=20, blank=True)
	def __unicode__(self):
		return self.numero

class Hebergement(models.Model):
	foyer = models.ForeignKey(Foyer, verbose_name=u'Foyer', blank=True, null=True)
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200, blank=True)
	ville = models.CharField(verbose_name=u'Ville', max_length=50, blank=True)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10, blank=True)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20, blank=True)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20, blank=True)
	fax = models.CharField(verbose_name=u'Fax', max_length=20, blank=True)
	email = models.EmailField(verbose_name=u'E-mail', blank=True)
	def __unicode__(self):
		return self.nom

class Convoyage(models.Model):
	bus = models.ForeignKey(Bus, verbose_name=u'Bus')
	saison = models.ForeignKey(Saison, verbose_name=u'Saison')
	texte = models.TextField(verbose_name=u'Présentation', blank=True)
	info = models.TextField(verbose_name=u'Informations', blank=True)
	def __unicode__(self):
		return self.saison.__unicode__()
	def depart(self):
		e = self.etape_set.order_by('date_arrivee')[0]
		return e
	def arrivee(self):
		e = self.etape_set.order_by('date_arrivee').reverse()[0]
		return e

class Etape(models.Model):
	convoyage = models.ForeignKey(Convoyage, verbose_name=u'Convoyage')
	ville = models.CharField(verbose_name=u'Ville', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200, blank=True)
	date_arrivee = models.DateTimeField(verbose_name=u'Date et heure d\'arrivée')
	date_depart = models.DateTimeField(verbose_name=u'Date et heure de départ')
	info = models.TextField(verbose_name=u'Informations', blank=True)
	souhaits = models.ManyToManyField(Animateur, through='EtapeSouhait', related_name='souhaits')
	def __unicode__(self):
		return self.ville
	def vacancierEntree(self):
		return ConvoyageVacancier.objects.filter(convoyage = self.convoyage, entree = self.id).count()
	def vacancierSortie(self):
		return ConvoyageVacancier.objects.filter(convoyage = self.convoyage, sortie = self.id).count()
	def animateurEntree(self):
		return ConvoyageAnimateur.objects.filter(convoyage = self.convoyage, entree = self.id).count()
	def animateurSortie(self):
		return ConvoyageAnimateur.objects.filter(convoyage = self.convoyage, sortie = self.id).count()

class ConvoyageVacancier(models.Model):
	convoyage = models.ForeignKey(Convoyage, verbose_name=u'Convoyage')
	entree = models.ForeignKey(Etape, verbose_name=u'Étape entrée', related_name='vacanciersentrees')
	sortie = models.ForeignKey(Etape, verbose_name=u'Étape sortie', related_name='vacancierssorties')
	vacancier = models.ForeignKey(Vacancier, verbose_name=u'Vacancier')
	hebergement = models.ForeignKey(Hebergement, verbose_name=u'Hébergement', blank=True, null=True)
	def __unicode__(self):
		return self.vacancier.__unicode__()

class ConvoyageAnimateur(models.Model):
	CONVOYEUR_ROLE = ((u'R', u'Responsable'),(u'M', u'Responsable médicament'),(u'C', u'Convoyeur'),(u'V', u'Voyageur'))
	convoyage = models.ForeignKey(Convoyage, verbose_name=u'Convoyage')
	entree = models.ForeignKey(Etape, verbose_name=u'Étape entrée', related_name='animateursentrees')
	sortie = models.ForeignKey(Etape, verbose_name=u'Étape sortie', related_name='animateurssorties')
	animateur = models.ForeignKey(Animateur, verbose_name=u'Animateur')
	hebergement = models.ForeignKey(Hebergement, verbose_name=u'Hébergement', blank=True, null=True)
	role = models.CharField(verbose_name=u'Rôle', max_length=1, choices=CONVOYEUR_ROLE)
	def __unicode__(self):
		return self.role

class EtapeSouhait(models.Model):
	etape = models.ForeignKey(Etape, verbose_name=u'Étape')
	animateur = models.ForeignKey(Animateur, verbose_name=u'Animateur')
	saison = models.ForeignKey(Saison, verbose_name=u'Saison')
	rang = models.SmallIntegerField(verbose_name=u'Ordre de préférence')
	def __unicode__(self):
		return self.etape.__unicode__()
