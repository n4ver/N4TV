function validateForm() {
	var url = document.forms["logGetter"]["logsurl"].value;
	console.log(url);
	if (url.match(/^(https:\/\/logs\.tf\/)(\d+)(#\d+)$/) != null) {
		var match = url.match(/^(https:\/\/logs\.tf\/)(\d+)(#\d+)$/);
		var log = match[2];
	}
	else if (url.match(/^(https:\/\/logs\.tf\/)(\d+)(#)$/) != null) {
		var match = url.match(/^(https:\/\/logs\.tf\/)(\d+)(#)$/);
		var log = match[2];
	}
	else if (url.match(/^(https:\/\/logs\.tf\/)(\d+)$/) != null){
		var match = url.match(/^(https:\/\/logs\.tf\/)(\d+)$/);
		var log = match[2];
	}
	else {
		alert("Invalid Log");
		return false;
	}
	console.log(log);
	return true;
}