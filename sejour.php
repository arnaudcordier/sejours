<?php

// 	N°;VILLE DE SEJOUR;Nom du séjour;DIRECTEUR;BAFD GRATUIT;Adresse 1;Adresse 2;CP;VILLE;DATE DE NAISSANCE;LIEU DE NAISSANCE;TEL;TEL PORTABLE;E-mail;N° de Permis;N° de Carte d'Identité

$fichier = file_get_contents('sejour utf.csv');

$lignes = split("\n", $fichier);
$definition = array_shift($lignes);

$sejour_pk = 0;

foreach ($lignes as $num => $ligne) {
	$champs = explode(';', $ligne);
	if (!empty($champs)) {
		array_map('trim', $champs);
		foreach($champs as $k => $v) {
			$champs[$k] = preg_replace('/[\',]/',' ',$v);
		}

		list ($code, $sejour) = $champs;

		$sejour_pk++;
		preg_match('/(.*) - du (\d\d)\.\d(\d)\.\d\d au (\d\d)\.\d(\d)\.\d\d/',$sejour,$m);
		if ($m) {
			$sejour = $m[1];
			$debut = "2012-".$m[3]."-".$m[2];
			$fin = "2012-".$m[5]."-".$m[4];
		} else {
			echo "problème ligne $num : $sejour\n";
		}

echo <<<B
- fields: {autonomie: B, date_debut: $debut, date_fin: $fin, date_reunion: null,
    date_visite: null, descriptif: '', info: '', nom: '$sejour', numero: '$code',
    prix: 0, saison: 1, structure: , texte: ''}
  model: sejours.sejour
  pk: $sejour_pk

B;
	}
}

?>