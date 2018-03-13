# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import datetime as dt

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count
from django.db.models import Avg

# Models in app UserAccount
# Model for extension part of default user model
class UserProfile(models.Model):
	# Attributes
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)	
	phone_number = models.CharField(max_length=30, default='')

	# Derived attribute for simplier access to user attribute first_name
	@property
	def first_name(self):
	    return self.user.first_name
	@first_name.setter
	def first_name(self, value):
		self.user.first_name = value


	# Derived attribute for simplier access to user attribute last_name
	@property
	def last_name(self):
	    return self.user.last_name
	@last_name.setter
	def last_name(self,value):
		self.user.last_name = value

	# Derived attribute for simplier access to user attribute username
	@property
	def username(self):
	    return self.user.username
	@username.setter
	def username(self,value):
		self.user.username = value

	# Derived attribute for simplier access to user attribute email
	@property
	def email(self):
	    return self.user.email
	@email.setter
	def email(self,value):
		self.user.email = value

	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number):
		new = cls(user=user, phone_number=phone_number)
		new.save()
		return new

	# Method for getting a particular user profile by user_id
	def getByUserID(user_id):
		return UserProfile.objects.get(user__id=user_id)

	# Method for getting a particualr user profile by username
	def getByUsername(username):
		return UserProfile.objects.get(user__username=username)

	# To string function for User Profiles
	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

# Model for admin specialization of user profiles
class Admin(models.Model):
	# Attributes
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)

	# Derived attribute for simplier access to user attribute first_name
	@property
	def first_name(self):
	    return self.user_profile.first_name
	@first_name.setter
	def first_name(self, value):
		self.user_profile.first_name = value

	# Derived attribute for simplier access to user attribute last_name
	@property
	def last_name(self):
	    return self.user_profile.last_name
	@last_name.setter
	def last_name(self, value):
		self.user_profile.last_name = value

	# Derived attribute for simplier access to user attribute username
	@property
	def username(self):
	    return self.user_profile.username
	@username.setter
	def username(self, value):
		self.user_profile.username = value

	# Derived attribute for simplier access to user attribute email
	@property
	def email(self):
	    return self.user_profile.email
	@email.setter
	def email(self, value):
		self.user_profile.email = value

	# Method for getting all admins
	def listAll():
		return Admin.objects.all().exclude(user_profile__user__username="mytutor")

	# Method for getting a particualr admin user profile by username
	def getByUsername(username):
		try:
			return Admin.objects.get(user_profile__user__username=username)
		except:
			return None

	# Method for getting a particualr admin user profile by user id
	def getByUserID(user_id):
		try:
			return Admin.objects.get(user_profile__user__id=user_id)
		except:
			return None

	# To string function for Student
	def __str__(self):
		return str(self.user_profile)

# Model for student specialization of user profiles
class Student(models.Model):
	# Attributes
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)

	# Derived attribute for simplier access to user attribute first_name
	@property
	def first_name(self):
	    return self.user_profile.first_name
	@first_name.setter
	def first_name(self, value):
		self.user_profile.first_name = value

	# Derived attribute for simplier access to user attribute last_name
	@property
	def last_name(self):
	    return self.user_profile.last_name
	@last_name.setter
	def last_name(self, value):
		self.user_profile.last_name = value

	# Derived attribute for simplier access to user attribute username
	@property
	def username(self):
	    return self.user_profile.username
	@username.setter
	def username(self, value):
		self.user_profile.username = value

	# Derived attribute for simplier access to user attribute email
	@property
	def email(self):
	    return self.user_profile.email
	@email.setter
	def email(self, value):
		self.user_profile.email = value

	# Derived attribute for simplier access to user profile attribute phone number
	@property
	def phone_number(self):
	    return self.user_profile.phone_number
	@phone_number.setter
	def phone_number(self, value):
		self.user_profile.phone_number = value

	# Method for create a new user profile instance
	@classmethod
	def create(cls, user, phone_number):
		user_profile = UserProfile.create(user=user, phone_number=phone_number)
		new = cls(user_profile=user_profile)
		new.save()
		return user_profile

	# Method for getting all Student records
	def listAll():
		return Student.objects.all()

	# Method for getting a particular student by username
	def getByUsername(username):
		# Try retrieving student record
		try:
			student = Student.objects.get(user_profile__user__username=username)
			return student
		# Return nothing if student do not exist
		except:
			return None

	# Override save method of student
	def saveAll(self):
		self.save()
		self.user_profile.save()
		self.user_profile.user.save()

	# To string function for Student
	def __str__(self):
		return str(self.user_profile)

