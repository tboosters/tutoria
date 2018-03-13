var selectedTutor=JSON.parse(sessionStorage.getItem("selectedTutor"));

var selected= new Array(24*7); //avalible=0, blacked out=1, booked=2
var nextWeek=0;


var today=new Date();
today.setHours(today.getHours()+24);
var endDate=new Date(today);
endDate.setDate(endDate.getDate()+6);
var t=Math.ceil(Math.abs(today - START_DATE) / 36e5);
console.log("T: " + t);

function createTimeTable()
{
    var timeTable='';
    var hr, min;
    var time=12;
    var ampm='a';

    console.log(selected);

    for(var i=0; i<24; i++)
    {
        timeTable=timeTable+'<tr><th class="time">'+ time + ampm +'</th>';
        for(var j=0; j<7; j++)
        {
            hr=i;
            min=0;
            var tempDate=new Date(START_DATE);
            tempDate.setDate(START_DATE.getDate()+j);
            tempDate.setHours(START_DATE.getHours()+hr);
            tempDate.setMinutes(START_DATE.getMinutes()+min);

            if(tempDate>today && tempDate<endDate)
            {
                timeTable=timeTable+'<td id="'+ dates[j] + '_' + hr + '_' + min + '"';
                if(selected[i+j*24-t + 24 + 168*nextWeek]==0)
                {
                    timeTable=timeTable+' style="background: DODGERBLUE" ' +
                                        'onclick="onSelect(this)" onmouseover="onSelectMouseOver(this)" onmouseleave="onSelectMouseLeave(this)">Select';
                }
                else if(selected[i+j*24-t + 24 + 168*nextWeek]==1)
                {
                    timeTable=timeTable+' style="background: GREY">Blacked Out';
                }
                else if(selected[i+j*24-t + 24 + 168*nextWeek]==2)
                {
                    timeTable=timeTable+' style="background: RED">Booked';
                }
                else
                {
                    timeTable=timeTable+'">';
                }
                timeTable=timeTable+'</td>';   
            }
            else
            {
                timeTable=timeTable+'<td></td>';
            }
        }
        timeTable=timeTable+'</tr>';

        time=time===12? 1 : time+1;
        if(time===12)
        {
            ampm='p';
        }
    }

    document.getElementById('timeTable').innerHTML=timeTable;
}

function loadTimeSlot()
{
    var URL="../account/availableTimes";
    var data={'csrfmiddlewaretoken':"{{ csrf_token }}", 'tutor_id': selectedTutor.tutor_id};
    $.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            selected=response.data.availableTimes;
            createTimeTable();
        }
        else
        {
            alert(response.errno + ": " + response.msg);
            //update page
        }
    });
}

loadTimeSlot();

//add listener to the next and previous key
var week=0; //0: displaying current week; 1: displaying the next week
document.getElementById("prev").addEventListener("click", function(e) {
    if(week===1)
    {
        START_DATE.setDate(START_DATE.getDate()-7);
        nextWeek=0;
        createDayTable();
        createTimeTable();
        week--;
        t=Math.floor(((Math.abs(today - START_DATE) % 86400000) % 3600000) / 60000 /30);
    }
});

document.getElementById("next").addEventListener("click", function(e) {
    if(week===0)
    {
        START_DATE.setDate(START_DATE.getDate()+7);
        nextWeek=1;
        createDayTable();
        createTimeTable();
        week++;
        t=Math.floor(((Math.abs(today - START_DATE) % 86400000) % 3600000) / 60000 /30);
    }
});