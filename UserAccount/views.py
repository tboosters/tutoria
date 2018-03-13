from django.contrib.auth import authenticate
from django.contrib.auth import login as defaultLogin
from django.contrib.auth import logout as defaultLogout
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader

import json

from Bookings.models import Booking
from UserAccount.models import TimeSlot
from UserAccount.models import Student
from UserAccount.models import Tutor
from UserAccount.models import Admin
from UserAccount.models import University
from UserAccount.models import Tag
from UserAccount.models import Review
from Wallet.models import Wallet

from datetime import datetime
import datetime as dt

# Views for UserAccount App

# Retrieve all userprofiles for admins
def listUsers(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieving tutor information
    try:
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(1, 'User not logged in')

        # Retrieve tutor by tutor id
        admin = Admin.getByUsername(request.user.username)
        if not admin:
            # Raise not found response
            raise Exception(2, 'Not an admin')

        students = Student.listAll()
        tutors = Tutor.listAll()
        # Generate data
        for s in students:
            if not any(d['username'] == s.username for d in data):
                s_data = {
                    "username": s.username,
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "active": s.user_profile.user.is_active
                }
                data.append(s_data)

        for t in tutors:
            if not any(d['username'] == t.username for d in data):
                t_data = {
                    "username": t.username,
                    "first_name": t.first_name,
                    "last_name": t.last_name,
                    "active": t.user_profile.user.is_active
                }
                data.append(t_data)

        # Raise success response and return data
        errno = 0
        msg = 'Request succeeded!'
    except Exception as e:
        # Catch error responses raised
        try:
            errno, msg = e.args
        except:
            raise e

    # Pack information into JSON
    message = {
        "errno": errno,
        "msg": msg,
        "data": data
    }
    # Render response
    return JsonResponse(message)

# Retrieve tutor informtion for student by htp request
def getTutor(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieve tutor name from http request
    tutor_id = request.GET.get('id', '')
    # Define containers
    tutor = Tutor()

    # Retrieving tutor information
    try:
        if tutor_id == '':
            # Raise bad request response
            raise Exception(1, 'Empty tutor information')

        # Retrieve tutor by tutor id
        tutor = Tutor.getByTutorID(tutor_id)
        if not tutor:
            # Raise not found response
            raise Exception(2, 'Tutor not found')

        # Retrieving available time for the tutor
        timeSlots = TimeSlot.filterByTutorUserID(tutor_id)
        # Raise success response and return data
        errno = 0
        msg = 'Request succeeded!'
        data = {
            "tutor": tutor,
            "availableilableTimes": timeSlots
        }
    except Exception as e:
        # Catch error responses raised
        try:
            errno, msg = e.args
        except:
            raise e

    # Pack information into JSON
    message = {
        "errno": errno,
        "msg": msg,
        "data": data
    }
    # Render response
    return JsonResponse(message)

# Redirect method for account tutor and account student
def accountProfile(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieving tutor information
    try:
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(1, 'User not logged in')

        # Try retrieving student user from logged in user
        student = Student.getByUsername(request.user.username)
        # Try retrieving tutor user from logged in user
        tutor = Tutor.getByUsername(request.user.username)
        # Try retrieving admin user from logged in user
        admin = Admin.getByUsername(request.user.username)

        # redirect as tutor
        if tutor != None:
            # Redirect to accountTutor
            return accountTutor(request)
        # redirect as student
        if student != None:
            # Redirect to accountStudent
            return accountStudent(request)
        # redirect as admin
        if admin != None:
            return accountAdmin(request)

        # Raise bad request response by unknown user type
        raise Exception(2, 'unknown user type')

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)

# Retrieve tutor profile information as tutor by username
def accountTutor(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieving tutor information
    try:
        # Try retrieving student user from logged in user
        student = Student.getByUsername(request.user.username)
        # Try retrieving tutor user from logged in user
        tutor = Tutor.getByUsername(request.user.username)

        # Determine if the tutor is also a student
        is_student = (student != None)

        # Retrieve university information
        university = University()
        try:
            university = tutor.university
        except:
            # Raise not found response caused by university not set
            raise Exception(4, 'Tutor university not set')

        # Retrieve all courses of the tutor
        courses = []
        for c in tutor.listAllCourses():
            item = {}
            item["id"] = c.id
            item["name"] = c.name
            courses.append(item)
        # Retrieve all tags of the tutor
        tags = []
        for t in tutor.listAllTags():
            item = {}
            item["id"] = t.id
            item["name"] = t.name
            tags.append(item)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "firstName" : tutor.first_name,
            "lastName" : tutor.last_name,
            "username" : tutor.username,
            "email" : tutor.email,
            "telNum" : tutor.phone_number,
            "is_student" : is_student,
            "is_tutor" : True,
            "tutorFee" : tutor.hourly_rate,
            "tutorID" : tutor.tutor_id,
            "tutorType" : tutor.tutor_type,
            "university" : university.name,
            "searchable" : tutor.searchable,
            "courseTag" : courses,
            "subjectTag" : tags
        }
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
    return JsonResponse(message)

# Retrieve student profile information as student by username
def accountStudent(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieving student information
    try:
        # Try retrieving student user from logged in user
        student = Student.getByUsername(request.user.username)
        # Try retrieving tutor user from logged in user
        tutor = Tutor.getByUsername(request.user.username)

        # Determine if the student is also a tutor
        is_tutor = (tutor != None)
            
        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "firstName" : student.first_name,
            "lastName" : student.last_name,
            "username" : student.username,
            "email" : student.email,
            "telNum" : student.phone_number,
            "is_student" : True,
            "is_tutor" : is_tutor
        }
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
    return JsonResponse(message)

# Retrieve admin profile information as admin by username
def accountAdmin(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieving admin information
    admin = Admin.getByUsername(request.user.username)
    try:
        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "firstName" : admin.first_name,
            "lastName" : admin.last_name,
            "username" : admin.username,
            "email" : admin.email,
            "telNum" : "",
            "is_student" : False,
            "is_tutor" : False
        }
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
    return JsonResponse(message)

# Retrieve all avaliable times for a particualr tutor
def getTimeSlots(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieving tutor information
    try:
        try:
            # Retrieve request information
            request_json = json.loads(request.body)
            tutor_id = request_json['tutor_id']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if tutor_id == '':
            # Raise bad request response caused by empty tutor_id
            raise Exception(2, 'Empty tutor id')

        # Retrieve available timeslots by tutor user id
        timeSlots = TimeSlot.get7DayTimeSlots(tutor_id)
            
        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "availableTimes": timeSlots
        }
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
    return JsonResponse(message)

# Method for black out time slot
def disableTimeSlot(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    try:
        try:
            # Retrieve request information
            request_json = json.loads(request.body)
            start_time = datetime.strptime(request_json['start_time'][:24], '%a %b %d %Y %H:%M:%S')
            # end_time = datetime.strptime(request_json['end_time'][:24], '%a %b %d %Y %H:%M:%S')
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Retrieve tutor object
        tutor = Tutor.getByUsername(request.user.username)
        if tutor == None:
            # Raise bad request response by user is not a tutor
            raise Exception(3, 'User is not a tutor')

        # Find endtime
        if tutor.type == 'contracted':
            delta = dt.timedelta(minutes=30)
        else:
            delta = dt.timedelta(hours=1)
        end_time = start_time + delta

        # Try to mark calander
        timeSlot = TimeSlot.markCalendar(tutor.tutor_id, start_time, end_time, 'available', 'unavailable')
        if timeSlot == None:
            # Raise bad request response by time slot not found
            raise Exception(4, 'Unable to change time slot status')

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)

# Method for black out time slot
def enableTimeSlot(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    try:
        try:
            # Retrieve request information
            request_json = json.loads(request.body)
            start_time = datetime.strptime(request_json['start_time'][:24], '%a %b %d %Y %H:%M:%S')
            # end_time = datetime.strptime(request_json['end_time'][:24], '%a %b %d %Y %H:%M:%S')
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Retrieve tutor object
        tutor = Tutor.getByUsername(request.user.username)
        if tutor == None:
            # Raise bad request response by user is not a tutor
            raise Exception(3, 'User is not a tutor')

        # Find endtime
        if tutor.type == 'contracted':
            delta = dt.timedelta(minutes=30)
        else:
            delta = dt.timedelta(hours=1)
        end_time = start_time + delta

        # Try to mark calander
        timeSlot = TimeSlot.markCalendar(tutor.tutor_id, start_time, end_time, 'unavailable', 'available')
        if timeSlot == None:
            # Raise bad request response by time slot not found
            raise Exception(4, 'Unable to change time slot status')

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)

# Sign up a new user using provided information
def signup(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieving signup information
    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            username = request_json['username']
            email = request_json['email']
            password1 = request_json['password1']
            password2 = request_json['password2']
            first_name = request_json['first_name']
            last_name = request_json['last_name']
            phone_number = request_json['phone_number']
            is_student = request_json['is_student']
            is_tutor = request_json['is_tutor']
            is_contracted = request_json['is_contracted']
            is_private = request_json['is_private']
            tutor_id = request_json['tutor_id']
            university = request_json['university']
            hourly_rate = request_json['hourly_rate']

        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if username == '':
            # Raise bad request response caused by empty username
            raise Exception(2, 'Empty username')

        if email == '':
            #Raise bad request response caused by empty email
            raise Exception(3, 'Empty email')

        if password1 != password2:
            # Raise bad request response caused by mismatch passwords
            raise Exception(4, 'Password mismatch')

        if password1 == '':
            # Raise bad request responce caused by empty password
            raise Exception(5, 'Empty password')

        if first_name == '':
            # Raise bad request response caused by empty first name
            raise Exception(6, 'Empty first name')

        if last_name == '':
            # Raise bad request response caused by empty last name
            raise Exception(7, 'Empty last name')

        if phone_number == '':
            # Raise bad request response caused by enpty phone number
            raise Exception(8, 'Empty phone number')

        if (not is_student and not is_tutor) or (is_contracted and is_private):
            # Raise bad request response created by invaliad user type
            raise Exception(9, 'Invalid user type')

        try:
            # Create user
            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create user profile
            if is_student:
                # Create user profile as student
                profile = Student.create(user=user, \
                                            phone_number=phone_number)
            if is_tutor:
                # Determine tutor type
                tutor_type = "contracted"
                if is_contracted:
                    tutor_type = "contracted"
                elif is_private:
                    tutor_type = "private"

                # Create user profile as contracted tutor
                profile = Tutor.create(user=user, \
                                        phone_number=phone_number, \
                                        tutor_type=tutor_type, \
                                        tutor_id=tutor_id, \
                                        university=university, \
                                        hourly_rate=float(hourly_rate))

                # Create time slots for the newly created tutor
                # Define start time
                start_time = datetime.now()
                start_time = start_time.replace(second=0, microsecond=0)
                # Define end time
                end_time = start_time + dt.timedelta(days=7)
                # Batch create time slots for all tutor
                TimeSlot.rangeCreate(Tutor.getByUsername(profile.username), start_time, end_time, 'available')

            # Create wallet
            Wallet.create(wallet_balance=0, user_profile=profile)

        except Exception as e:
            # Raise bad request response caused by unable to create and save user
            print(e)
            user.delete()
            raise Exception(11, 'Unable to save or create user')

        # Log in user
        user = authenticate(username=username, password=password1)
        defaultLogin(request, user)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)

# Edit a existing user profile using provided information
def editProfile(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieving signup information
    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            email = request_json['email']
            first_name = request_json['first_name']
            last_name = request_json['last_name']
            phone_number = request_json['phone_number']
            hourly_rate = request_json['hourly_rate']
            searchable = request_json['searchable']
            courses = request_json['courses']
            tags = request_json['tags']

        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        if email == '':
            #Raise bad request response caused by empty email
            raise Exception(3, 'Empty email')

        if first_name == '':
            # Raise bad request response caused by empty first name
            raise Exception(4, 'Empty first name')

        if last_name == '':
            # Raise bad request response caused by empty last name
            raise Exception(5, 'Empty last name')

        if phone_number == ' ':
            # Raise bad request response caused by enpty phone number
            raise Exception(6, 'Empty phone number')

        # Try retrieving student user profile from logged in user
        student = Student.getByUsername(request.user.username)
        if student != None:
            # Redirect to accountStudent
            print(student)
            student.email = email
            student.first_name = first_name
            student.last_name = last_name
            student.phone_number = phone_number
            student.saveAll()

         # Try retrieving tutor user profile from logged in user
        tutor = Tutor.getByUsername(request.user.username)
        if tutor != None:
            # Redirect to accountTutor
            print(tutor.email)
            print(email)
            tutor.email = email
            tutor.first_name = first_name
            tutor.last_name = last_name
            tutor.phone_number = phone_number
            tutor.hourly_rate = hourly_rate
            tutor.searchable = searchable
            tutor.tags.clear()
            for c in courses:
                tutor.tags.add(Tag.getByTagID(c))
            for t in tags:
                tutor.tags.add(Tag.getByTagID(t))
            tutor.saveAll()

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)

# Method for checking if a user is allowed to review a tutor
def requestReview(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieving request information
    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            tutor_id = request_json['tutor_id']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        # Check if user has logged in
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Get student that makes the request
        student = Student.getByUsername(request.user.username)
        if not student:
            # Raise bad request response by request not made by a student
            raise Exception(3, 'User is not student')

        # Get tutor to be reviewed
        tutor = Tutor.getByTutorID(tutor_id)
        if not tutor:
            # Raise bad request response by tutor id not found
            raise Exception(4, 'No such tutor')

        # Check if pass booking exist
        bookingSet = Booking.filterByStudentUsername(student.username)
        bookingSet &= Booking.filterByTutorUsername(tutor.username)
        bookingSet &= Booking.filterByEndTimeBefore(datetime.now())
        if not bookingSet:
            # Raise bad request response by no matching booking
            raise Exception(5, 'User not allowed to review')

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = []
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
    return JsonResponse(message)


# Method for creating a review for a tutor
def review(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieving request information
    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            tutor_id = request_json['tutor_id']
            stars = request_json['stars']
            comment = request_json['comment']
            is_anonymous = request_json['is_anonymous']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        # Check if user has logged in
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Get student that makes the request
        student = Student.getByUsername(request.user.username)
        if not student:
            # Raise bad request request not made by a student
            raise Exception(3, 'User is not student')

        # Get tutor to be reviewed
        tutor = Tutor.getByTutorID(tutor_id)
        if not tutor:
            raise Exception(4, 'No such tutor')

        # Create review
        if not Review.create(stars, comment, tutor, student, is_anonymous):
            # Throw exception when a review is not created because of invalid number of stars
            raise Exception(5, 'Invalid number of stars')

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = []
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
    return JsonResponse(message)

# List reviews of a tutor
def listReview(request):
        # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieving request information
    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            tutor_id = request_json['tutor_id']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        # Check if user has logged in
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Get tutor to be reviewed
        tutor = Tutor.getByTutorID(tutor_id)
        if not tutor:
            # Raise bad request response by tutor id not found
            raise Exception(3, 'No such tutor')

        # Check if pass booking exist
        reviews = Review.retrieveReview(tutor)
        # Generating review data
        review_data = []
        for r in reviews:
            e = {
                "stars": r.stars,
                "comment": r.comment
            }
            if r.is_anonymous:
                e['student'] = 'Anonymous'
            else:
                e['student'] = str(r.student)
            review_data.append(e)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "average": Review.averageRating(tutor),
            "entries": review_data
        }
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
    return JsonResponse(message)

# Retrieve all university record
def getUniversities(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieve university objects
    universities = University.listAll()

    # Extract information from query set
    for u in universities:
        print(u.name)
        item = {}
        item["name"] = u.name
        item["id"] = u.id
        data.append(item)
        
    # Filling response body
    errno = 0
    msg = "Request succeeded"
    data = data

    # Generate response message
    message = {
        "errno": errno,
        "msg": msg,
        "data": data 
    }
    return JsonResponse(message)

# Retrieve all tag record
def getTags(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieve tag objects
    tags = Tag.listAllTags()

    # Extract information from query set
    for t in tags:
        item = {}
        item["name"] = t.name
        item["id"] = t.id
        data.append(item)
        
    # Filling response body
    errno = 0
    msg = "Request succeeded"
    data = data

    # Generate response message
    message = {
        "errno": errno,
        "msg": msg,
        "data": data 
    }
    return JsonResponse(message)

# Retrieve all course record
def getCourses(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = []

    # Retrieve course objects
    tags = Tag.listAllCourses()

    # Extract information from query set
    for t in tags:
        item = {}
        item["name"] = t.name
        item["id"] = t.id
        data.append(item)
        
    # Filling response body
    errno = 0
    msg = "Request succeeded"
    data = data

    # Generate response message
    message = {
        "errno": errno,
        "msg": msg,
        "data": data 
    }
    return JsonResponse(message)

# Log in a user using provided information
def login(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieving login information
    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            username = request_json['username']
            password = request_json['password']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if username == '':
            # Raise bad request response caused by empty username
            raise Exception(2, 'Empty username')

        if password == '':
            # Raise bad request response caused by empty password
            raise Exception(3, 'Empty password')

        # Autentiate user
        user = authenticate(username=username, password=password)
        if user == None:
            # Raise bad request response caused by invalid login informations
            raise Exception(4, 'Invalid Login')
        # Log in user
        defaultLogin(request, user)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)

# Log out a user
def logout(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    try:
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(1, 'User not logged in')

        # Log out user
        defaultLogout(request)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {}
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
    return JsonResponse(message)