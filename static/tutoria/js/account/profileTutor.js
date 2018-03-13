var name=sessionStorage.getItem('firstName') + ' ' + sessionStorage.getItem('lastName');
var email=sessionStorage.getItem('email');
var username=sessionStorage.getItem('username');
var telNum=sessionStorage.getItem('telNum');

var tutorID= sessionStorage.getItem('tutorID');
var tutorType= sessionStorage.getItem('tutorType');
var tutoringFee= sessionStorage.getItem('tutoringFee');
var university=sessionStorage.getItem('university');
var tutoringFee=sessionStorage.getItem('tutoringFee');
var courseTag=JSON.parse(sessionStorage.getItem('courseTag'));
var subjectTag=JSON.parse(sessionStorage.getItem('subjectTag'));

var html=
"<tr>" +
	'<td>'+ "Tutor ID" + '</td><td>:</td><td>' + "@" + tutorID +'</td>' +
"</tr>" +
"<tr>" +
	'<td>'+ "Username" + '</td><td>:</td><td>' + username +'</td>' +
"</tr>" +
"<tr>" +
	'<td>'+ "Email" + '</td><td>:</td><td>' + email +'</td>' +
"</tr>" +
"<tr>" +
	'<td>'+ "Mobile Number" + '</td><td>:</td><td>' + telNum +'</td>' +
"</tr>" +
"<tr>" +
	'<td>'+ "Courses" + '</td><td>:</td><td>';
	for(var i=0; i<courseTag.length; i++)
	{
		html=html+courseTag[i].name + ' ';
	}
	html=html+"</td>" +
"</tr>" +
"<tr>" +
	'<td>'+ "Subject Tag" + '</td><td>:</td><td>';
	for(var i=0; i<subjectTag.length; i++)
	{
		html=html+"#" +subjectTag[i].name + ' ';
	}
	html=html+"</td>" +
"</tr>";


document.getElementById('name').innerHTML=name;
document.getElementById('tutorType').innerHTML=tutorType=="contracted"? "Contracted Tutor" : "Private Tutor";
document.getElementById('hourlyRate').innerHTML=tutoringFee==0? "Free of Charge" : "$"+tutoringFee;
document.getElementById('info').innerHTML=html;


sessionStorage.setItem("isSearch", 0);
document.getElementById('tabs').innerHTML='<object type="text/html" data="tutorTabs.html" width="100%" height="100%"></object>';