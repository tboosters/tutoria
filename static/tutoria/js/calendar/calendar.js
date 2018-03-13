var studentName=sessionStorage.getItem('firstName') + ' ' + sessionStorage.getItem('lastName');
var studentEmail=sessionStorage.getItem('email');
var studnetUsername=sessionStorage.getItem('username');
var studentTelNum=sessionStorage.getItem('telNum');

var tutorName=sessionStorage.getItem('tutorFirstName') + ' ' + sessionStorage.getItem('tutorLastName');
var tutorUsername=sessionStorage.getItem('tutorUsername');
var tutorUserID=parseInt(sessionStorage.getItem('tutorUserID'));
var tutorEmail=sessionStorage.getItem('tutorEmail');
var tutorTelNum=sessionStorage.getItem('tutorTelNum');
var tutoringFee=sessionStorage.getItem('tutoringFee');
var tutorID=sessionStorage.getItem('tutorID');
var tutorType=sessionStorage.getItem('tutorType');
var university=sessionStorage.getItem('university');

var months = ['January','February','March','April','May','June','July',
    'August','September','October','November','December'];
var today = new Date();
document.getElementById("spanMonthAndYear").innerHTML=months[today.getMonth()]+ ' ' + today.getFullYear();

//display all 7 dates of the current week
var start=0;
var day = today.getDay() - start;
var date = today.getDate() - day;

var START_DATE=new Date(today.setDate(date));
START_DATE.setHours(0);
START_DATE.setMinutes(0);
START_DATE.setSeconds(0);
var dates=new Array(7);
function createDayTable()
{
    var dayTable='<tr><th class="emptyCell"></th>';
    var tempDate=new Date(START_DATE);
    for(var i=0; i<7; i++)
    {
        dayTable=dayTable+'<th>'+tempDate.getDate();
        dates[i]=tempDate.getDate();
        if(tempDate.getDate()===1)
        {
            dayTable=dayTable+'/'+(tempDate.getMonth()+1);
        }
        dates[i]=dates[i]+'_'+(tempDate.getMonth()+1)+'_' + tempDate.getFullYear();
        dayTable=dayTable+'</th>';
        tempDate.setDate(tempDate.getDate()+1);
    }

    dayTable=dayTable+'</tr>';
    document.getElementById('days').innerHTML=dayTable;
}

createDayTable();

var startDate;
var endDate;
//select time slot
function onSelect(cell)
{
    sessionStorage.setItem('studentName', studentName);
    sessionStorage.setItem('studentEmail', studentEmail);
    sessionStorage.setItem('studentTelephoneNumber', studentTelNum);
    sessionStorage.setItem('tutorName', tutorName);
    sessionStorage.setItem('tutorID', tutorID);
    sessionStorage.setItem('university', university);
    sessionStorage.setItem('tutorType', tutorType);
    sessionStorage.setItem('tutoringFee', tutoringFee);
    sessionStorage.setItem('tutorEmail', tutorEmail);
    sessionStorage.setItem('tutorTelephoneNumber', tutorTelNum);

    sessionStorage.setItem("isSearch", 1);

    var dateTime=cell.getAttribute('id').split('_');

    startDate=new Date(parseInt(dateTime[2]), parseInt(dateTime[1])-1, parseInt(dateTime[0]));
    startDate.setHours(parseInt(dateTime[3]), parseInt(dateTime[4]));
    endDate=new Date(startDate);
    if(tutorType=='contracted')
    {
        endDate.setMinutes(endDate.getMinutes()+30);
    }
    else
    {
        endDate.setHours(endDate.getHours()+1);
    }

    sessionStorage.setItem('startDate', startDate.getDate() + ' ' + months[startDate.getMonth()] + ' ' + startDate.getFullYear() + ' ' +
                            ("0" + startDate.getHours()).slice(-2) + ':' + ("0" + startDate.getMinutes()).slice(-2));
    sessionStorage.setItem('endDate', endDate.getDate() + ' ' + months[endDate.getMonth()] + ' ' + endDate.getFullYear() + ' ' +
                            ("0" + endDate.getHours()).slice(-2) + ':' + ("0" + endDate.getMinutes()).slice(-2));
    sessionStorage.setItem('startDateUTC', startDate);
    sessionStorage.setItem('endDateUTC', endDate);
    window.open("../booking/bookingDetailsRequestConfirm.html", "", "width=900,height=600");
}

function onSelectMouseOver(cell)
{
    cell.style.color="#666";
}

function onSelectMouseLeave(cell)
{
    cell.style.color="white";
}