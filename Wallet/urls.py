from django.conf.urls import url

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from . import views
from Bookings import views as bviews

urlpatterns = [
	# Url for getting wallet page
	url(r'^$', TemplateView.as_view(template_name='wallet.html'), name='wallet'),

	# Url for getting wallet balance
	url(r'^balance', csrf_exempt(views.getBalance), name='balance'),

    # Url for users to add value to wallet / transfer money out
    url(r'^addValue', csrf_exempt(views.studentAddValue), name='addValue'),
    url(r'^tutorTransfer', csrf_exempt(views.tutorTransferMoney), name='tutorTransfer'),
    url(r'^myTutorTransfer', csrf_exempt(views.myTutorTransferMoney), name='myTutorTransfer'),

    # Url for users to view transaction records
    url(r'^transactions', csrf_exempt(bviews.listTransactions), name='transactions')
]
