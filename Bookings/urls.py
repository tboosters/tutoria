from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from django.views.decorators.csrf import csrf_exempt

# Urls for Search app
urlpatterns = [
    # Url for verifying coupon
    url(r'^verify', views.verifyCoupon, name='verifyCoupon'),

    url(r'^listBookings', csrf_exempt(views.listBookings), name='listBooking'),
    url(r'^createBooking', csrf_exempt(views.createBooking), name='createBooking'),
    url(r'^removeBooking', csrf_exempt(views.removeBooking), name='removeBooking'),

    url(r'^bookingDetailsViewing', TemplateView.as_view(template_name='bookingDetailsViewing.html')),
    url(r'^bookingDetailsConfirmed', TemplateView.as_view(template_name='bookingDetailsConfirmed.html')),
    url(r'^bookingDetailsCancelled', TemplateView.as_view(template_name='bookingDetailsCancelled.html')),
    url(r'^bookingDetailsRequestConfirm', TemplateView.as_view(template_name='bookingDetailsRequestConfirm.html'))

]