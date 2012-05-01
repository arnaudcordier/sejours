# -*- coding: utf8 -*-
from django.db import models

# Create your models here.

class Personne(models.Model):
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	prenom = models.CharField(verbose_name=u'Prénom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200)
	ville = models.CharField(verbose_name=u'Ville', max_length=50)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10)
	pays = models.CharField(verbose_name=u'Pays', max_length=50)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20)
	fax = models.CharField(verbose_name=u'Fax', max_length=20)
	email = models.EmailField(verbose_name=u'E-mail')
	SEXE_CHOIX = ((u'M', u'Masculin'),(u'F', u'Féminin'))
	sexe = models.CharField(verbose_name=u'Sexe', max_length=1, choices=SEXE_CHOIX)
	nationalite = models.CharField(verbose_name=u'Nationalité', max_length=50)
	naissance_date = models.DateField(verbose_name=u'Date de naissance')
	naissance_ville = models.CharField(verbose_name=u'Ville de naissance', max_length=50)
	naissance_departement = models.CharField(verbose_name=u'Département de naissance', max_length=50)
	def __unicode__(self):
		return self.nom + ' ' + self.prenom

class Foyer(models.Model):
	responsable = models.ForeignKey(Personne, verbose_name=u'Responsable')
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200)
	ville = models.CharField(verbose_name=u'Ville', max_length=50)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20)
	fax = models.CharField(verbose_name=u'Fax', max_length=20)
	email = models.EmailField(verbose_name=u'E-mail')
	FOYER_TYPE = ((u'F', u'Foyer'),(u'P', u'Particuluer'))
	type = models.CharField(verbose_name=u'Type', max_length=1, choices=FOYER_TYPE)
	def __unicode__(self):
		return self.nom

class Animateur(models.Model):
	personne = models.OneToOneField(Personne)
	secu_num = models.CharField(verbose_name=u'Numéro de sécu', max_length=50)
	bafa = models.BooleanField(verbose_name=u'BAFA')
	afps = models.BooleanField(verbose_name=u'AFPS')
	psc1 = models.BooleanField(verbose_name=u'PSC1')
	psc2 = models.BooleanField(verbose_name=u'PSC2')
	bafd = models.BooleanField(verbose_name=u'BAFD')
	bnssa = models.BooleanField(verbose_name=u'BNSSA')
	sb = models.BooleanField(verbose_name=u'Surveillant de Baignade')
	expe_handicap = models.BooleanField(verbose_name=u'Expériences dans le handicap')
	expe_sejour = models.BooleanField(verbose_name=u'Expériences en séjour')
	texte = models.TextField(verbose_name=u'Informations')
	permis_num = models.CharField(verbose_name=u'Numéro de permis', max_length=50)
	permis_date = models.DateField(verbose_name=u'Date du permis')
	carte_sejour_num = models.CharField(verbose_name=u'Numéro de carte de séjour', max_length=50)
	def __unicode__(self):
		return self.personne.__str__()

class Vacancier(models.Model):
	personne = models.OneToOneField(Personne)
	maison = models.ForeignKey(Foyer, verbose_name=u'Lieu d\'habitation', related_name='+')
	foyer = models.ForeignKey(Foyer, verbose_name=u'Foyer fréquenté', related_name='+')
	AUTONOMIE_CHOIX = ((u'B', u'Bonne'),(u'M', u'Moyenne'),(u'R', u'Réduite'))
	autonomie = models.CharField(verbose_name=u'Autonomie', max_length=1, choices=AUTONOMIE_CHOIX)
	traitement = models.BooleanField(verbose_name=u'Traitement')
	tuteurs = models.ManyToManyField(Personne, through='Tuteur', related_name='personne')
	def __unicode__(self):
		return self.personne.__str__()

class Tuteur(models.Model):
	TUTEUR_ROLE = ((u'1', u'Inscripteur'),(u'2', u'Payeur'),(u'3', u'Consigne'),(u'4', u'Respônsable'),(u'5', u'Contact d\'urgence'))
	vacancier = models.ForeignKey(Vacancier)
	personne = models.ForeignKey(Personne)
	role = models.CharField(verbose_name=u'Rôle', max_length=1, choices=TUTEUR_ROLE)
	def __unicode__(self):
		return self.role

