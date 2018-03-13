var name=sessionStorage.getItem('firstName') + ' ' + sessionStorage.getItem('lastName');
var email=sessionStorage.getItem('email');
var username=sessionStorage.getItem('username');
var telNum=sessionStorage.getItem('telNum');

var html=
"<tr>" +
	'<td>'+ "Username" + '</td><td>:</td><td>' + username +'</td></tr>' +
"</tr>" +
"<tr>" +
	'<td>'+ "Email" + '</td><td>:</td><td>' + email +'</td></tr>' +
"</tr>" +
"<tr>" +
	'<td>'+ "Mobile Number" + '</td><td>:</td><td>' + telNum +'</td></tr>' +
"</tr>";

document.getElementById('name').innerHTML=name;
document.getElementById('info').innerHTML=html;

document.getElementById('calendar').innerHTML='<object type="text/html" data="calendarDisplay.html" width="100%" height="100%"></object>';