function requestReview(){
	var tutorID_json = JSON.parse(sessionStorage.getItem('selectedTutor'));
    var tutorID;
    if(tutorID_json == null){
        tutorID = sessionStorage.getItem('tutorID');
    }else{
        tutorID = tutorID_json.tutor_id;
    }
	console.log(tutorID);
	var URL = "/account/requestReview";
	var data = {
		"tutor_id": tutorID
	};

	$.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            document.getElementById("reviewModal").style.display = "block";
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }
    });
}

function closeReviewModal(){
	document.getElementById("reviewModal").style.display = "none";
}

function review(){
    var tutorID_json = JSON.parse(sessionStorage.getItem('selectedTutor'));
    var tutorID;
    if(tutorID_json == null){
        tutorID = sessionStorage.getItem('tutorID');
    }else{
        tutorID = tutorID_json.tutor_id;
    }
	var formData = new FormData(document.getElementById("reviewForm"));

	var URL = "/account/review";
	var data = {
		"tutor_id": tutorID,
		"is_anonymous": (formData.get("is_anonymous")=="on"),
		"stars": parseInt(formData.get("stars")),
		"comment": formData.get("comment")
	};

	$.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            alert("Review has been sent!");
            document.getElementById("reviewForm").reset();
            closeReviewModal();
            showReviewEntries();
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }
    });
}

function showReviewEntries(){
    var tutorID_json = JSON.parse(sessionStorage.getItem('selectedTutor'));
    var tutorID;
    if(tutorID_json == null){
        tutorID = sessionStorage.getItem('tutorID');
    }else{
        tutorID = tutorID_json.tutor_id;
    }
    var URL = "/account/listReview";
    var data = {
        "tutor_id": tutorID
    };

    $.post(URL, JSON.stringify(data), function(response)
    {
        if(response.errno==0)
        {
            var avg = document.getElementById("reviewEntries_avg");
            avg.innerHTML = response.data.average;

            var table = document.getElementById("reviewEntries_table");
            var old_tbody = table.getElementsByTagName("tbody")[0];
            var new_tbody = document.createElement("tbody");

            for(var i = 0; i < response.data.entries.length; i++){
                var row = new_tbody.insertRow(-1);

                var stars = row.insertCell(-1);
                stars.innerHTML = response.data.entries[i].stars;
                stars.style.textAlign = "center";

                var student = row.insertCell(-1);
                student.innerHTML = response.data.entries[i].student;
                student.style.textAlign = "center";

                var comment = row.insertCell(-1);
                comment.innerHTML = response.data.entries[i].comment;
                comment.style.textAlign = "center";
            }
            table.replaceChild(new_tbody, old_tbody);
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }
    });
}