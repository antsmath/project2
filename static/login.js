

// Create register flow if flacker isn't in local storage, update login to register
if (!localStorage.getItem('login_name')) {
	document.getElementById('name').innerHTML = "Register Flack Name";
	document.getElementById('login').innerHTML = "Register";

	//Validate password and repassword match and are greater than 7
	document.getElementById('login').disabled = true;
	document.querySelectorAll('#password, #repassword').forEach(onkeyup = () => {
		if (document.getElementById('repassword').value.length > 7  && document.getElementById('password').value === document.getElementById('repassword').value)
			document.getElementById('login').disabled = false;
		else
			document.getElementById('login').disabled = true;
	});

} else {
	//Place login_name from local storage and make it read only
	document.getElementById('login_name').value = localStorage.getItem('login_name')
	document.getElementById('login_name').readOnly = true;

	// Remove Password fields
	var list = document.getElementById("password_group");
	while (list.hasChildNodes()) {
		list.removeChild(list.firstChild);
	}
};
