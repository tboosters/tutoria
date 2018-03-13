var tutorType=sessionStorage.getItem('tutorType');

// var html="<tr>" + 
//             "<td>First name:</td>" + 
//             "<td><input type='text' id='firstName' value=" + sessionStorage.getItem('firstName') + "></td>" + 
//         "</tr>" + 
//         "<tr>" + 
//             "<td>Last name:</td>" + 
//             "<td><input type='text' id='lastName' value=" + sessionStorage.getItem('lastName') + "></td>" + 
//         "</tr>" + 
//         "<tr>" + 
//             "<td>Contact email address:</td>" + 
//             "<td><input type='email' id='email' value=" + sessionStorage.getItem('email') + "></td>" + 
//         "</tr>" + 
//         "<tr>" + 
//             "<td>Contact phone number:</td>" + 
//             "<td><input type='text' id='phone' value=" + sessionStorage.getItem('telNum') + "></td>" + 
//         "</tr>";
document.getElementById('firstName').value = sessionStorage.getItem('firstName');
document.getElementById('lastName').value = sessionStorage.getItem('lastName');
document.getElementById('email').value = sessionStorage.getItem('email');
document.getElementById('phone').value = sessionStorage.getItem('telNum');

if(!(tutorType == 'undefined' || tutorType == null || tutorType=="")) //isTutor
{
    var table = document.getElementById('setting');

    // Get course list
    var URL = "/account/getCourses"
    var courses_list = [];
    var tutor_courses = JSON.parse(sessionStorage.getItem('courseTag'));
    $.post(URL, null, function(response)
    {
        if(response.errno==0)
        {
            courses_list = response.data;

            var courses = table.insertRow(-1);
            var courses_desc = courses.insertCell(-1);
            courses_desc.innerHTML = "Teaching courses (course code):";
            var courses_select_cell = courses.insertCell(-1);
            var courses_select = document.createElement('select');
            courses_select_cell.appendChild(courses_select);
            courses_select.id = "courses_select";
            courses_select.style.width = "200px";
            courses_select.size = 5;
            courses_select.name = "courses";
            courses_select.multiple = "multiple";
            for(var i = 0; i < courses_list.length; i++){
                courses_select.options[i] = new Option(courses_list[i].name, courses_list[i].id);
                for(var j = 0; j < tutor_courses.length; j++){
                    if(tutor_courses[j].id == courses_list[i].id){
                        courses_select.options[i].selected = true;
                    }
                }
            }
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }   
    }); 

    // Get tag list
    var URL = "/account/getTags"
    var tags_list = [];
    var tutor_tags = JSON.parse(sessionStorage.getItem('subjectTag'));
    $.post(URL, null, function(response)
    {
        if(response.errno==0)
        {
            tags_list = response.data;
            var tags = table.insertRow(-1);
            var tags_desc = tags.insertCell(-1);
            tags_desc.innerHTML = "Subject tags:";
            var tags_select_cell = tags.insertCell(-1);
            var tags_select = document.createElement('select');
            tags_select_cell.appendChild(tags_select);
            tags_select.id = "tags_select";
            tags_select.style.width = "200px";
            tags_select.size = 5;
            tags_select.name = "tags";
            tags_select.multiple = "multiple";
            for(var i = 0; i < tags_list.length; i++){
                tags_select.options[i] = new Option(tags_list[i].name, tags_list[i].id);
                for(var j = 0; j < tutor_tags.length; j++){
                    if(tutor_tags[j].id == tags_list[i].id){
                        tags_select.options[i].selected = true;
                    }
                }
            }

            // var new_tag = table.insertRow(-1);
            // var new_tag_desc = new_tag.insertCell(-1);
            // new_tag_desc.innerHTML = "Create new tags:"
            // var new_tag_input_cell = new_tag.insertCell(-1);
            // var new_tag_input = document.createElement("input");
            // new_tag_input_cell.appendChild(new_tag_input);
            // new_tag_input.name = "new_tag";
            // new_tag_input.placeholder = "Enter your tags here, separate with space";
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }   
    });

    // html=html+
    // "<tr>" + 
    //     "<td>Teaching courses (course code):</td>" + 
    //     "<td><input type='text' id='course' value=" + "courses" + " placeholder='separate course codes by space' size=50></td>" + 
    // "</tr>" +
    // "<tr>" + 
    //     "<td>Subject tags:</td>" + 
    //     "<td><input type='text' id='tags' value=" + "tags" + " placeholder='separate tags by space' size=50></td>" + 
    // "</tr>";

    if(tutorType=='contracted')
    {
        var rate = table.insertRow(-1);
        var rate_desc = rate.insertCell(-1);
        rate_desc.innerHTML = "Hourly rate:";
        var rate_value = rate.insertCell(-1);
        rate_value.innerHTML = "N/A";

        // html=html+
        // "<tr>" + 
        //     "<td>Hourly rate:</td>" + 
        //     "<td>N/A</td>" + 
        // "</tr>";
    }
    else
    {
        var rate = table.insertRow(-1);
        var rate_desc = rate.insertCell(-1);
        rate_desc.innerHTML = "Hourly rate (must be a mutiple of 10): $";
        var rate_value = rate.insertCell(-1);
        var rate_value_input = document.createElement('input');
        rate_value.appendChild(rate_value_input);
        rate_value_input.min = 0
        rate_value_input.name = "hourly_rate";
        rate_value_input.value = sessionStorage.getItem('tutoringFee');

        // html=html+
        // "<tr>" + 
        //     "<td>Hourly Rate (must be a mutiple of 10): </td>" + 
        //     "<td> $<input type=number' id='hourlyRate' step='10' style='width: 3em' value=" + 0 +" min=0></td>" + 
        // "</tr>";
    }

    var searchable = table.insertRow(-1);
    var searchable_desc = searchable.insertCell(-1);
    searchable_desc.innerHTML = "Profile searchable by students";
    var searchable_check = searchable.insertCell(-1);
    var searchable_check_input = document.createElement('input');
    searchable_check.appendChild(searchable_check_input);
    searchable_check_input.type = "checkbox";
    searchable_check_input.name = "searchable";
    searchable_check_input.checked = sessionStorage.getItem('searchable')=="true"; 
}

