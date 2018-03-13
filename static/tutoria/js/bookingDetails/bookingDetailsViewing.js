var bookID=sessionStorage.getItem('bookingID');

function cancel()
{
    var html='<button type="button" class="cancelButton" onclick="onCancel()">Cancel Booking</button>';
    document.getElementById('cancelButtonWrapper').innerHTML=html;
}

function onCancel()
{
    if(confirm("Cancel the current tutorial?")===true)
    {
        var data = {'booking_id': bookID};
        $.post("removeBooking", JSON.stringify(data), function(response)
        {
            if(response.errno == 0)
            {
                window.opener.location.reload();
                window.open('bookingDetailsCancelled.html', "_self");
            }
            else
            {
                alert(response.errno + ": " + response.msg);
            }
        });
    }
}

cancel();