class Saison(models.Model):
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	def __unicode__(self):
		return self.nom

class Structure(models.Model):
	proprietaire = models.ForeignKey(Personne, verbose_name=u'Propriétaire')
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200)
	ville = models.CharField(verbose_name=u'Ville', max_length=50)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10)
	pays = models.CharField(verbose_name=u'Pays', max_length=50)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20)
	fax = models.CharField(verbose_name=u'Fax', max_length=20)
	email = models.EmailField(verbose_name=u'E-mail')
	type_hebergement = models.CharField(verbose_name=u'Type', max_length=50)
	nb_place = models.SmallIntegerField(verbose_name=u'Nombre de place')
	nb_lit_superpose = models.SmallIntegerField(verbose_name=u'Nombre de lit supperposés')
	texte = models.TextField(verbose_name=u'Présentation')
	info = models.TextField(verbose_name=u'Informations')
	infirmerie = models.BooleanField(verbose_name=u'Infirmerie')
	bureau = models.BooleanField(verbose_name=u'Bureau')
	internet = models.BooleanField(verbose_name=u'Internet')
	wifi = models.BooleanField(verbose_name=u'Wifi')
	agreement_js = models.CharField(verbose_name=u'Agréement JS', max_length=50)
	dass = models.CharField(verbose_name=u'Numéro DASS', max_length=50)
	def __unicode__(self):
		return self.nom

class Sejour(models.Model):
	structure = models.ForeignKey(Structure, verbose_name=u'Structure')
	saison = models.ForeignKey(Saison, verbose_name=u'Saison')
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	numero = models.CharField(verbose_name=u'Numéro', max_length=50)
	date_debut = models.DateField(verbose_name=u'Date de début')
	date_fin = models.DateField(verbose_name=u'Date de fin')
	AUTONOMIE_CHOIX = ((u'B', u'Bonne'),(u'M', u'Moyenne'),(u'R', u'Réduite'))
	autonomie = models.CharField(verbose_name=u'Autonomie', max_length=1, choices=AUTONOMIE_CHOIX)
	texte = models.TextField(verbose_name=u'Présentation')
	info = models.TextField(verbose_name=u'Informations')
	descriptif = models.TextField(verbose_name=u'Descriptif du catalogue')
	prix = models.SmallIntegerField(verbose_name=u'Prix')
	date_visite = models.DateField(verbose_name=u'Date de la visite')
	date_reunion = models.DateField(verbose_name=u'Date de la réunion')
	vacanciers = models.ManyToManyField(Vacancier, through='SejourVacancier', related_name='vacancier')
	animateurs = models.ManyToManyField(Animateur, through='SejourAnimateur', related_name='animateur')
	def __unicode__(self):
		return self.nom

class SejourVacancier(models.Model):
	sejour = models.ForeignKey(Sejour, verbose_name=u'Séjour')
	vacancier = models.ForeignKey(Vacancier, verbose_name=u'Vacancier')
	ville_depart = models.CharField(verbose_name=u'Ville de départ', max_length=50)
	ville_arrivee = models.CharField(verbose_name=u'Ville d\'arrivée', max_length=50)
	date_debut = models.DateField(verbose_name=u'Date début')
	date_fin = models.DateField(verbose_name=u'Date fin')
	def __unicode__(self):
		return 'du ' + self.date_debut + ' au ' + self.date_fin

class SejourAnimateur(models.Model):
	ANIMATEUR_ROLE = ((u'D', u'Directeur'),(u'A', u'Animateur'),(u'S', u'Personne de service'),(u'B', u'Bénévole'))
	sejour = models.ForeignKey(Sejour, verbose_name=u'Séjour')
	animateur = models.ForeignKey(Animateur, verbose_name=u'Animateur')
	date_debut = models.DateField(verbose_name=u'Date début')
	date_fin = models.DateField(verbose_name=u'Date fin')
	role = models.CharField(verbose_name=u'Rôle', max_length=1, choices=ANIMATEUR_ROLE)
	def __unicode__(self):
		return self.role + ' du ' + self.date_debut + ' au ' + self.date_fin

