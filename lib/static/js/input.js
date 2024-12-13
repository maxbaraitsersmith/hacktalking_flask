var inputDOM;
var tagify;
var justSubmitted = true;
var inputSuggestions = [];

function postAjax(url,data={},successFunc=null) {
	$.ajax({ 
		url: url, 
		type: 'POST', 
		contentType: 'application/json', 
		data: data,

		success: function(response) {  
			if (successFunc) {successFunc(response);}
		}
	}); 
}
function catchError(response) {
	if (response.error == true) {
		textbox.value = "ERROR SENDING DATA";
	}
}

function isANumber(str) { //check if string is a number
	if (typeof str != "string") return false 
	return !isNaN(str) && 
		!isNaN(parseFloat(str)) 
}

function submit(value) {
	var datum = {
		"type": "input",
		"text": value,
		"timestamp": Date.now()/1000.0, //time since epoch in seconds
	};
	postAjax('/addDatum',JSON.stringify(datum),catchError);
	tagify.removeAllTags();
	window.setTimeout(tagify.dropdown.show, 1);
	justSubmitted = true;
	inputDOM.innerHTML = "";
}

window.onload = (event) => {
	postAjax("/getInputSuggestions",{}, (_inputSuggestions) => {
		// for (var i=0;i<_inputSuggestions.length;i++) {
		// 	_inputSuggestions[i] = (i+1)+" "+_inputSuggestions[i];
		// }
		inputSuggestions = _inputSuggestions
		tagify = new Tagify($("#input")[0], {
			whitelist: _inputSuggestions,
			focusable: false,
			autoComplete: {enabled: true},
			dropdown: {
				position: 'input',
				enabled: 0,
				closeOnSelect : true,
				highlightFirst: true
			}
		});
		tagify.on("add", function(e) {
			submit(e.detail.data.value)
		})
		tagify.dropdown.show();
		inputDOM = $(".tagify__input")[0];
	});

	window.addEventListener('keypress', function (e) {

		if (justSubmitted && e.key.length == 1 && e.key != 0 && isANumber(e.key)) {
			if (e.key-1 < inputSuggestions.length) {
				window.setTimeout( function(){
					submit(inputSuggestions[e.key-1]);
					justSubmitted = true;
				}, 1);
			}
		}
		else {
			justSubmitted = false;
		}
	});
};