

$(document).on('submit','#valid', function(){
	alert("Slip approved successfully!");
});

$(document).on('submit','#invalid', function(){
	alert("Slip rejected!");
});

// $(document).on('click','#slip_picture', function(){
// 	$(this).width(500);
// });

var $img = $('#slip_picture');
$img.click(function resize(e){
	$img.css({
		height: '25%',
		width: '80%'
	});
});