# Model for tutor specialization of user profiles
class Tutor(models.Model):
	# Attributes
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
	tutor_id = models.CharField(unique=True, max_length=30)
	tutor_type_choices = (('contracted', 'contracted'), ('private', 'private'))
	tutor_type = models.CharField(max_length=30, choices=tutor_type_choices, default='contracted')
	hourly_rate = models.DecimalField(max_digits=30, decimal_places=2, default=0.0)
	searchable = models.BooleanField(default=True)
	university = models.ForeignKey('University', blank=True, null=True)
	tags = models.ManyToManyField("Tag", blank=True)

	# Derived attribute for simplier access to user attribute first_name
	@property
	def first_name(self):
	    return self.user_profile.first_name
	@first_name.setter
	def first_name(self, value):
		self.user_profile.first_name = value

	# Derived attribute for simplier access to user attribute last_name
	@property
	def last_name(self):
	    return self.user_profile.last_name
	@last_name.setter
	def last_name(self, value):
		self.user_profile.last_name = value

	# Derived attribute for simplier access to user attribute username
	@property
	def username(self):
	    return self.user_profile.username
	@username.setter
	def username(self, value):
		self.user_profile.username = value

	# Derived attribute for simplier access to user attribute email
	@property
	def email(self):
	    return self.user_profile.email
	@email.setter
	def email(self, value):
		self.user_profile.email = value

	# Derived attribute for simplier access to user profile attribute phone number
	@property
	def phone_number(self):
	    return self.user_profile.phone_number
	@phone_number.setter
	def phone_number(self, value):
		self.user_profile.phone_number = value

	# Override save method of tutor
	def saveAll(self):
		self.save()
		self.user_profile.save()
		self.user_profile.user.save()

	# Method for create a new tutor instance
	@classmethod
	def create(cls, user, phone_number, tutor_type, university, tutor_id, hourly_rate):
		user_profile = UserProfile.create(user=user, phone_number=phone_number)
		if tutor_type == "contracted":
			hourly_rate = 0
		new = cls(user_profile=user_profile, \
						tutor_type=tutor_type, \
						university=University.objects.get(id=int(university)), \
						tutor_id=tutor_id, \
						hourly_rate=float(hourly_rate))
		new.save()
		return user_profile

	# Method for getting all tutor records
	def listAll():
		return Tutor.objects.all()

	# Method for getting an empty queryset for tutor
	def getEmptySet():
		return Tutor.objects.none()

	# Method for getting all searchable tutor records
	def listAllSearchable():
		return Tutor.objects.filter(searchable=True)

	# Method for getting a particular tutor by tutor id
	def getByTutorID(tutor_id):
		# Try retrieving tutor record
		try:
			tutor = Tutor.objects.get(tutor_id__exact=tutor_id)
			return tutor
		# Return nothing if tutor do not exist
		except:
			return None

	# Method for getting a particular tutor by username
	def getByUsername(username):
		# Try retrieving tutor record
		try:
			tutor = Tutor.objects.get(user_profile__user__username=username)
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
			query |= Q(user_profile__user__first_name__icontains=k)
			query |= Q(user_profile__user__last_name__icontains=k)
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
		availableTutors = TimeSlot.objects.filter(start_time__gte=now, end_time__lt=oneweek, status='available', tutor__in=tutorList).values_list('tutor', flat=True)
		result = tutorList.filter(user_profile__user__id__in=availableTutors)
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
			query |= Q(tags__name__icontains=k)
		#return queryset
		return Tutor.objects.filter(query)

	# Method for getting tutor records by tutor type
	def filterByTutorType(keywordArray):
		# Convert type if input is not array
		if not isinstance(keywordArray, list):
			keywordArray = [keywordArray]
		# Initialize query
		query = Q()
		# Insert or query for each tag in keyword array
		if (keywordArray[0]):
			query |= Q(tutor_type='contracted')
		if (keywordArray[1]):
			query |= Q(tutor_type='private')
		# Return queryset
		return Tutor.objects.filter(query)

	# Method for getting private tutor records by hourly price range
	def filterByPriceRange(rangeFrom, rangeTo):
		# Initialize query
		query = Q()
		# Insert and query for the price range
		query = Q(hourly_rate__gte=rangeFrom) & Q(hourly_rate__lte=rangeTo)
		# return queryset
		return Tutor.objects.filter(query)

	# Method for getting all tags of a tutor
	def listAllTags(self):
		return self.tags.filter(tag_type='tag')

	# Method for getting all courses of a tutor
	def listAllCourses(self):
		return self.tags.filter(tag_type='course')

	# To string function for Student
	def __str__(self):
		return str(self.user_profile)

