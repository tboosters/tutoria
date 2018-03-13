var selected = new Array(48*7);
var selected2;

function loadTimeSlot()
{
    var URL="../booking/listBookings";
    console.log(sessionStorage.getItem('isTutor'));
    console.log(sessionStorage.getItem('isStudent'));
    var data={"is_tutor": JSON.parse(sessionStorage.getItem('isTutor')), "is_student": JSON.parse(sessionStorage.getItem('isStudent'))};
    $.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            if(!(sessionStorage.getItem('tutorType') == 'undefined' || sessionStorage.getItem('tutorType') == null || sessionStorage.getItem('tutorType')=="")) //is a tutor
            {
                var URL="availableTimes";
                var data={'csrfmiddlewaretoken':"{{ csrf_token }}", 'tutor_id': sessionStorage.getItem('tutorID')};
                $.post(URL, JSON.stringify(data), function(response2)
                {
                    if(response2.errno==0)
                    {
                        //response.data.availableTimes 0: avalible; 1 blacked out; 2: booked
                        buildCalendar(response.data.bookings_as_student, response.data.bookings_as_tutor, response2.data.availableTimes);
                    }
                    else
                    {
                        alert(response.errno + ": " + response2.msg);
                    }
                });
            }
            else
            {
                buildCalendar(response.data.bookings_as_student, null, null);  
            }
        }
        else
        {
            alert(response.errno + ": " + response.msg);
            //update page
        }
    });
}

var nextWeek=0;

var today=new Date();
today.setHours(today.getHours()+24);
var endDate=new Date(today);
endDate.setDate(endDate.getDate()+6);
var t;
if(sessionStorage.getItem("tutorType")=="contracted")
{
    t=Math.ceil(Math.abs(today - START_DATE) / (36e5/2));
}
else
{
    t=Math.ceil(Math.abs(today - START_DATE) / 36e5);
}

function buildCalendar(dataStudent, dataTutor, tutorBooking)
{
    selected=dataStudent;
    selected2=dataTutor;

    var timeTable='';
    var hr, min;
    var time=12;
    var ampm='a';

    var nextRow=[0,0,0,0,0,0,0];
    var k=0;
    for(var i=0; i<48; i++)
    {
        if(i%2===0)
        {
            timeTable=timeTable+'<tr><th class="time" rowspan="2">'+ time + ampm +'</th>';
        }
        else
        {
            timeTable=timeTable+'<tr>';
        }

        for(var j=0; j<7; j++)
        {
            hr=parseInt(i/2);
            min=i%2*30;
            if(i>=nextRow[j])
            {
                timeTable=timeTable+'<td id="'+ dates[j] + '_' + hr + '_' + min;

                var tempDate=new Date(START_DATE);
                tempDate.setDate(START_DATE.getDate()+j);
                tempDate.setHours(START_DATE.getHours()+hr);
                tempDate.setMinutes(START_DATE.getMinutes()+min);


                var done=false;
                if(selected!=null && selected.length!=0 && !done)
                {
                    var dateTime=dates[j].split('_');
                    var thisDateTemp=new Date(dateTime[2], dateTime[1]-1, dateTime[0], hr, min, 0, 0);
                    // if(dateTemp.getDate()==dateTime[0] && dateTemp.getMonth()+1==dateTime[1] && dateTemp.getFullYear()==dateTime[2] && dateTemp.getHours()==hr && dateTemp.getMinutes()==min)
                    k = isBooked(thisDateTemp, selected);
                    if(k != -1)
                    {
                        console.log(thisDateTemp);
                        timeTable=timeTable+'_' + selected[k].id + '"' + ' style="background: DODGERBLUE" ' +
                                        'onclick="onView(this, ' + k + ')" onmouseover="onSelectMouseOver(this)" onmouseleave="onSelectMouseLeave(this)"';

                       if(selected[k].tutor_type=='private')
                       {
                            timeTable=timeTable + ' rowspan=2';
                            nextRow[j]=i+2;
                       }

                       timeTable=timeTable + '>View';
                       done=true;
                       console.log("test");
                    }
                }
                
                if(dataTutor!=null && dataTutor.length!=0 && !done)
                {
                    var dateTime=dates[j].split('_');
                    var thisDateTemp=new Date(dateTime[2], dateTime[1]-1, dateTime[0], hr, min, 0, 0);
                    // if(dateTemp.getDate()==dateTime[0] && dateTemp.getMonth()+1==dateTime[1] && dateTemp.getFullYear()==dateTime[2] && dateTemp.getHours()==hr && dateTemp.getMinutes()==min)
                    k = isBooked(thisDateTemp, dataTutor);
                    if(k != -1)
                    {
                        timeTable=timeTable+'_' + dataTutor[k].id + '"' + ' style="background: BLUE" ' +
                                        'onclick="onView2(this, ' + k + ')" onmouseover="onSelectMouseOver(this)" onmouseleave="onSelectMouseLeave(this)"';

                       if(sessionStorage.getItem('tutorType')=='private')
                       {
                            timeTable=timeTable + ' rowspan=2';
                            nextRow[j]=i+2;
                       }

                       timeTable=timeTable + '>Booked';
                       done=true;
                       console.log("test2");
                    }
                }

                if(tempDate>today && tempDate<endDate && !done)
                {
                    if(sessionStorage.getItem('tutorType')=='private' && min==0)
                    {
                        if(tutorBooking[Math.round(i/2+j*24-t + 24 + 168*nextWeek)]==0)
                        {
                            timeTable=timeTable+'" style="background: LIGHTBLUE" rowspan=2 onmouseover="onBlackOutHover(this)" onmouseover="onBlackOutLeave(this) onclick="onDisableClick()">avalible';
                        }
                        else if(tutorBooking[Math.round(i/2+j*24-t + 24 + 168*nextWeek)]==1)
                        {
                            timeTable=timeTable+'" style="background: GREY" rowspan=2 onmouseover="onBlackOutHover(this)" onmouseover="onBlackOutLeave(this) onclick="onEnableClick()">Blacked Out';
                        }
                        else
                        {
                            timeTable=timeTable+'" rowspan=2>';
                        }
                        nextRow[j]=i+2;
                        done=true;
                    }
                    else if(sessionStorage.getItem('tutorType')=='contracted')
                    {
                        if(tutorBooking[i+j*48-t + 48 + 336*nextWeek]==0)
                        {
                            timeTable=timeTable+'" style="background: LightBLUE" onmouseover="onBlackOutHover(this)" onmouseover="onBlackOutLeave(this) onclick="onDisableClick()">avalible';
                        }
                        else if(tutorBooking[i+j*48-t + 48 +  336*nextWeek]==1)
                        {
                            timeTable=timeTable+'" style="background: GREY" onmouseover="onBlackOutHover(this)" onmouseover="onBlackOutLeave(this) onclick="onEnableClick()">Blacked Out';
                        }
                        else
                        {
                            timeTable=timeTable+'">';
                        }
                        done=true;
                    }
                }

                if(!done)
                {
                    timeTable=timeTable+'">';
                }

                timeTable=timeTable+'</td>';
            }
        }

        timeTable=timeTable+'</tr>';

        if(i%2===1)
        {
            time=time===12? 1 : time+1;
            if(time===12)
            {
                ampm='p';
            }
        }
    }

    document.getElementById('timeTable').innerHTML=timeTable;
}

