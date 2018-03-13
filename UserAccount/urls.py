from django.conf.urls import url
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt

from . import views

# Urls for UserAccount app
urlpatterns = [

    # Url for display tutor information as student
    #tutor tabs can display when comment this
    #url(r'^tutor', views.getTutor, name='getTutor'),

    # Url for listing all users, only accessible by admins
    url(r'^all', csrf_exempt(views.listUsers), name='all'),

    # Url for display user information
    url(r'^accountProfile', csrf_exempt(views.accountProfile), name='accountProfile'),

    # Url for display tutor information as student
    #url(r'^accountTutorAsk', csrf_exempt(views.accountTutor), name='accountTutor'),
    url(r'^profileTutor', TemplateView.as_view(template_name='profileTutor.html')),
    url(r'^searchProfileTutor', TemplateView.as_view(template_name='searchProfileTutor.html')),
    url(r'^tutorTabs', TemplateView.as_view(template_name='tutorTabs.html')),

    # Url for display user profile as student
    #url(r'^accountStudentAsk', csrf_exempt(views.accountStudent), name='accountStudent'),
    url(r'^profileStudent', TemplateView.as_view(template_name='profileStudent.html')),
    url(r'^calendarDisplay', TemplateView.as_view(template_name='calendarDisplay.html')),

    # Url for access tutor timeslots as student
    url(r'^searchCalendarContracted', TemplateView.as_view(template_name='searchCalendarContracted.html')),
    url(r'^searchCalendarPrivate', TemplateView.as_view(template_name='searchCalendarPrivate.html')),
    url(r'^availableTimes', csrf_exempt(views.getTimeSlots), name='availableTimes'),

    # Url for modify time slots
    url(r'^disableTimeSlot', csrf_exempt(views.disableTimeSlot), name='disableTimeSlot'),
    url(r'^enableTimeSlot', csrf_exempt(views.enableTimeSlot), name='enableTimeSlot'),

    # Url for navigation bar on user ai overlay
    url(r'^navBar', TemplateView.as_view(template_name='navBar.html')),
    
    #account page, content will be switched (e.g. search result, profile, setting, etc)
    url(r'^account', TemplateView.as_view(template_name='account.html')),

    #profile setting template
    url(r'^profileSetting', TemplateView.as_view(template_name='profileSetting.html')),

    # Url for creating review
    url(r'^review', csrf_exempt(views.review), name='review'),
    # Url for requesting review
    url(r'^requestReview', csrf_exempt(views.requestReview), name='requestReview'),
    # Url for isting review
    url(r'^listReview', csrf_exempt(views.listReview), name='listReview'),

    # Url for getting a list of all universities
    url(r'^getUniversities$', views.getUniversities, name='getUniversities'),
    # Url for getting a list of all tags
    url(r'^getTags$', csrf_exempt(views.getTags), name='getTags'),
    # Ul for getting a list of all courses
    url(r'^getCourses$', csrf_exempt(views.getCourses), name='getCourses'),
]
