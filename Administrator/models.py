from random import choice

from django.db import models
from django.contrib.auth.models import User

from UserAccount.models import Student
from UserAccount.models import Tutor

import string

# Model for password reset token
class PasswordResetToken(models.Model):
	# Arributes
	token_string = models.CharField(max_length=30, primary_key=True)
	user = models.ForeignKey(User)

	# Generate a token by given user email and return the token string
	def generateToken(email):
		# Retrieve user account by given email
		user = User.objects.filter(email=email)
		if user:
			# Generate a unique random token string
			user = user.first()
			token_string = ""
			while token_string == "" or PasswordResetToken.objects.filter(token_string=token_string):
				for i in range(30):
					token_string += choice(string.ascii_letters + string.digits)

			# Create and save the token
			token = PasswordResetToken(token_string=token_string, user=user)
			token.save()
			return token_string
		else:
			return None

	# Verify a token
	def verifyToken(token_string):
		token = PasswordResetToken.objects.filter(token_string=token_string)
		if token:
			return True
		else:
			return False

	# Retrieve the user for a particular token, delete the token in the process
	def useToken(token_string):
		# Retrieve user account by given token string
		token = PasswordResetToken.objects.filter(token_string=token_string)
		if token:
			user = token.first().user
			token.first().delete()
			return user
		else:
			return None

	# To string
	def __str__(self):
		return self.token_string