function onBlackOutHover(cell)
{
    cell.style.background="grey";
}

function onBlackOutLeave(cell)
{
    cell.style.background="lightblue";
}

function onDisableClick(cell)
{
    var dateTime=cell.getAttribute('id').split('_');

    var startDate=new Date(parseInt(dateTime[2]), parseInt(dateTime[1])-1, parseInt(dateTime[0]));
    startDate.setHours(parseInt(dateTime[3]), parseInt(dateTime[4]));


    var URL="disableTimeSlot";
    var data={'csrfmiddlewaretoken':"{{ csrf_token }}", "start_time": startDate, "end_time": ""};
    $.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            loadTimeSlot();
        }
    });
}

function onEnableClick(cell)
{
    
    var startDate=new Date(parseInt(dateTime[2]), parseInt(dateTime[1])-1, parseInt(dateTime[0]));
    startDate.setHours(parseInt(dateTime[3]), parseInt(dateTime[4]));


    var URL="enableTimeSlot";
    var data={'csrfmiddlewaretoken':"{{ csrf_token }}", "start_time": startDate, "end_time": ""};
    $.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            loadTimeSlot();
        }
    });

}

function isBooked(thisDateTemp, list){
    var k = -1;
    for(var i = 0; i < list.length; i++){
        var dateTemp = new Date(list[i].start_time);
        dateTemp.setHours(dateTemp.getHours());
        if(thisDateTemp.getTime() === dateTemp.getTime()){
            k = i;
            break;
        }
    }
    return k;
}

loadTimeSlot();