// document.getElementById('setting').innerHTML=html;

function onApply()
{
    //send request
    var URL = "/editProfile";
    //create json from the formData
    var formData = new FormData(document.getElementById("profileSetting"));
    var json_raw = {
        "searchable": false,
        "courses": [],
        "tags": [],
        "hourly_rate": 0
    };
    for(var entry of formData.entries()){
        if(entry[0] == "searchable"){
            console.log(entry);
            json_raw[entry[0]] = (entry[1].length > 0);
        }else{
            json_raw[entry[0]] = entry[1];
        }
    }
    var json = JSON.stringify(json_raw);
    console.log(json);

    $.post(URL, json, function(response)
    {
        if(response.errno==0)
        {
            //setting
            sessionStorage.setItem('firstName', document.getElementById('firstName').value);
            sessionStorage.setItem('lastName', document.getElementById('lastName').value);
            sessionStorage.setItem('email', document.getElementById('email').value);
            sessionStorage.setItem('telNum', document.getElementById('phone').value);

            if(tutorType == 'undefined' || tutorType == null || tutorType=="")
            {
                window.parent.document.getElementById('content').setAttribute('src', "profileStudent.html");
            }
            else
            {
                //course and subject tag
                var courses_select = document.getElementById("courses_select").options;
                var new_courses = [];
                for(var i = 0; i < courses_select.length; i++){
                    if(courses_select[i].selected){
                        var c = {
                            "name": courses_select[i].text,
                            "id": courses_select[i].value
                        };
                        new_courses.push(c);
                    }
                }

                var tags_select = document.getElementById("tags_select").options;
                var new_tags = [];
                for(var i = 0; i < tags_select.length; i++){
                    if(tags_select[i].selected){
                        var t = {
                            "name": tags_select[i].text,
                            "id": tags_select[i].value
                        };
                        new_tags.push(t);
                    }
                }

                sessionStorage.setItem('courseTag', JSON.stringify(new_courses));
                sessionStorage.setItem('subjectTag', JSON.stringify(new_tags));
                sessionStorage.setItem('searchable', json_raw.searchable);

                if(tutorType!='contracted')
                {
                    sessionStorage.setItem('tutoringFee', json_raw.hourly_rate);
                }
                window.parent.document.getElementById('content').setAttribute('src', "profileTutor.html");
            }     
        }
        else
        {
            alert(response.errno + ": " + response.msg);
        }   
    });
}