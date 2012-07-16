$(".rechercheAnimateur").autocomplete({
	source: function( request, response ) {
		$.ajax({
			url: '/rechercheanimateur/'+request.term,
			success: function( data ) {
// 				console.log(data);
				response( $.map( data, function( item ) {
					return {
						label: item.prenom + " " + item.nom + " (" + item.email + ")",
						value: item.prenom + " " + item.nom,
						id: item.id
					}
				}));
			}
		});
	},
	minLength: 3,
	select: function( event, ui ) {
		$hidden = $(this).next('input[type="hidden"]');
		$hidden.val(ui.item.id);
	}
});