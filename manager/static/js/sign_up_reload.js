jQuery(document).ready(function(){
	var name = $("#name").val(),
		surname = $("#surname").val();
		birth_date = $("#birth_date").val();
		nid = $("#nid").val();
		phone = $("#phone").val();

	if (name != "" && surname != "" && birth_date != "" && nid != "" && phone != "")
		location.reload(); 
});