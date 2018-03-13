from . import views

from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

# Urls for Administrator app
urlpatterns = [
	# Url for accessing admin page
	url(r'^$', TemplateView.as_view(template_name='admin.html')),

	# Url for controlling access
	url(r'^controlAccess', csrf_exempt(views.controlAccess), name='controlAccess')
]