# Model for tutor tags
class Tag(models.Model):
	# Attributes
	name = models.CharField(max_length=30, default='')
	tag_type_choices = (('course', 'course'), ('tag', 'tag'))
	tag_type = models.CharField(max_length=10, choices=tag_type_choices, default='tag')

	# Method for getting all tag records
	def listAllTags():
		return Tag.objects.filter(tag_type='tag')

	# Method for getting all course records
	def listAllCourses():
		return Tag.objects.filter(tag_type='course')

	# Method for getting a tag by tag id
	def getByTagID(tag_id):
		try:
			return Tag.objects.get(id=tag_id)
		except:
			return None

	# To string function for Tags
	def __str__(self):
		return str(self.tag_type) + ": " + str(self.name)

# Model for available time slots of tutors
class TimeSlot(models.Model):
	# Attributes
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	tutor = models.ForeignKey('Tutor')
	status_choices = (('available', 'available'), ('unavailable', 'unavailable'), ('booked', 'booked')) 
	status = models.CharField(max_length=30, choices=status_choices, default='available')

	# Method for create a new time slot instance
	@classmethod
	def create(cls, tutor, start_time, end_time, status='unavailable'):
		new = cls(tutor=tutor, start_time=start_time, end_time=end_time, status=status)
		new.save()
		return new

	# Method for create a range of time slot instances per tutor
	def rangeCreate(tutor, from_time, to_time, status='unavailable'):
		# Align time to minute
		from_time = from_time.replace(second=0, microsecond=0)
		to_time = to_time.replace(second=0, microsecond=0)
		# Change time values for different tutor types
		if (tutor.tutor_type == 'contracted'):
			# Change time values for contracted tutors
			if (from_time.minute > 0 and from_time.minute < 30):
				from_time = from_time.replace(minute=30)
			elif(from_time.minute > 30):
				from_time = from_time.replace(minute=0)
				from_time = from_time + dt.timedelta(hours=1)
			if (to_time.minute > 0 and to_time.minute < 30):
				to_time = to_time.replace(minute=30)
			elif(to_time.minute > 30):
				to_time = to_time.replace(minute=0)
				to_tiem = to_time + dt.timedelta(hours=1)
			interval = dt.timedelta(minutes=30)
		elif (tutor.tutor_type == 'private'):
			# Change time values for private tutors
			if (from_time.minute > 0):
				from_time = from_time.replace(minute=0)
				from_time = from_time + dt.timedelta(hours=1)
			if (to_time.minute > 0):
				to_time = to_time.replace(minute=0)
				to_time = to_time + dt.timedelta(hours=1)
			interval = dt.timedelta(hours=1)
		# Create timeslot per intervals
		current_time = from_time
		while current_time <= to_time:
			end_time = current_time + interval
			# Only create a new time slot if it does not overlap other timeslots
			if (not TimeSlot.objects.filter(tutor=tutor, start_time__lte=end_time, end_time__gt=current_time)):
				TimeSlot.create(tutor=tutor, \
									start_time=current_time, \
									end_time=current_time+interval,
									status=status)
				print("TimeSlots created for", tutor.first_name, tutor.last_name, "from", current_time, "to", end_time)
			current_time = end_time

	# Method for create a range of time slot intances for all tutors
	def rangeCreateAll(from_time, to_time, status='unavailable'):
		allTutors = Tutor.objects.all()
		for tutor in allTutors:
			TimeSlot.rangeCreate(tutor=tutor, \
									from_time=from_time, \
									to_time=to_time, \
									status=status)

	# TimeSlot batch creation function, duration in type datetime, legacy
	def batchCreate(duration):
		allTutors = Tutor.objects.all()
		start = datetime.now()
		start = start.replace(second=0, microsecond=0)
		for t in allTutors:
			current = start
			target = start + duration
			while start < target:
				end = start + dt.timedelta(minutes=30)
				TimeSlot.create(t, current, end)
			print("TimeSlots created for", t.first_name, t.last_name, "from", start, "to", target)

	# Method for getting all available time slots for a particular tutor
	def filterByTutorUserID(tutor_user_id):
		return TimeSlot.objects.filter(tutor__user=tutor_user_id).order_by("start_time")

	# Method for getting all available time slots as number array for a particular tutor
	def getTimeSlots(tutor_id):
		# Queryset for available times
		timeSlot = TimeSlot.objects.filter(tutor__tutor_id=tutor_id)
		aTimeArray = []
		for aTime in timeSlot:
			if(aTime.status == 'available'):
				aTimeArray.append(0)
			if(aTime.status == 'unavailable'):
				aTimeArray.append(1)
			if(aTime.status == 'booked'):
				aTimeArray.append(2)
		return aTimeArray


	# Method for getting all available time slots as number array for a particular tutor
	def get7DayTimeSlots(tutor_id):
		# Queryset for available times
		timeSlot = TimeSlot.objects.filter(tutor__tutor_id=tutor_id, start_time__gte=datetime.now(), end_time__lt=datetime.now()+dt.timedelta(days=7))
		aTimeArray = []
		for aTime in timeSlot:
			if(aTime.status == 'available'):
				aTimeArray.append(0)
			if(aTime.status == 'unavailable'):
				aTimeArray.append(1)
			if(aTime.status == 'booked'):
				aTimeArray.append(2)
		return aTimeArray


	# Check availability of timeslot
	def checkAvailability(tutor_id, start_time, end_time):
		print(TimeSlot.objects.filter( \
							tutor__tutor_id=tutor_id \
							, start_time=start_time \
							, end_time=end_time \
							))

		# Get status of the timeslot
		try:
			status = TimeSlot.objects.get( \
							tutor__tutor_id=tutor_id \
							, start_time=start_time \
							, end_time=end_time \
							).status
		except:
			return False
		
		return status == 'available'

	# Remove available timeslot for this tutor from "old" status to "new" status
	def markCalendar(tutor_id, start_time, end_time, old, new):
		try:
			timeslot_to_be_marked = TimeSlot.objects.get( \
						tutor__tutor_id=tutor_id \
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

	# To string function for Time Slot
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
	student = models.ForeignKey('student')
	is_anonymous = models.BooleanField(default=False)

	# Method for create a new review instance
	@classmethod
	def create(cls, stars, comment, tutor, student, is_anonymous):
		new = None
		# Create review only when there is a valid number of stars
		if 0 <= stars <= 5:
			new = cls(stars=stars, comment=comment, tutor=tutor, student=student, is_anonymous=is_anonymous)
			new.save()
		return new 

	def retrieveReview(tutor):
		return Review.objects.filter(tutor=tutor)

	def averageRating(tutor):
		avg = Review.objects.filter(tutor=tutor).aggregate(Avg('stars'))['stars__avg']
		if not avg:
			return 0
		else:
			return avg


	# To string function for Reviews
	def __str__(self):
		return "Review for " + str(self.tutor)

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

