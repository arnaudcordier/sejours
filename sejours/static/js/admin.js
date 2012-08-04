$("#voir_animateur_form").submit(function() {
	var id = $("#voir_animateur").val();
	if (id) document.location = "/animateur/" + id;
	return false;
});

$("#voir_animateur_form .rechercheAnimateur")
	.autocomplete("option",{
		select: function( event, ui ) {
			$hidden = $(this).next('input[type="hidden"]');
			$hidden.val(ui.item.id);
			$("#voir_animateur_form").submit();
		}
	}
);