function onView(cell, k)
{
    bookingID = selected[k].id;
    tutorID = selected[k].tutor_id;
    tutorType = selected[k].tutor_type;
    tutoringFee = selected[k].fee;
    university = selected[k].tutor_university;
    email = selected[k].tutor_email;
    tel = selected[k].tutor_phone_number;
    startDate = new Date(selected[k].start_time);
    endDate = new Date(selected[k].end_time);

    sessionStorage.setItem("isSearch", 0);
    sessionStorage.setItem('bookingID', bookingID);

    sessionStorage.setItem('tutor_first_name', selected[k].tutor_first_name);
    sessionStorage.setItem('tutor_last_name', selected[k].tutor_last_name);
    sessionStorage.setItem('tutorID', tutorID);
    sessionStorage.setItem('university', university);
    sessionStorage.setItem('tutorType', tutorType);
    sessionStorage.setItem('tutoringFee', tutoringFee);
    sessionStorage.setItem('tutorEmail', email);
    sessionStorage.setItem('tutorTelNum', tel);

    // sessionStorage.setItem('startDate', startDate);
    // sessionStorage.setItem('endDate', endDate);

    // var dateTime=cell.getAttribute('id').split('_');

    // sessionStorage.setItem('bookingID', dateTime[5]);

    // startDate=new Date(parseInt(dateTime[2]), parseInt(dateTime[1])-1, parseInt(dateTime[0]));
    // startDate.setHours(parseInt(dateTime[3]), parseInt(dateTime[4]));

    // endDate=new Date(startDate);
    // if(tutorType==='Contracted')
    // {
    //     endDate.setMinutes(endDate.getMinutes()+30);
    // }
    // else
    // {
    //     endDate.setHours(endDate.getHours()+1);
    // }

    sessionStorage.setItem('startDate', startDate.getDate() + ' ' + months[startDate.getMonth()] + ' ' + startDate.getFullYear() + ' ' +
                            ("0" + startDate.getHours()).slice(-2) + ':' + ("0" + startDate.getMinutes()).slice(-2));
    sessionStorage.setItem('endDate', endDate.getDate() + ' ' + months[endDate.getMonth()] + ' ' + endDate.getFullYear() + ' ' +
                            ("0" + endDate.getHours()).slice(-2) + ':' + ("0" + endDate.getMinutes()).slice(-2));
    window.open("../booking/bookingDetailsViewing.html", "", "width=900,height=600");
}


function onView2(cell, k)
{
    bookingID = selected2[k].id;
    startDate = new Date(selected2[k].start_time);
    endDate = new Date(selected2[k].end_time);

    sessionStorage.setItem("isSearch", 2);
    sessionStorage.setItem('bookingID', bookingID);

    sessionStorage.setItem('student_first_name', selected2[k].student_first_name);
    sessionStorage.setItem('student_last_name', selected2[k].student_last_name);
    sessionStorage.setItem('student_phone_number', selected2[k].student_phone_number);
    sessionStorage.setItem('student_email', selected2[k].student_email);

    sessionStorage.setItem('tutor_first_name', sessionStorage.getItem("firstName"));
    sessionStorage.setItem('tutor_last_name', sessionStorage.getItem("lastName"));
    sessionStorage.setItem('tutorID', sessionStorage.getItem("tutorID"));
    sessionStorage.setItem('university', sessionStorage.getItem("university"));
    sessionStorage.setItem('tutorType', sessionStorage.getItem("tutorType"));
    sessionStorage.setItem('tutoringFee', sessionStorage.getItem("tutoringFee"));
    sessionStorage.setItem('tutorEmail', sessionStorage.getItem("email"));
    sessionStorage.setItem('tutorTelNum', sessionStorage.getItem("telNum"));

    sessionStorage.setItem('startDate', startDate);
    sessionStorage.setItem('endDate', endDate);

    // startDate = new Date(selected[k].start_time);
    // endDate = new Date(selected[k].end_time);

    sessionStorage.setItem('startDate', startDate.getDate() + ' ' + months[startDate.getMonth()] + ' ' + startDate.getFullYear() + ' ' +
                            ("0" + startDate.getHours()).slice(-2) + ':' + ("0" + startDate.getMinutes()).slice(-2));
    sessionStorage.setItem('endDate', endDate.getDate() + ' ' + months[endDate.getMonth()] + ' ' + endDate.getFullYear() + ' ' +
                            ("0" + endDate.getHours()).slice(-2) + ':' + ("0" + endDate.getMinutes()).slice(-2));
    window.open("../booking/bookingDetailsViewing.html", "", "width=900,height=600");
}

//add listener to the next and previous key
var week=0; //0: displaying current week; 1: displaying the next week
document.getElementById("prev").addEventListener("click", function(e) {
    if(week===1)
    {
        START_DATE.setDate(START_DATE.getDate()-7);
        createDayTable();
        loadTimeSlot();
        week--;
        nextWeek=0;
    }
});

document.getElementById("next").addEventListener("click", function(e) {
    if(week===0)
    {
        START_DATE.setDate(START_DATE.getDate()+7);
        createDayTable();
        loadTimeSlot();
        week++;
        nextWeek=1;
    }
});