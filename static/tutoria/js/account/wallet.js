function onWallet(){
	document.getElementById('content').setAttribute('src', "../wallet");
}

function getActions(){
	var isStudent = JSON.parse(sessionStorage.getItem("isStudent"));
	var isTutor = JSON.parse(sessionStorage.getItem("isTutor"));
	var actions = document.getElementById("wallet_actions");
	if(isStudent){
		var addValue = document.createElement("button");
		actions.appendChild(addValue);
		addValue.appendChild(document.createTextNode("Add Value"));
		addValue.onclick = function(){
			showAddValue();
		};
	}
	if(isTutor || (!isTutor && !isStudent)){
		var transfer = document.createElement("button");
		actions.appendChild(transfer);
		transfer.appendChild(document.createTextNode("Transfer Money"));
		transfer.onclick = function(){
			showTransferMoney();
		}
	}
}

function getWallet(){
	var URL = "/wallet/balance";
	$.post(URL, null, function(response)
	    {
	    	if(response.errno==0)
    		{
		    	var balance = document.getElementById("wallet_balance");
		    	balance.innerHTML = response.data.balance;
		    }
		    else
		    {
		    	alert(response.errno + ": " + response.msg);
		    }
	    }
	);
}

function getTransactions(){
	var URL = "/wallet/transactions";
	var data = {
		"days": 30
	};
	$.post(URL, JSON.stringify(data), function(response)
	    {
	    	if(response.errno==0)
    		{
    			var table = document.getElementById("transaction_table");
    			var old_tbody = table.getElementsByTagName("tbody")[0];
    			var new_tbody = document.createElement("tbody");

    			for(var i = 0; i < response.data.length; i++){
    				var transaction = response.data[i];
    				var row = new_tbody.insertRow(-1);

    				var time = row.insertCell(-1);
    				var time_data = transaction.time;
    				time_processed = time_data.substring(0, 10) + " " + time_data.substring(11, 19);
    				time.innerHTML = time_processed;
    				time.style.textAlign = "center";

    				var amount = row.insertCell(-1);
    				amount.innerHTML = transaction.amount;
    				amount.style.textAlign = "center";

    				var details = row.insertCell(-1);
    				details.innerHTML = transaction.detail;
    				details.style.textAlign = "center";
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

function showAddValue(){
	document.getElementById("addValueModal").style.display = "block";
}

function closeAddValue(){
	document.getElementById("addValueModal").style.display = "none";
}

function addValue(){
	var formData = new FormData(document.getElementById("addValueForm"));
	var URL = "/wallet/addValue";
	var data = {
		"amount": parseInt(formData.get("amount"))
	};
	$.post(URL, JSON.stringify(data), function(response)
	    {
	    	if(response.errno==0)
    		{
    			getWallet();
    			getTransactions();
    			document.getElementById("addValueForm").reset()
    			closeAddValue();
		    }
		    else
		    {
		    	alert(response.errno + ": " + response.msg);
		    }
	    }
	);
}

function showTransferMoney(){
	document.getElementById("transferMoneyModal").style.display = "block";
}

function closeTransferMoney(){
	document.getElementById("transferMoneyModal").style.display = "none";
}

function transferMoney(){
	var isStudent = JSON.parse(sessionStorage.getItem("isStudent"));
	var isTutor = JSON.parse(sessionStorage.getItem("isTutor"));

	var formData = new FormData(document.getElementById("transferMoneyForm"));
	var URL = "";
	if(isTutor){
		URL = "/wallet/tutorTransfer";
	}else if(!isTutor && !isStudent){
		URL = "/wallet/myTutorTransfer";
	}
	var data = {
		"amount": parseInt(formData.get("amount"))
	};
	$.post(URL, JSON.stringify(data), function(response)
	    {
	    	if(response.errno==0)
    		{
    			getWallet();
    			getTransactions();
    			document.getElementById("transferMoneyForm").reset()
    			closeTransferMoney();
		    }
		    else
		    {
		    	alert(response.errno + ": " + response.msg);
		    }
	    }
	);
}