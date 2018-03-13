# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import datetime as dt

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count

# Models in app UserAccount
# Model for extension part of default user model
class UserProfile(models.Model):
	# Attributes
	user = models.OneToOneField(User, on_delete=models.CASCADE)	
	phone_number = models.CharField(max_length=30, default='')

	# Derived attribute for simplier access to user attribute first_name
	@property
	def first_name(self):
	    return self.user.first_name

	# Derived attribute for simplier access to user attribute last_name
	@property
	def last_name(self):
	    return self.user.last_name

	# Derived attribute for simplier access to user attribute username
	@property
	def username(self):
	    return self.user.username

	# Derived attribute for simplier access to user attribute email
	@property
	def email(self):
	    return self.user.email

	# Method for create a new user profile instance, should be overridden
	@classmethod
	def create(cls):
		print ("Method should not be directly called without overriding")

	# Method for getting a particular user by user_id
	def getByUserID(user_id):
		return User.objects.get(id=user_id)

	def getByUsername(username):
		return User.objects.get(user__username=username)

	# To string function for User Profiles
	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

# Model for admin specialization of user profiles
class Admin(UserProfile):
	pass

# Model for student specialization of user profiles
class Student(UserProfile):

	# Method for getting a particular student by user id
	def getByUsername(username):
		# Try retrieving student record
		try:
			student = Student.objects.filter(user__username=username)
			studentPrivateTutor = StudentPrivateTutor.objects.filter(user__username=username)
			studentContractedTutor = StudentContractedTutor.objects.filter(user__username=username)
			if student:
				return student.first()
			if studentPrivateTutor:
				return studentPrivateTutor.first()
			if studentContractedTutor:
				return studentContractedTutor.first()
		# Return nothing if student do not exist
		except:
			return None

	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number):
		return cls(user = user, \
						phone_number = phone_number)

