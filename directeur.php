<?php

// 	N°;VILLE DE SEJOUR;Nom du séjour;DIRECTEUR;BAFD GRATUIT;Adresse 1;Adresse 2;CP;VILLE;DATE DE NAISSANCE;LIEU DE NAISSANCE;TEL;TEL PORTABLE;E-mail;N° de Permis;N° de Carte d'Identité

$fichier = file_get_contents('directeur utf.csv');

$lignes = split("\n", $fichier);
$definition = array_shift($lignes);

$user_pk = 1;
$personne_pk = 0;

foreach ($lignes as $ligne) {
	$champs = explode(';', $ligne);
	if (!empty($champs)) {
		array_map('trim', $champs);
	foreach($champs as $k => $v) {
		$champs[$k] = preg_replace('/[\',]/',' ',$v);
	}

	list ($num, $sejour_ville, $sejour_nom, $nom, $bafd, $adresse1, $adresse2, $cp, $ville, $naissance_date, $naissance_lieu, $tel, $portable, $email, $permis_num, $identite_num) = $champs;

		$user_pk++;
		$personne_pk++;
		$username = preg_replace('/ /','',$nom)."_$user_pk";
		preg_match('/(\d\d)\/(\d\d)\/(\d\d\d\d)/',$naissance_date,$dates);
		if ($dates)
			$naissance_date = $dates[3]."-".$dates[2]."-".$dates[1];
		else
			$naissance_date = '';
		preg_match('/(.*)( \((\d\d)\) *)$/', $naissance_lieu, $naissance);
		if ($naissance) {
			$naissance_lieu = $naissance[1];
			$naissance_departement = $naissance[3];
		} else {
		 $naissance_departement = '';
		}
echo <<<B
- fields:
    date_joined: 2012-05-05 13:41:58+00:00
    email: '$email'
    first_name: ''
    groups: [2]
    is_active: true
    is_staff: false
    is_superuser: false
    last_login: 2012-06-07 07:07:20+00:00
    last_name: '$nom'
    password: ''
    user_permissions: []
    username: '$username'
  model: auth.user
  pk: $user_pk
- fields: {mugshot: '', privacy: registered, user: $user_pk}
  model: sejours.eedfprofile
  pk: $user_pk
- fields: {adresse: '$adresse1', cp: '$cp', email: '$email',
    fax: '', mobile: '$portable', naissance_date: $naissance_date, naissance_departement: '$naissance_departement',
    naissance_ville: '$naissance_lieu', nationalite: "Française", nom: '$nom', pays: France,
    prenom: '', sexe: M, tel: '$tel', user: $user_pk, ville: '$ville'}
  model: sejours.personne
  pk: $personne_pk
- fields: {afps: false, bafa: false, bafd: true, bnssa: false, carte_sejour_num: '', identite_num: '$identite_num',
    expe_handicap: false, expe_sejour: false, permis_date: null, permis_num: '$permis_num', personne: $personne_pk,
    psc1: false, psc2: false, sb: false, secu_num: '', texte: ''}
  model: sejours.animateur
  pk: $personne_pk

B;
	}
}

?>