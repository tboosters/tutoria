var searchResult=JSON.parse(sessionStorage.getItem("searchResult"));
searchResult.sort(compareFee);
updatePage();

function updatePage()
{
	var html="";
	for(var i=0; i<searchResult.length; i++)
	{
		html=html+ "<li onclick='onSearchResultSelected("+ i +")'>" + createShortProfile(searchResult[i]) + "</li>";
	}

	document.getElementById("searchResult").innerHTML=html;
}

function compareFee(a,b) 
{
	aRate = parseFloat(a.hourly_rate);
	bRate = parseFloat(b.hourly_rate);
	if (aRate < bRate)
	{
		return -1;
	}
	else if (aRate > bRate)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

function compareRating(a,b) 
{
	if (a.rating > b.rating)
	{
		return -1;
	}
	else if (a.rating < b.rating)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

function sorting(idx)
{
	if(idx==0)
	{
		searchResult.sort(compareFee);
	}
	else if(idx==1)
	{
		searchResult.sort(compareRating);
	}

	updatePage();
}

function createShortProfile(object)
{
	var rating="";
	var rate=object.rating;
	for(var i=0; i<5; i++)
	{
		if(i<rate)
		{
			rating=rating+"<span class='fa fa-star checked'></span>";
		}
		else
		{
			rating=rating+"<span class='fa fa-star'></span>";
		}
	}

	var numOfTag=10;
	var tags="";
	for(var i=0; i<numOfTag; i++)
	{
		tags=tags+"#Tag ";
	}

	var fee=object.hourly_rate;
	var contrated=object.tutor_type=="contracted"? true : false;

	var html="<img src=\"static/img/profile.png\" width='70px' height='70px' style='display: inline-block; vertical-align:top; margin-right: 10px;'>" + 
				"<div style='display:inline-block;'>" + 
					"<div style='font-weight:bold; font-size: 20px; display:inline-block; margin-right: 30px;'>" + object.first_name + " " + 	object.last_name + "</div>" + 
					rating +
					"<div style='color: grey; font-size: 12px;'>" + "@" + object.tutor_id + "</div>" +
					"<div style='font-size: 18px;'>" + object.unviersity + "</div>" +
					"<div style='color: grey; font-size: 12px;'>";
	for(var i=0; i<object.tag.length; i++)
	{
		html=html+ "#" + object.tag[i] + " ";
	}

	html=html+ "</div>" +
	"</div>"
	+
	"<div style='display:inline-block; float: right; margin-right:20px'>" + 
		"<div style='font-weight:bold; font-size: 48px; display:inline-block;'>"+ (fee==0?"N/A":"$"+fee) +"</div>";
	
	if(contrated)
	{
		html=html+"<div style='color: grey; font-size: 12px;'>Contracted Tutor</div>";
	}


	html=html+"</div></div>";
	return html;
}


function onSearchResultSelected(idx)
{
	sessionStorage.setItem("selectedTutor", JSON.stringify(searchResult[idx]));
	sessionStorage.setItem("isSearch", 1);
	window.open("../account/searchProfileTutor.html", "_self");
}