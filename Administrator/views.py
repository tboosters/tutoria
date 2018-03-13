from django.core import serializers
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader

import json

from UserAccount.models import UserProfile
from .models import PasswordResetToken

# Views for Administrator App

# Control access to Tutoria through user authentication
def controlAccess(request):
	# Initialize response message variables
	errno = -1
	msg = ''
	data = {}

	# Retrieving tutor information
	try:
		try:
			# Retrieve request information
			request_body = json.loads(request.body)
			username = request_body['username']
			freeze = request_body['freeze']
		except:
			# Raise bad request response
			raise Exception(1, 'Bad reqeust')

		user_profile = UserProfile.getByUsername(username)
		if freeze:
			user_profile.user.is_active = False
		else:
			user_profile.user.is_active = True
		user_profile.user.save()
		errno = 0
		msg = 'Request succeeded!'

	except Exception as e:
		# Catch error responses raised
		try:
			errno, msg = e.args
		except:
			raise e

	# Build response message
	message = {
		'errno': errno,
		'msg': msg,
		'data': data
	}
	return JsonResponse(message)

# Request a reset password token
def requestResetToken(request):
	# Initialize response message variables
	errno = -1
	msg = ''
	data = {}

	try:
		try:
			# Retrieve request information
			request_body = json.loads(request.body)
			email = request_body['email']
		except:
			# Raise bad request response
			raise Exception(1, 'Bad reqeust')

		# Create a reset 
		token = PasswordResetToken.generateToken(email)
		if token == "":
			# Raise bad request response caused by unknown email
			raise Exception(2, 'Unknown email')
		
		# Fill in response content
		errno = 0
		msg = 'Request succeeded!'
		data['token'] = token

		# Send 'email' containing the token to the user
		print("To: ", email, "\n", \
			"You have requested a password reset. Please enter the following token in the password reset page:\n",
			token)
	except Exception as e:
		# Catch error responses raised
		try:
			errno, msg = e.args
		except:
			raise e

	# Build response message
	message = {
		'errno': errno,
		'msg': msg,
		'data': data
	}
	return JsonResponse(message)

# Verify a token
def verifyToken(request):
	# Initialize response message variables
	errno = -1
	msg = ''
	data = {}

	try:
		try:
			# Retrieve request information
			request_body = json.loads(request.body)
			token = request_body['token']
		except:
			# Raise bad request response
			raise Exception(1, 'Bad reqeust')

		# Verify token
		if not PasswordResetToken.verifyToken(token):
			# Raise bad request response caused by unknown token
			raise Exception(2, 'Unknown token')

		# Fill in response content
		errno = 0
		msg = 'Request succeeded!'
	except Exception as e:
		# Catch error responses raised
		try:
			errno, msg = e.args
		except:
			raise e

	# Build response message
	message = {
		'errno': errno,
		'msg': msg,
		'data': data
	}
	return JsonResponse(message)

# Initiate reset password by a given reset password token
def resetPassword(request):
	# Initialize response message variables
	errno = -1
	msg = ''
	data = {}

	try:
		try:
			# Retrieve request information
			request_body = json.loads(request.body)
			token = request_body['token']
			password1 = request_body['password1']
			password2 = request_body['password2']
		except:
			# Raise bad request response
			raise Exception(1, 'Bad reqeust')

		if password1 != password2:
			# Raise bad request response caused by mismatch passwords
			raise Exception(2, 'Password mismatch')

		if password1 == '':
			# Raise bad request responce caused by empty password
			raise Exception(3, 'Empty password')

		# Retrieve user from the given token
		user = PasswordResetToken.useToken(token)
		if not user:
			# Raise bad request response by unknown token
			raise Exception(4, 'unknown token')

		# Reset password
		user.set_password(password1)
		user.save()
		
		# Fill in response content
		errno = 0
		msg = 'Request succeeded!'

	except Exception as e:
		# Catch error responses raised
		try:
			errno, msg = e.args
		except:
			raise e

	# Build response message
	message = {
		'errno': errno,
		'msg': msg,
		'data': data
	}
	return JsonResponse(message)