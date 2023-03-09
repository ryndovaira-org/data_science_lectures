$(document).ready(function() {
	QuestionsSetup();
});

window.onresize = function(){
	QuestionsSetup();
}

function clickAnswer(id, ans, ind) {

	var radios = document.getElementsByName(id);
	var i = 0, len = radios.length;
	var checked = false;
	var userAnswer;
	var answer_id = [];
	var userChoice = -1;

	for( ; i < len; i++ ) {

		answer_id.push(radios[i].value);
		if(radios[i].checked) {
			checked = true;
			userAnswer = radios[i].value;
			userChoice = i + 1;
		}
	}

	if(userChoice == -1){
		return;
	}

	num_of_questions = ($(".questions-body").size());

	if(document.getElementById(id).style.display != "block"){

		ind = ind - 1;

		shift = parseInt($("#" + id).css('height'));

		for(i = 0; i < len; i++){
			h = $("#" + id + answer_id[i]).css('height');
			shift = parseInt(h) + shift;
		}

		//shift = shift;

		anchor = $(".question:eq("+ind+")");

	    h = anchor.height();
		anchor.css('height', h + shift + 'px');

	    ind += 1;

	    for(; ind < num_of_questions; ++ind){

		    body = $(".questions-body:eq(" + ind + ")");

		    height = body.outerHeight();

		    offsetTop = body.position().top;

		    body.css('top', offsetTop + shift + 'px');

	    }
	}

	if(userChoice == ans){
		document.getElementById(id).innerHTML = "<h5 style=\"color:green;\">Correct!</h5>";
		document.getElementById(id).style.display = "block";
		for(i = 0; i < len; i++){
			document.getElementById(id + answer_id[i]).style.display = "block";
		}

	} else {
		document.getElementById(id).innerHTML = "<h5 style=\"color:red;\">Incorrect. Please review your feedback above.</h5>";
		document.getElementById(id).style.display = "block";
		for(i = 0; i < len; i++){
			document.getElementById(id + answer_id[i]).style.display = "block";
		}
	}

	QuestionsSetup();

}

function QuestionsSetup() {

	// vertically align sidenote body with sidenote
	function align(anchor, body) {
		var height = body.outerHeight(), offsetTop = anchor.position().top;

        anchor.css('height', height + 'px');
		body.css('top', offsetTop + 'px');
		//body.css('top', align.offsetTop + 'px');

	}

	$(".question").each(function(index) {
		//alert($(this).height());
		var anchor = $(this),
			body = $(".questions-body:eq(" + index + ")");
			align(anchor, body);

	});

}
