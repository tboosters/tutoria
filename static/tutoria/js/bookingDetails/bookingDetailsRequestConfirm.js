var couponCodeCorrect=true;
function createCouponCodeInput()
{
    var html='<input type="checkbox" name="enable" id="useCouponCode" onclick="useCoupon(this.checked)"> Coupon Code ' +
        '<input type="text" id="couponCodeInput" name="couponCode" disabled size="32">';

    document.getElementById('couponCode').innerHTML=html;
}

var discount=0;
var tutoringFee=parseFloat(detailsInfo[7].substring(1));

function total()
{
    var html='<tr><td>Tutoring Fee:</td><td></td><td>' + '$'+tutoringFee + '</td></tr>' +
        '<tr><td>Commission Fee:</td><td></td><td>' + '$'+ tutoringFee*0.05 + '</td></tr>' +
        '<tr><td>Coupon Discount:</td><td>-</td><td>' + '$'+ discount + '</td></tr>' +
        '<tr><td colspan="3"><hr></td></tr>' +
        '<tr><td>Total:</td><td></td><td>' + '$'+ (tutoringFee+tutoringFee*0.05-discount) + '</td></tr>';
    document.getElementById('total').innerHTML=html;
    sessionStorage.setItem('tutoringFee', tutoringFee+tutoringFee*0.05-discount);
}

function terms()
{
    var html='<input type="checkbox" name="terms" id="agreeTerms" onclick="agreeTerms(this.checked)"> I agree to the terms of <a href="https://www.google.com" target="_blank">Tutoria Payment Agreement</a>';
    document.getElementById('terms').innerHTML=html;
}

function confirmButton()
{
    var html='<button type="button" class="confirmButton" onclick="onConfirm()">Confirm</button>';
    document.getElementById('confirmButtonWrapper').innerHTML=html;
}

function useCoupon(use)
{
    if(!use)
    {
        document.getElementById('couponCodeInput').setAttribute("disabled","disabled");
        discount=0;
    }
    else
    {
        document.getElementById('couponCodeInput').removeAttribute("disabled");
        if(couponCodeCorrect)
        {
            discount=tutoringFee*0.05;
        }
    }

    total();
}

function agreeTerms(agree)
{

}

function onConfirm()
{
    if(!document.getElementById("agreeTerms").checked)
    {

    }
    else if(!couponCodeCorrect)
    {

    }
    else
    {
        if(confirm("Book the current tutorial?")===true)
        {
            var URL="../booking/createBooking";
            var data={'csrfmiddlewaretoken':"{{ csrf_token }}", 'tutor_id': selectedTutor.tutor_id, 'fee': tutoringFee, 'start_time': startDateUTC , 'end_time': endDateUTC, 'coupon_code': document.getElementById('couponCodeInput').value};
            $.post(URL, JSON.stringify(data), function(response)
            {
                if(response.errno==0)
                {
                    window.opener.location.reload();
                    window.open('../booking/bookingDetailsConfirmed.html',"_self");
                }
                else
                {
                    alert(response.errno + ": " + response.msg);
                    //update page
                }
            });
        }
    }
}

createCouponCodeInput();
total();
terms();
confirmButton();