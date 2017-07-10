
// html to pdf renderer...

function getPDF(){
	
	var doc = new jsPDF('p', 'pt', 'a1', true);
	doc.fromHTML($('#user_account_content').get(0), 130, 30, {
		'width': 750,
	});
	doc.save('page_file.pdf');

}
