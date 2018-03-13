from django.core import serializers
from django.db.models import DecimalField
from django.db.models import IntegerField
from django.db.models import Value
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader

from itertools import chain

import json

from UserAccount.models import Tutor
from UserAccount.models import University
from UserAccount.models import Tag

# Views for Search App

# Default page for search application
def index(request):
    context = {}
    return render(request, 'index.html', context)


# Search tutor by http request
def searchTutor(request):
    # Retrieve search critera from http request
    # Search critera in standardurl parameters search/search?keyword=k&date=1997&....
    keyword = request.GET.get('keyword', '')
    # Define containers
    context = {}
    tutorList = QuerySet()
    # Retrieving tutor informations
    if keyword == '':
        # Default search return all search results
        tutorList = Tutor.listAll()
    else:
        # Search tutor names with provided search critera
        # Separate mutiple keywords into array by space delimiter
        keywordArray = keyword.split()
        # Get tutors by provided queries
        tutorList = Tutor.filterByName(keywordArray)

    # Build context for template rendering
    context['tutorList'] = tutorList

    # Respond search result to client
    if not tutorList:
        # Empty search result
        return HttpResponse("No match result is found")
    else:
        # Render context into template
        results = ""
        for obj in tutorList:
            #results += str(obj) + "<br>"
            results += str(obj) + "<br>"
        return HttpResponse(results)
        #return render(request, '', context)

# Advanced Search tutor by json request
def searchTutorAdvanced(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []
    # Retrieving tutor information
    try:
        try:
            # Retrieve request information
            request_json = json.loads(request.body)
            name = request_json['name']
            university = request_json['university']
            courses = request_json['courses']
            tags = request_json['tags']
            price_range = request_json['price_range']
            tutor_type = request_json['tutor_type']
            seven_days = request_json['seven_days']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        # Get intial query sets
        tutorList = Tutor.listAllSearchable()    
        if seven_days:
            tutorList = Tutor.filterByAvailableIn7Days(tutorList)

        # Get query set for names
        if (isinstance(name, str) and name != "") or (isinstance(name, list) and name[0] != ""):
            tutorList &= Tutor.filterByName(name)
            
        # Get query set for university
        if (isinstance(university, str) and university != "") or (isinstance(university, list) and university[0] != ""):
            tutorList &= Tutor.filterByUniversity(university)

        # Get query set for courses
        if (isinstance(courses, str) and courses != "") or (isinstance(courses, list) and courses[0] != ""):
            tutorList &= Tutor.filterByTags(courses)

        # Get query set for tags
        if (isinstance(tags, str) and tags != "") or (isinstance(tags, list) and tags[0] != ""):
            tutorList &= Tutor.filterByTags(tags)
            
        # Get query set for price range
        if isinstance(price_range, list) and (price_range[0] != "" or price_range[1] != ""):
            if price_range[0] == "":
                price_range[0] = "0"
            if price_range[1] == "":
                price_range[1] = "2147483647"
            tutorList &= Tutor.filterByPriceRange(float(price_range[0]), float(price_range[1]))

        # Get query set for tutor type
        if isinstance(tutor_type, list):
            tutorList &= Tutor.filterByTutorType(tutor_type)

        # Exract information from tutor list
        for t in tutorList:
            # Exclude logged in tutor from search
            if (request.user.is_authenticated() and request.user.username == t.username):
                continue

            item = {}
            item["first_name"] = t.first_name
            item["last_name"] = t.last_name
            item["rating"] = 3
            item["tutor_id"] = t.tutor_id
            item["university"] = t.university.name
            item["email"] = t.email
            tags = []
            for tag in t.listAllTags():
                tags.append(tag.name)
            item["tag"] = tags
            item["tutor_type"] = t.tutor_type
            item["hourly_rate"] = t.hourly_rate
            data.append(item)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = data
    except Exception as e:
        # Catch error responses raised
        try:
            errno, msg = e.args
        except:
            raise e

    # Generate response message
    message = {
        "errno": errno,
        "msg": msg,
        "data": data 
    }
    #return HttpResponse(str(errno) + ": " + msg)
    return JsonResponse(message)

# Testing page response for private calendar
def calendarPrivate(request):
    context = {}
    return render(request, 'calendarPrivate.html', context)

# Testing response from private calendar JSON post calls
def testCalendarResponse(request):
    # Verify incoming resonse is JSON
    if request.is_ajax():
        if request.method == 'POST':
            try:
                # Retrieving data from incomming JSON
                content = json.loads(request.body.decode('utf-8'))
                return HttpResponse('recieved x = ', content['x'], ', y = ', content['y'], ', selected date = ', content['selectedDate'])
            except:
                # Raise bad request response
                return HttpResponseBadRequest()
    # Error message
    return HttpResponseNotFound()
