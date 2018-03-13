function populateUserTable(){
	var URL = "/account/all"
	$.post(URL, null, function(response)
	    {
	    	if(response.errno==0)
    		{
		    	var table = document.getElementById("admin_user_table");
		    	var old_tbody = table.getElementsByTagName("tbody")[0];
		    	var new_tbody = document.createElement("tbody");

		    	for(var i = 0; i < response.data.length; i++){
		    		var row = new_tbody.insertRow(-1);
		    		row.id = response.data[i].username;

		    		var username = row.insertCell(-1);
		    		username.innerHTML = response.data[i].username;
		    		username.style.textAlign = "center";

		    		var firstName = row.insertCell(-1);
		    		firstName.innerHTML = response.data[i].first_name;
		    		firstName.style.textAlign = "center";

		    		var lastName = row.insertCell(-1);
		    		lastName.innerHTML = response.data[i].last_name;
		    		lastName.style.textAlign = "center";

		    		var actions = row.insertCell(-1);
		    		var actions_button = document.createElement("button");
		    		if(response.data[i].active){
		    			actions_button.appendChild(document.createTextNode("Block"));
		    			actions_button.onclick = function(){
		    				blockAccess(this.parentNode.parentNode, true);
		    			}
		    		}else{
		    			actions_button.appendChild(document.createTextNode("Unblock"));
		    			actions_button.onclick = function(){
							blockAccess(this.parentNode.parentNode, false);
		    			}
		    		}
		    		actions.style.textAlign = "center";
		    		actions.appendChild(actions_button);
		    	}

		    	table.replaceChild(new_tbody, old_tbody);
		    }
		    else
		    {
		    	alert(response.errno + ": " + response.msg);
		    }
	    }
	);
}

function blockAccess(row, block){
	if(!confirm("Are you sure you want to modify " + row.id + "'s access?")){
		return;
	}
	var URL = "/administrator/controlAccess";
	var data = {
		"username": row.id,
		"freeze": block
	};
	console.log(JSON.stringify(data));
	$.post(URL, JSON.stringify(data), function(response)
	    {
	    	if(response.errno==0)
    		{
		    	populateUserTable();
		    }
		    else
		    {
		    	alert(response.errno + ": " + response.msg);
		    }
	    }
	);
}