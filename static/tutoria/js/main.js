function onLogin()
{
	var URL="login";
    var data={'csrfmiddlewaretoken':"{{ csrf_token }}", "username": document.getElementById("username").value, "password": document.getElementById("password").value};
    $.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            //window.open('../booking/bookingDetailsConfirmed.html',"_self");
            $.post("account/accountProfile", JSON.stringify(data), function(response2)
		    {
		    	if(response2.errno==0)
        		{
			    	sessionStorage.setItem('firstName', response2.data.firstName);
		            sessionStorage.setItem('lastName', response2.data.lastName);
		            sessionStorage.setItem('username', response2.data.username);
		            sessionStorage.setItem('email', response2.data.email);
		            sessionStorage.setItem('telNum', response2.data.telNum);

		            sessionStorage.setItem('tutorType', response2.data.tutorType);
		            sessionStorage.setItem('tutorID', response2.data.tutorID);
		            sessionStorage.setItem('tutoringFee', response2.data.tutorFee);
		            sessionStorage.setItem('university', response2.data.university);
		            sessionStorage.setItem('searchable', response2.data.searchable);
		            sessionStorage.setItem('courseTag', JSON.stringify(response2.data.courseTag));
		            sessionStorage.setItem('subjectTag', JSON.stringify(response2.data.subjectTag));

					sessionStorage.setItem('isStudent', JSON.stringify(response2.data.is_student));
					isStudent = response2.data.is_student;
					sessionStorage.setItem('isTutor', JSON.stringify(response2.data.is_tutor));
					isTutor = response2.data.is_tutor;
					window.location.href='account/account.html';
			    }
			    else
			    {
			    	alert(response2.errno + ": " + response2.msg);
			    }
		    });
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }
    });
}

function isTutor(checkbox)
{
	if(checkbox.checked == true){
        document.getElementById("tutor1").style.display = "block";
        document.getElementById("tutor2").style.display = "block";
    }else{
        document.getElementById("tutor1").style.display = "none";
        document.getElementById("tutor2").style.display = "none";
   }
}

function onSignUp()
{
	var URL="signup";
	var data={'csrfmiddlewaretoken':"{{ csrf_token }}", 
			"username": document.getElementById("usernameIn").value, 
			"password1": document.getElementById("password1").value, 
			"password2": document.getElementById("password2").value, 
			"first_name": document.getElementById("firstname").value, 
			"last_name": document.getElementById("lastname").value, 
			"phone_number": document.getElementById("mobile").value, 
			"is_student": document.getElementById("student").checked, 
			"is_tutor": document.getElementById("tutor").checked, 
			"is_contracted": document.getElementById("contractedTutor").checked, 
			"is_private": document.getElementById("privateTutor").checked, 
			"tutor_id": document.getElementById("tutorID").value, 
			"university": document.getElementById("university").value,
			"hourly_rate": document.getElementById("hourlyRate").value,
			"email": document.getElementById("email").value
		};

	$.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
        	sessionStorage.setItem('firstName', document.getElementById("firstname").value);
            sessionStorage.setItem('lastName', document.getElementById("lastname").value);
            sessionStorage.setItem('username', document.getElementById("usernameIn").value);
            sessionStorage.setItem('email', document.getElementById("email").value);
            sessionStorage.setItem('telNum', document.getElementById("mobile").value);

            sessionStorage.setItem('tutorType', "");
            sessionStorage.setItem('tutorID', document.getElementById("tutorID").value);
            sessionStorage.setItem('tutoringFee', document.getElementById("hourlyRate").value);
            sessionStorage.setItem('university', document.getElementById("university").value);
            sessionStorage.setItem('isStudent', JSON.stringify(document.getElementById("student").checked));
			sessionStorage.setItem('isTutor', JSON.stringify(document.getElementById("tutor").checked));
	        window.location.href='account/account.html';
        }
        else
        {
        	alert(response.errno + ": " + response.msg);
        }	
    });	
}

function forgotPassword()
{
	window.location.href="forgotPassword.html";
}