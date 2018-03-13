# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from UserAccount.models import UserProfile

# Create your models here.

# Models in app Wallet
class Wallet(models.Model):
	wallet_id = models.AutoField(primary_key = True)
	wallet_balance = models.DecimalField(max_digits = 30, decimal_places = 2)
	user_profile = models.OneToOneField('UserAccount.UserProfile', on_delete=models.CASCADE, blank=True, null=True)

	# Method for create a new user wallet instance
	@classmethod
	def create(cls, wallet_balance, user_profile):
		new = cls(wallet_balance=wallet_balance, user_profile=user_profile)
		new.save()
		return new

	# Get wallet of the user with user_id
	def getByUserID(user_id):
		try:
			if user_id == -1:
				# Special case for getting my tutor wallet
				return Wallet.objects.get(user_profile__user__username="mytutor")
			else:
				userAccountObject = User.objects.get(id=user_id)
				userProfileObject = UserProfile.objects.get(user=userAccountObject)
				print(userProfileObject)
				return Wallet.objects.get(user_profile=userProfileObject)
		except:
			return None

	# Decrement user's wallet balance by fee
	def decrementBalance(user_id, fee):
		try:
			wallet = Wallet.getByUserID(user_id)
			# Get original balance
			oldBalance = wallet.wallet_balance
		except:
			# Return failure of any retrieval
			return -1
		# Calculate new balance of the wallet
		newBalance = oldBalance - fee
		# Update balance
		wallet.wallet_balance = newBalance
		wallet.save()
		# Return success of action
		return newBalance
	
	# Increment user's wallet balance by fee
	def incrementBalance(user_id, fee):
		try:
			wallet = Wallet.getByUserID(user_id)
			# Get original balance
			oldBalance = wallet.wallet_balance
		except:
			# Return failure of any retrieval
			return -1
		# Calculate new balance of the wallet
		newBalance = oldBalance + fee
		# Update balance
		wallet.wallet_balance = newBalance
		wallet.save()
		# Return success of action
		return newBalance

	# To string finction for wallets
	def __str__(self):
		return str(self.user_profile) + " ($" + str(self.wallet_balance) + ")"