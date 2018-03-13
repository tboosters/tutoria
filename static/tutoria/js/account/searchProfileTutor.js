var selectedTutor=JSON.parse(sessionStorage.getItem("selectedTutor"));

console.log(selectedTutor);

var html=
"<tr>" +
	"<td><h1>" + selectedTutor.first_name + " " + selectedTutor.last_name + "</h1></td>" +
"</tr>" +
"<tr>" +
	"<td>@" + selectedTutor.tutor_id + "</td>" +
"</tr>" +
"<tr>" +
	"<td>" + selectedTutor.university + "</td>" +
"</tr>" +
"<tr>" +
	"<td>" + selectedTutor.email + "</td>" +
"</tr>" +
"<tr>" +
	"<td>";

	for(var i=0; i<selectedTutor.tag.length; i++)
	{
		html=html+selectedTutor.tag[i];
	}
	
	html=html+"</td>" +
"</tr>";

var html2="";
if(selectedTutor.hourly_rate==0)
{
	
}


document.getElementById('info').innerHTML=html;

sessionStorage.setItem("isSearch", 1);
document.getElementById('tabs').innerHTML='<object type="text/html" data="tutorTabs.html" width="100%" height="100%"></object>';