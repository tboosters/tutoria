from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from . import views

# Urls for Search app
urlpatterns = [
	# Url for index page 
    url(r'^$', views.index, name='index'),

    # Url for search tutor
    url(r'^search$', views.searchTutor, name='searchTutor'),

    # Url for search tutor with advanced options
    url(r'^searchadvance$', csrf_exempt(views.searchTutorAdvanced), name='searchTutorAdvanced'),
    url(r'^searchResult', TemplateView.as_view(template_name='searchResult.html')),
]