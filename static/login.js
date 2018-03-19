

// Create register flow if flacker isn't in local storage, update login to register
if (!localStorage.getItem('user_name')) {
	document.getElementById('name').innerHTML = "Register Flack Name";
	document.getElementById('login').innerHTML = "Register";

	//Validate password and repassword match
	document.getElementById('login').onclick = () => {
		let submitFlag = true;
		if (!(document.getElementById('password').value === document.getElementById('repassword').value)) {
			alert("Uh Oh! The Re-entered password did not match password.");
			event.preventDefault();
		}
	};

} else {
	//Place user_name from local storage and make it read only
	document.getElementById('name').innerHTML = "Welcome back " + localStorage.getItem('user_name') + "!";
	document.getElementById('user_name').value = localStorage.getItem('user_name')

	// Remove Repassword field for login
	var list = document.getElementById("repassword-main");
	while (list.hasChildNodes()) {
		list.removeChild(list.firstChild);
	}
};
