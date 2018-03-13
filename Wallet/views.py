# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

import json

from UserAccount.models import Student
from UserAccount.models import Tutor
from UserAccount.models import Admin
from Wallet.models import Wallet
from Bookings.models import Transaction

# Create your views here.

# Method for students to add value to their wallet
def studentAddValue(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieving tutor information
    try:
        # Try retrieving the amount to be added to the wallet
        try:
            request_json = json.loads(request.body)
            amount = request_json['amount']
        except:
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Try retrieving student user from logged in user
        student = Student.getByUsername(request.user.username)
        if student == None:
        	# Raise bad request response by unknown user type
        	raise Exception(3, 'Not a student')

        # Increment the amount
        new_balance = Wallet.incrementBalance(student.user_profile.user.id, amount)
        # Create Transaction record for value added
        Transaction.createTransaction(student.user_profile.user.id, \
                                        amount, \
                                        'Value added by student ' + \
                                        str(student) + "("+student.username+")")

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
        	"new_balance": new_balance
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

# Method for getting wallet balance of a user
def getBalance(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieving tutor information
    try:
        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Retrieve wallet from logged in user
        if not Admin.getByUsername(request.user.username):
            wallet = Wallet.getByUserID(request.user.id)
        else:
            wallet = Wallet.getByUserID(-1)
        if wallet == None:
            # Raise bad request response by wallet not found
            raise Exception(3, 'Wallet not found')

        balance = wallet.wallet_balance

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "balance": balance
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

def tutorTransferMoney(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieving tutor information
    try:
        # Try retrieving the amount to be added to the wallet
        try:
            request_json = json.loads(request.body)
            amount = request_json['amount']
        except:
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Try retrieving tutor user from logged in user
        tutor = Tutor.getByUsername(request.user.username)
        if tutor == None:
            # Raise bad request response by unknown user type
            raise Exception(3, 'Not a tutor')

        # Check if the wallet has enough amount for transfer
        old_balance = Wallet.getByUserID(tutor.user_profile.user.id).wallet_balance
        if old_balance - amount < 0:
            raise Exception(4, 'Not enough balance')
        # Increment the amount
        new_balance = Wallet.decrementBalance(tutor.user_profile.user.id, amount)
        # Create Transaction record for value transferred
        Transaction.createTransaction(tutor.user_profile.user.id, \
                                        -amount, \
                                        'Value transferred by tutor ' +\
                                        str(tutor) + "("+tutor.username+")")

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "new_balance": new_balance
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

def myTutorTransferMoney(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}
    # Retrieving tutor information
    try:
        # Try retrieving the amount to be added to the wallet
        try:
            request_json = json.loads(request.body)
            amount = request_json['amount']
        except:
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        # Try retrieving admin user from logged in user
        admin = Admin.getByUsername(request.user.username)
        if admin == None:
            # Raise bad request response by unknown user type
            raise Exception(3, 'Not an admin')

        # Check if the wallet has enough amount for transfer
        old_balance = Wallet.getByUserID(-1).wallet_balance
        if old_balance - amount < 0:
            raise Exception(4, 'Not enough balance')
        # Increment the amount
        new_balance = Wallet.decrementBalance(-1, amount)
        # Create Transaction record for value transferred
        Transaction.createTransaction(-1, \
                                        -amount, \
                                        'Value transferred by myTutor admin ' + admin.username)

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "new_balance": new_balance
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