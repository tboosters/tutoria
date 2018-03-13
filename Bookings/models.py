# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import datetime as dt

from django.db import models

from UserAccount.models import User
from UserAccount.models import UserProfile
from UserAccount.models import Student
from UserAccount.models import Admin
from UserAccount.models import TimeSlot
from Wallet.models import Wallet

# Models in app Bookings
# Model for bookings made by student in booking a tutor session
class Booking(models.Model):
	booking_id = models.AutoField(primary_key = True)
	book_time = models.DateTimeField()
	book_fee = models.DecimalField(max_digits = 30, decimal_places = 2)
	time_slot = models.ForeignKey('UserAccount.TimeSlot', blank=True, null=True)
	cancelled = models.BooleanField(default=False)
	student = models.ForeignKey('UserAccount.Student')
	coupon = models.ForeignKey('Coupon', blank=True, null=True)

	# Return the record with booking_id
	def getBooking(booking_id):
		try:
			return Booking.objects.get(booking_id=booking_id)
		except:
			return None

	# Return all the bookings booked by student
	def filterByStudentUsername(student_username):
		return Booking.objects.filter(student__user_profile__user__username=student_username)

	# Return all the bookings booking a tutor
	def filterByTutorUsername(tutor_username):
		return Booking.objects.filter(time_slot__tutor__user_profile__user__username=tutor_username)

	# Return all the bookings booked by student
	def filterByStudentUserID(student_user_id):
		return Booking.objects.filter(student__user_profile__user__id=student_user_id).order_by("time_slot__start_time")

	# Return all the bookings booking a tutor
	def filterByTutorUserID(tutor_user_id):
		return Booking.objects.filter(time_slot__tutor__user_profile__user__id=tutor_user_id).order_by("time_slot__start_time")

	# Return all the bookings ends before a specific time
	def filterByEndTimeBefore(time):
		return Booking.objects.filter(time_slot__end_time__lt=time)

	# Return all the bookings ending at specified time
	def filterByEndTime(time):
		# 5 seconds tolerance to cope with system delay / demo etc.
		tolerance = dt.timedelta(seconds=5)
		return Booking.objects.filter(time_slot__end_time__gte=time-tolerance, time_slot__end_time__lte=time+tolerance)

	# Check the pre-conditions for a student to be able to book a session
	# OK  -  errno: 0
	# Student does not exsist  -  errno: 1, msg: 'No such student'
	# Wallet has enough balance?  -  errno: 2, msg: 'Not enough balance'
	# Is the tutor free at this time?  -  errno: 3, msg: 'Session time is not available'
	# Student still have the quota?  -  errno: 4, msg: 'Student has no quota'
	def checkPreConditions(student_user_id, tutor_id, fee, start_time, end_time):
		# Initiate results
		errno = -1
		msg = ''
		# Check if student exists
		try:
			studentObject = Student.objects.get(user_profile__user__id=student_user_id)
		except:
			# Student is not found
			return {'errno': 1, 'msg': 'No such student'}

		# Get current wallet balance
		userAccountObject = User.objects.get(id=student_user_id)
		userProfileObject = UserProfile.objects.get(user=userAccountObject)
		wallet_current_balance = Wallet.objects.get(user_profile=userProfileObject).wallet_balance
		# Check if wallet has enough balance
		if wallet_current_balance - fee < 0:
			# Not enough current balance to pay for tutor fee
			return {'errno': 2, 'msg': 'Not enough balance'}

		# Still have quota, continue
		if TimeSlot.checkAvailability(tutor_id, start_time, end_time):
			# Create datetime object for day of start_time and the next day with time 00:00:00
			thisDay = datetime.combine(start_time.date(), datetime.min.time())
			nextDay = datetime.combine(start_time.date() + dt.timedelta(days=1) \
					, datetime.min.time())
			try:
				# Get any booking of this student in the day of the sessions time
				booking = Booking.objects.get(student=studentObject \
				, time_slot__start_time__gte=thisDay\
				, time_slot__end_time__lt=nextDay)
				if booking.cancelled:
					return {'errno': 0, 'msg': ''}
				else:
					return {'errno': 4, 'msg': 'Student has no quota'}
			except:
				return {'errno': 0, 'msg': ''}
		else:
			return {'errno': 3, 'msg': 'Session time is not available'}

	# Create a new booking
	def createBooking(student_user_id, fee, time_slot, coupon_code=""):
		try:
			studentObject = Student.objects.get(user_profile__user__id=student_user_id)
			# Get time of booking
			now = datetime.now()
			# Create new booking record
			new_Booking = Booking( \
				student= studentObject\
				, book_time=now \
				, book_fee=fee \
				, time_slot=time_slot)
			if (coupon_code != ""):
				new_Booking.coupon = Coupon.getByCode(coupon_code)
			new_Booking.save()
			# Return the newly created booking id
			return new_Booking.booking_id
		except Exception as e:
			raise e
			return None

	# Remove the booking (only when the corresponding studentId is provided)
	def removeBooking(student_user_id, booking_id):
		try:
			# Get the student object related to this booking
			studentObject = Student.objects.get(user_profile__user__id=student_user_id)
			booking = Booking.objects.get(student=studentObject, booking_id=booking_id)
			booking.cancelled = True;
			booking.save()
			# Return true if removal succeeded
			return True
		except:
			# Return false if removal failed
			return False

	# To string function for bookings
	def __str__(self):
		return str(self.time_slot) + " booked by " + str(self.student)

# Model for cupons
class Coupon(models.Model):
	coupon_code = models.CharField(max_length = 30)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	# Validate coupon code specified
	def isValid(code):
		# Get current datetime
		now = datetime.now()
		# Find a match in database of same coupon code and matches the valid period
		match = Coupon.objects.filter(coupon_code=code).filter(start_time__lte=now).filter(end_time__gte=now)
		# Return if a match can be found -> whether the coupon code is valid
		return match.exists()

	# Get a coupon by a given coupon code
	def getByCode(coupon_code):
		try:
			return Coupon.objects.get(coupon_code=coupon_code)
		except:
			return None

	# To string function for coupons
	def __str__(self):
		return str(self.coupon_code) + " (" +\
				 str(self.start_time.date()) + " " +\
				 str(self.start_time.time()) + " - " +\
				 str(self.end_time.time()) + ")"

# Model for transaction records
class Transaction(models.Model):
	amount = models.DecimalField(max_digits = 30, decimal_places = 2, default = 0.0)
	time = models.DateTimeField()
	detail = models.TextField()
	wallet = models.ForeignKey('Wallet.Wallet')

	# Method for create a new transaction instance
	def createTransaction(user_id, amount, detail):
		# Retrieve wallet object for specific user
		wallet = Wallet.getByUserID(user_id)

		new_transaction = Transaction(amount = amount, \
									time = datetime.now(), \
									detail = detail, \
									wallet =wallet)
		new_transaction.save()
		return new_transaction

	# Method for retrieving transactions in 'days' days
	def retrieveTransactions(user_id, days):
		# Retrieve wallet object for specific user
		if not Admin.getByUserID(user_id):
			wallet = Wallet.getByUserID(user_id)
		else:
			wallet = Wallet.getByUserID(-1)
		# Retrieve time now
		now = datetime.now()
		# Retrieve the transactions
		transactions = Transaction.objects.filter(wallet = wallet, \
												time__lte = now, \
												time__gte = now-dt.timedelta(days=days))
		return transactions

	# To string function for transcations
	def __str__(self):
		return str(self.wallet.user_profile) + ": " + \
				"$" + str(self.amount) + " " + \
				str(self.detail)