
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

window.onload = (event) => {
	window.addEventListener('keypress', function (e) {
        data = {
            "start": "30.5",
            "end": "34.29"
        }
        postAjax("/playAudio", data)
	});
};