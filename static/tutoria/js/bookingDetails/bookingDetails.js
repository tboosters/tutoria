var start=new Date();

var name=sessionStorage.getItem('firstName') + ' ' + sessionStorage.getItem('lastName');
var username=sessionStorage.getItem('username');
var userID=parseInt(sessionStorage.getItem('userID'));
var email=sessionStorage.getItem('email');
var telNum=sessionStorage.getItem('telNum');

var isSearch=sessionStorage.getItem("isSearch");
var detailsInfo=new Array(11);
if(isSearch==1)
{
    var selectedTutor=JSON.parse(sessionStorage.getItem("selectedTutor"));
    console.log(selectedTutor); 

    detailsInfo=[name, email, telNum, selectedTutor.first_name + " " + selectedTutor.last_name, selectedTutor.tutor_id, selectedTutor.university, 
                    selectedTutor.tutor_type, '$'+selectedTutor.hourly_rate, selectedTutor.email, "N/A",
        sessionStorage.getItem('startDate'), sessionStorage.getItem('endDate')];
}
else if(isSearch==0)
{
    detailsInfo=[name, email, telNum, sessionStorage.getItem('tutor_first_name') + " " + sessionStorage.getItem('tutor_last_name'), sessionStorage.getItem('tutorID'), sessionStorage.getItem('university'), 
                    sessionStorage.getItem('tutorType'), '$'+sessionStorage.getItem('tutoringFee'), sessionStorage.getItem('tutorEmail'), sessionStorage.getItem('tutorTelNum'),
        sessionStorage.getItem('startDate'), sessionStorage.getItem('endDate')];
}
else if(isSearch==2)
{
    detailsInfo=[sessionStorage.getItem("student_first_name") + " " + sessionStorage.getItem("student_last_name"), 
                sessionStorage.getItem("student_email"), sessionStorage.getItem("student_phone_number"), 
                sessionStorage.getItem('tutor_first_name') + " " + sessionStorage.getItem('tutor_last_name'), 
                sessionStorage.getItem('tutorID'), sessionStorage.getItem('university'), 
                sessionStorage.getItem('tutorType'), '$'+sessionStorage.getItem('tutoringFee'), 
                sessionStorage.getItem('tutorEmail'), sessionStorage.getItem('tutorTelNum'),
                sessionStorage.getItem('startDate'), sessionStorage.getItem('endDate')];
}

var startDateUTC=sessionStorage.getItem('startDateUTC');
var endDateUTC=sessionStorage.getItem('endDateUTC');
function createDetailsTable()
{
    var detailsTable='';
    const detailsTitle=['Student Name', 'Student Email', 'Student Telephone Number',
                    'Tutor Name', 'Tutor ID', 'University', 'Tutor Type', 'Tutoring Fee', 'Tutor Email', 'Tutor Telephone Number',
                    'Tutorial Session Start', 'Tutorial Session End'];
    for(var i=0; i<detailsTitle.length; i++)
    {
            detailsTable=detailsTable+'<tr><td>'+ detailsTitle[i] + '</td><td>:</td><td>' + detailsInfo[i] +'</td></tr>';
    }
    document.getElementById('details').innerHTML=detailsTable;
}

createDetailsTable();

function refreshParent() 
{
    window.opener.location.reload(true);
}
window.onunload = refreshParent;