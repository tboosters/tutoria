var name=sessionStorage.getItem('firstName') + ' ' + sessionStorage.getItem('lastName');
var username=sessionStorage.getItem('username');
var userID=parseInt(sessionStorage.getItem('userID'));
var email=sessionStorage.getItem('email');
var telNum=sessionStorage.getItem('telNum');
var avatar=null;
var tutorType=sessionStorage.getItem('tutorType');
var isStudent = JSON.parse(sessionStorage.getItem('isStudent'));
var isTutor = JSON.parse(sessionStorage.getItem('isTutor'));

document.getElementById('title').textContent=name;

if(isStudent)
{
	document.getElementById('content').setAttribute('src', "profileStudent.html");
}
else if(isTutor)
{
	document.getElementById('content').setAttribute('src', "profileTutor.html");
}else{
    document.getElementById('content').setAttribute('src', "../administrator");
}


document.getElementById('content').onload = function() 
{
        document.getElementById('content').height=parseInt($(document).height())-62;
}



var content=document.getElementById('content');
var advancedSearch=document.getElementById('advancedSearch');
var advancedSearchShowing=false;	

function onEnterKeyPress()
{
    if(event.keyCode===13)
    {
        document.getElementById("searchButton").click();
    }
}

function onHomeSelected()
{
    window.location.href="account.html";
}

function showHideAdvancedSearch()
{
	if(!advancedSearchShowing)
	{
		advancedSearch.style.display="block";
		document.getElementById("showHideAdvancedSearch").textContent="hide advanced search";
	}
	else
	{
		advancedSearch.style.display="none";
		document.getElementById("showHideAdvancedSearch").textContent="show advanced search";
	}

	advancedSearchShowing=!advancedSearchShowing;
}

function onSearch()
{
	if(!(document.getElementById("search").value=="" && document.getElementById("university").value=="" && 
        document.getElementById("course").value=="" && document.getElementById("subjectTag").value=="" &&
        document.getElementById("priceFrom").value=="" && document.getElementById("priceTo").value=="" &&
        document.getElementById("contractedTutor").checked==false && document.getElementById("privateTutor").checked==false &&
        document.getElementById("timeSlotAvailable").checked==false))
    {
        var URL="../search/searchadvance";
        var data={'csrfmiddlewaretoken':"{{ csrf_token }}", "name": document.getElementById("search").value, "university": document.getElementById("university").value, 
                    "courses": document.getElementById("course").value.split(" "), "tags": document.getElementById("subjectTag").value.split(" "), 
                    "price_range": [document.getElementById("priceFrom").value, document.getElementById("priceTo").value], 
                    'tutor_type': [document.getElementById("contractedTutor").checked, document.getElementById("privateTutor").checked],
                    'seven_days': document.getElementById("timeSlotAvailable").checked};

        $.post(URL, JSON.stringify(data), function(response)
        {
            if(response.errno==0)
            {
                sessionStorage.setItem("searchResult", JSON.stringify(response.data));
                document.getElementById('content').setAttribute('src', "../search/searchResult.html");
                advancedSearchShowing=true;
                showHideAdvancedSearch();
            }
            else
            {
                alert(response.errno + ": " + response.msg);
            }
        });
    }
    else
    {
        alert("Please enter at least 1 searching criteria");
    }
}

function onSetting()
{
    document.getElementById('content').setAttribute('src', "profileSetting.html");
}