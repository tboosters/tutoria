var isSearch=sessionStorage.getItem('isSearch');

function openInfo(evt, name)
{
    var i, tabContent, tabLinks;
    tabContent=document.getElementsByClassName('tabContent');
    for (i = 0; i < tabContent.length; i++)
    {
        tabContent[i].style.display='none';
    }

    tabLinks=document.getElementsByClassName('tabLinks');
    for (i = 0; i < tabLinks.length; i++)
    {
        tabLinks[i].className = tabLinks[i].className.replace(' active', '');
    }

    document.getElementById(name).style.display = "block";
    evt.currentTarget.className += ' active';
}


function loadCalendar()
{
    if(isSearch==1)
    {
        var selectedTutor=JSON.parse(sessionStorage.getItem("selectedTutor"));
        if(selectedTutor.tutor_type=='contracted')
        {
            console.log("contracted");
            document.getElementById('Calendar').innerHTML='<object type="text/html" data="searchCalendarContracted.html" width="100%" height="100%"></object>';
        }
        else
        {
            console.log("private");
            document.getElementById('Calendar').innerHTML='<object type="text/html" data="searchCalendarPrivate.html" width="100%" height="100%"></object>';   
        }
        sessionStorage.setItem('isSearch', 0);
    }
    else
    {
        document.getElementById('Calendar').innerHTML='<object type="text/html" data="calendarDisplay.html" width="100%" height="100%"></object>';
    }
};

function showReview(){
    if(sessionStorage.getItem("selectedTutor") == null){
        document.getElementById("requestReview_button").style.display = "none";
    }
    showReviewEntries();
}

showReview()
loadCalendar();
document.getElementById('defaultOpen').click();