class Bus(models.Model):
	chauffeur = models.ForeignKey(Personne, verbose_name=u'Chauffeur')
	numero = models.CharField(verbose_name=u'Numéro', max_length=50)
	info = models.TextField(verbose_name=u'Informations')
	couleur = models.CharField(verbose_name=u'Couleur', max_length=20)
	def __unicode__(self):
		return self.couleur

class Hebergement(models.Model):
	foyer = models.ForeignKey(Foyer, verbose_name=u'Foyer')
	nom = models.CharField(verbose_name=u'Nom', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200)
	ville = models.CharField(verbose_name=u'Ville', max_length=50)
	cp = models.CharField(verbose_name=u'Code postal', max_length=10)
	tel = models.CharField(verbose_name=u'Téléphone', max_length=20)
	mobile = models.CharField(verbose_name=u'Mobile', max_length=20)
	fax = models.CharField(verbose_name=u'Fax', max_length=20)
	email = models.EmailField(verbose_name=u'E-mail')
	def __unicode__(self):
		return self.nom

class Convoyage(models.Model):
	bus = models.ForeignKey(Bus, verbose_name=u'Bus')
	saison = models.ForeignKey(Saison, verbose_name=u'Saison')
	texte = models.TextField(verbose_name=u'Présentation')
	info = models.TextField(verbose_name=u'Informations')
	def __unicode__(self):
		return self.saison.__unicode__()

class Etape(models.Model):
	convoyage = models.ForeignKey(Convoyage, verbose_name=u'Convoyage')
	ville = models.CharField(verbose_name=u'Ville', max_length=50)
	adresse = models.CharField(verbose_name=u'Adresse', max_length=200)
	date_arrivee = models.DateTimeField(verbose_name=u'Date et heure d\'arrivée')
	date_depart = models.DateTimeField(verbose_name=u'Date et heure de départ')
	info = models.TextField(verbose_name=u'Informations')
	vacanciers = models.ManyToManyField(Vacancier, through='EtapeVacancier')
	animateurs = models.ManyToManyField(Animateur, through='EtapeAnimateur')
	souhaits = models.ManyToManyField(Animateur, through='EtapeSouhait', related_name='+')
	def __unicode__(self):
		return self.ville

class EtapeVacancier(models.Model):
	etape = models.ForeignKey(Etape, verbose_name=u'Étape')
	vacancier = models.ForeignKey(Vacancier, verbose_name=u'Vacancier')
	entre = models.BooleanField(verbose_name=u'Rentre')
	hebergement = models.ForeignKey(Hebergement, verbose_name=u'Hébergement')
	def __unicode__(self):
		return self.vacancier.__unicode__()

class EtapeAnimateur(models.Model):
	CONVOYEUR_ROLE = ((u'R', u'Responsable'),(u'M', u'Responsable médicament'),(u'C', u'Convoyeur'),(u'V', u'Voyageur'))
	etape = models.ForeignKey(Etape, verbose_name=u'Étape')
	animateur = models.ForeignKey(Animateur, verbose_name=u'Animateur')
	entre = models.BooleanField(verbose_name=u'Rentre')
	hebergement = models.ForeignKey(Hebergement, verbose_name=u'Hébergement')
	role = models.CharField(verbose_name=u'Rôle', max_length=1, choices=CONVOYEUR_ROLE)
	def __unicode__(self):
		return self.role

class EtapeSouhait(models.Model):
	etape = models.ForeignKey(Etape, verbose_name=u'Étape')
	animateur = models.ForeignKey(Animateur, verbose_name=u'Animateur')
	rang = models.SmallIntegerField(verbose_name=u'Ordre de préférence')
	def __unicode__(self):
		return self.etape.__unicode__()