# Model for tutor specialization of user profiles
class Tutor(UserProfile):
	# Attributes
	tutor_id = models.CharField(unique=True, max_length=30)
	tutor_type_choices = (('contracted', 'contracted'), ('private', 'private'))
	tutor_type = models.CharField(max_length=30, choices=tutor_type_choices, default='contracted')
	university = models.ForeignKey('University')
	tags = models.ManyToManyField("Tag")

	# Method for getting all tutor records
	def listAll():
		return Tutor.objects.all()

	# Method for getting an empty queryset for tutor
	def getEmptySet():
		return Tutor.objects.none()

	# Method for getting a particular tutor by tutor id
	def getByTutorID(tutor_id):
		# Try retrieving tutor record
		try:
			tutor = Tutor.objects.get(tutor_id__exact=tutor_id)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting a particular tutor by user id
	def getByUsername(username):
		# Try retrieving tutor record
		try:
			tutor = Tutor.objects.get(user__username__exact=username)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting tutor records by name
	def filterByName(keywordArray):
		# Convert type if input is not array
		if isinstance(keywordArray, str):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each name in keyword array
		for k in keywordArray:
			print(k)
			query |= Q(user__first_name__icontains=k)
			query |= Q(user__last_name__icontains=k)
		# return queryset
		return Tutor.objects.filter(query)

	# Method for getting tutor records by university
	def filterByUniversity(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each university in keyword array
		for k in keywordArray:
			query |= Q(university__name=k)
		# return queryset
		return Tutor.objects.filter(query)

	# Method for getting contracted tutor records by at least 1 available timeslot in 7 days
	def filterByAvailableIn7Days(tutorList):
		now = datetime.now()
		oneweek = now + dt.timedelta(days=7)
		availableTutors = AvailableTime.objects.filter(start_time__gte=now, end_time__lt=oneweek, status='available', tutor__in=tutorList).values_list('tutor', flat=True)
		result = tutorList.filter(id__in=availableTutors)
		return result

	# Method for getting tutor records by tag
	def filterByTags(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each tag in keyword array
		for k in keywordArray:
			query |= Q(tags__name=k)
		#return queryset
		return Tutor.objects.filter(query)

	# Method for getting all tags of a tutor
	def listAllTags(self):
		return self.tags.filter(tag_type='tag')

		# Method for getting all courses of a tutor
	def listAllCourses(self):
		return self.tags.filter(tag_type='course')

# Model for contracted tutor specialization of tutors
class ContractedTutor(Tutor):
	
	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number, university, tutor_id):
		return cls(user = user, \
						phone_number = phone_number, \
						tutor_type = 'contracted', \
						university = University.objects.get(id=university), \
						tutor_id = tutor_id)

	# Method for getting all contracted tutor records
	def listAll():
		return ContractedTutor.objects.all()

	# Method for getting an empty queryset for contracted tutor
	def getEmptySet():
		return ContractedTutor.objects.none()

	# Method for getting a particular contracted tutor by tutor id
	def getByTutorID(tutor_id):
		# Try retrieving tutor record
		try:
			tutor = ContractedTutor.objects.get(tutor_id__exact=tutor_id)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting a particular contracted tutor by user id
	def getByUsername(username):
		# Try retrieving tutor record
		try:
			tutor = ContractedTutor.objects.get(user__username__exact=username)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting contracted tutor records by name
	def filterByName(keywordArray):
		# Convert type if input is not array
		if isinstance(keywordArray, str):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each name in keyword array
		for k in keywordArray:
			print(k)
			query |= Q(user__first_name__icontains=k)
			query |= Q(user__last_name__icontains=k)
		# return queryset
		return ContractedTutor.objects.filter(query)

	# Method for getting contracted tutor records by university
	def filterByUniversity(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each university in keyword array
		for k in keywordArray:
			query |= Q(university__name=k)
		# return queryset
		return ContractedTutor.objects.filter(query)

	# Method for getting contracted tutor records by tag
	def filterByTags(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each tag in keyword array
		for k in keywordArray:
			query |= Q(tags__name=k)
		#return queryset
		return ContractedTutor.objects.filter(query)

# Model for private tutor specialization of tutors
class PrivateTutor(Tutor):
	# Attributes
	hourly_rate = models.DecimalField(max_digits=30, decimal_places=2, default=0.0)

	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number, tutor_id, university, hourly_rate):
		return cls(user = user, \
						phone_number = phone_number, \
						tutor_type = 'private', \
						tutor_id = tutor_id, \
						university = University.objects.get(id=university), \
						hourly_rate = hourly_rate)

	# Method for getting all private tutor records
	def listAll():
		return PrivateTutor.objects.all()

	# Method for getting an empty queryset for private tutor
	def getEmptySet():
		return PrivateTutor.objects.none()

	# Method for getting a particular private tutor by tutor id
	def getByTutorID(tutor_id):
		# Try retrieving tutor record
		try:
			tutor = PrivateTutor.objects.get(tutor_id__exact=tutor_id)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting a particular private tutor by user id
	def getByUsername(username):
		# Try retrieving tutor record
		try:
			tutor = PrivateTutor.objects.get(user__username__exact=username)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting private tutor records by name
	def filterByName(keywordArray):
		# Convert type if input is not array
		if isinstance(keywordArray, str):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each name in keyword array
		for k in keywordArray:
			print(k)
			query |= Q(user__first_name__icontains=k)
			query |= Q(user__last_name__icontains=k)
		# return queryset
		return PrivateTutor.objects.filter(query)

	# Method for getting private tutor records by university
	def filterByUniversity(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each university in keyword array
		for k in keywordArray:
			query |= Q(university__name=k)
		# return queryset
		return PrivateTutor.objects.filter(query)

	# Method for getting private tutor records by tag
	def filterByTags(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each tag in keyword array
		for k in keywordArray:
			query |= Q(tags__name=k)
		#return queryset
		return PrivateTutor.objects.filter(query)

	# Method for getting private tutor records by hourly price range
	def filterByPriceRange(rangeFrom, rangeTo):
		# Initialize query
		query = Q()
		# Insert and query for the price range
		query = Q(hourly_rate__gte=rangeFrom) & Q(hourly_rate__lte=rangeTo)
		# return queryset
		return PrivateTutor.objects.filter(query)

# Model for contracted tutor doubles also as a student
class StudentContractedTutor(ContractedTutor):

	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number, university, tutor_id):
		return cls(user = user, \
						phone_number = phone_number, \
						tutor_type = 'contracted', \
						university = University.objects.get(id=university), \
						tutor_id = tutor_id)

# Model for private tutor doubles also as a student
class StudentPrivateTutor(PrivateTutor):

	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number, tutor_id, university, hourly_rate):
		return cls(user = user, \
						phone_number = phone_number, \
						tutor_type = 'private', \
						tutor_id = tutor_id, \
						university = University.objects.get(id=university), \
						hourly_rate = hourly_rate)
	
# Model for tutor tags
class Tag(models.Model):
	# Attributes
	name = models.CharField(max_length=30, default='')
	tag_type_choices = (('course', 'course'), ('tag', 'tag'))
	tag_type = models.CharField(max_length=10, choices=tag_type_choices, default='tag')

	# Method for getting all tag records
	def listAllTags():
		return Tag.objects.filter(tag_type='tag')

	# method for getting all course records
	def listAllCourses():
		return Tag.objects.filter(tag_type='course')

	# To string function for Tags
	def __str__(self):
		return str(self.tag_type) + ": " + str(self.name)

# Model for available time slots of tutors
class AvailableTime(models.Model):
	# Attributes
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	tutor = models.ForeignKey('Tutor')
	status_choices = (('available', 'available'), ('unavailable', 'unavailable'), ('booked', 'booked')) 
	status = models.CharField(max_length=30, choices=status_choices, default='available')

	# Method for getting all available time for a particular tutor
	def filterByTutorUserID(tutor_user_id):
		return AvailbleTime.objects.filter(tutor__user=tutor_user_id)

	# Method for getting all available time as number array for a particular tutor
	def getAvailableTimes(tutor_user_id):
		# Queryset for available times
		availableTime = AvailableTime.objects.filter(tutor__user=tutor_user_id)
		aTimeArray = []
		for aTime in availableTime:
			if(aTime.status == 'available'):
				aTimeArray.append(0)
			if(aTime.status == 'unavailable'):
				aTimeArray.append(1)
			if(aTime.status == 'booked'):
				aTimeArray.append(2)
		return aTimeArray

	# Check availability of timeslot
	def checkAvailability(tutor_user_id, start_time, end_time):
		# Get status of the timeslot
		try:
			status = AvailableTime.objects.get( \
							tutor__user=tutor_user_id \
							, start_time=start_time \
							, end_time=end_time \
							).status
		except:
			return False
		
		return status == 'available'

	# Remove available timeslot for this tutor from "old" status to "new" status
	def markCalendar(tutor_user_id, start_time, end_time, old, new):
		try:
			timeslot_to_be_marked = AvailableTime.objects.get( \
						tutor__user=tutor_user_id \
						, start_time=start_time \
						, end_time=end_time \
						, status=old)
			timeslot_to_be_marked.status = new
			timeslot_to_be_marked.save()
			# Return the timeslot queryset if action succeeds
			print('marked')
			return timeslot_to_be_marked
		except:
			# Return none if fail to retrieve an available timeslot -> this timeslot is already 
			return None

	# To string function for Available Time
	def __str__(self):
		return str(self.start_time.date()) + " " + \
				 str(self.start_time.time()) + " to " + \
				 str(self.end_time.time()) + " : " + \
				 str(self.tutor)

# Model for review of tutors
class Review(models.Model):
	# Attributes
	stars = models.IntegerField(default=0)
	comment = models.TextField(default='')
	tutor = models.ForeignKey('tutor')

	# To string function for Reviews
	def __str__(self):
		return "Review for " + str(tutor.name)

# Model for university of tutors
class University(models.Model):
	# Attributes
	name = models.CharField(max_length = 90, default='')

	# Method for getting all university records
	def listAll():
		return University.objects.all()

	# To string function for University
	def __str__(self):
		return self.name

