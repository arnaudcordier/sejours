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
		// 		console.log( ui.item ?
		// 			"Selected: " + ui.item.label + "," + ui.item.id :
		// 			"Nothing selected, input was " + this.value);
	},
	open: function() {
		$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
	},
	close: function() {
		$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
	}
});