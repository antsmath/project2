

// Create register flow if flacker isn't in local storage, update login to register
if (!localStorage.getItem('login_name')) {
	document.getElementById('name').innerHTML = "Register Flack Name";
	document.getElementById('login').innerHTML = "Register";

	//Validate password and repassword match and are greater than 7
	
	document.getElementById('login-form').addEventListener("submit", validatePassword);
	function validatePassword() {
		let submitFlag = true; 
		if (document.getElementById('password').value === document.getElementById('repassword').value)
			submitFlag = true;
		else {
			submitFlag = false;
			alert("Uh Oh! The Re-entered password did not match password.");
		}
		return submitFlag
	};

} else {
	//Place login_name from local storage and make it read only
	document.getElementById('name').innerHTML = "Welcome back " + localStorage.getItem('login_name') + "!";
	document.getElementById('login_name').value = localStorage.getItem('login_name')

	// Remove Password fields
	var list = document.getElementById("repassword");
	while (list.hasChildNodes()) {
		list.removeChild(list.firstChild);
	}
};
