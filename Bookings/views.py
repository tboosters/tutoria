#  -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

import decimal

from datetime import datetime
import datetime as dt

from Bookings.models import Booking
from Bookings.models import Coupon
from Bookings.models import Transaction
from UserAccount.models import TimeSlot
from UserAccount.models import UserProfile
from UserAccount.models import University
from Wallet.models import Wallet

import json

# Views for Bookings App

# Verify coupon by http request
def verifyCoupon(request):
    # Retrieve coupon code entered by user
    couponCode = request.GET.get('couponCode', '')
    # Check coupon validity
    message = {
        "errno": 0,
        "msg": "Request succeeded!",
        "data": {
            "is_valid": Coupon.isValid(couponCode)
        }
    }
    # Render response
    return JsonResponse(message)

# List all bookings for a particular user
def listBookings(request):
    # Initialize message variables
    errno = -1
    msg = ''
    data = {}

    # Retrieve request information
    user_id = request.user.id

    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            is_student = request_json['is_student']
            is_tutor = request_json['is_tutor']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        if user_id == '':
            # Raise bad request response by getting empty user id
            raise Exception(3, 'Interievable user id')

        bookingsAsStudent = []
        bookingsAsTutor = []
        if is_student:
            # Retrieve bookings booked by student
            bookingsData = Booking.filterByStudentUserID(user_id)
            for b in bookingsData: 
                if b.cancelled:
                    continue    
                info = {
                    "id": b.booking_id,
                    "start_time": b.time_slot.start_time,
                    "end_time": b.time_slot.end_time,
                    "tutor_type": b.time_slot.tutor.tutor_type,
                    "tutor_first_name": b.time_slot.tutor.first_name,
                    "tutor_last_name": b.time_slot.tutor.last_name,
                    "tutor_id": b.time_slot.tutor.tutor_id,
                    "tutor_university": b.time_slot.tutor.university.name,
                    "tutor_email": b.time_slot.tutor.email,
                    "tutor_phone_number": b.time_slot.tutor.phone_number,
                    "fee": b.book_fee
                }
                bookingsAsStudent.append(info)

        if is_tutor:
            # Retrieve bookings bookina a tutor
            bookingsData = Booking.filterByTutorUserID(user_id)
            for b in bookingsData:
                if b.cancelled:
                    continue 
                info = {
                    "id": b.booking_id,
                    "start_time": b.time_slot.start_time,
                    "end_time": b.time_slot.end_time,
                    "student_first_name": b.student.first_name,
                    "student_last_name": b.student.last_name,
                    "student_phone_number": b.student.phone_number,
                    "student_email": b.student.email,
                    "fee": b.book_fee
                }
                bookingsAsTutor.append(info)
            
        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "bookings_as_student": bookingsAsStudent,
            "bookings_as_tutor": bookingsAsTutor
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

def createBooking(request):
    errno = -1
    msg = ''
    data = []

    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            tutor_id = request_json['tutor_id']
            fee = request_json['fee']
            coupon_code = request_json['coupon_code']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        student_user_id = request.user.id
        if student_user_id == '':
            # Raise bad request response by getting empty user id
            raise Exception(3, 'Interievable user id')

        if coupon_code != "" and not Coupon.isValid(coupon_code):
            # Raise bad request response by invalid coupon
            raise Exception(4, 'Invalid coupon')

        # Define start and end time for the the booking
        start_time = datetime.strptime(request_json['start_time'][:24], '%a %b %d %Y %H:%M:%S')
        end_time = datetime.strptime(request_json['end_time'][:24], '%a %b %d %Y %H:%M:%S')
        
        # Check pre-conditions
        conditions = Booking.checkPreConditions(student_user_id, tutor_id, fee, start_time, end_time)
        if conditions['errno'] != 0:
            # Raise bad request response by unmet pre-conditions
            raise Exception(conditions['errno'], conditions['msg'])

        # Calculate fee with commission
        if coupon_code == "":
            fee = round(fee * decimal.Decimal(1.05), 1)
        else:
            fee = fee

        # Create new book record
        new_balance = Wallet.decrementBalance(student_user_id, fee)
        time_slot = TimeSlot.markCalendar(tutor_id, start_time, end_time, 'available', 'booked')
        booking_id = Booking.createBooking(student_user_id, fee, time_slot, coupon_code)

        # Create transaction record for student
        Transaction.createTransaction(student_user_id, \
                                -fee, \
                                "Booking Payment to MyTutor : time slot = " + \
                                str(time_slot))
        # Create transaction record for mytutor
        Transaction.createTransaction(-1, \
                                fee, \
                                "Pending fee : student id = " + str(student_user_id) + \
                                " pay for tutor id = " + str(tutor_id) + \
                                " time slot = " + str(time_slot))

        # Send 'email' to student
        print('(Student) You have booked a session:\n' + \
                'Booking ID: ' + str(booking_id) + '\n' + \
                'Start Time: ' + str(start_time) + '\n' + \
                'End Time: ' + str(end_time) + '\n' + \
                'Tutorial Fee: ' + str(fee) + '\n' + \
                'Wallet Remaining Balance: ' + str(new_balance) + '\n'
        )
        # Send 'email' to tutor
        print('(Tutor) A session is booked:\n' + \
                'Booking ID: ' + str(booking_id) + '\n' + \
                'Start Time: ' + str(start_time) + '\n' + \
                'End Time: ' + str(end_time) + '\n' + \
                'Tutorial Fee: ' + str(fee) + '\n'
        )

        # Filling response body
        errno = 0
        msg = "Request succeeded"
        data = {
            "booking_id": booking_id
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

def removeBooking(request):
    errno = -1
    msg = ''
    data = []

    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            booking_id = request_json['booking_id']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        student_id = request.user.id
        if student_id == '':
            # Raise bad request response by getting empty user id
            raise Exception(3, 'Interievable user id')

        # Retrieve booking object
        bookingObject = Booking.getBooking(booking_id)
        if not bookingObject:
            # Raise bad request response by in valid booking id
            raise Exception(4, 'Invalid booking id')

        # If a booking can be retrieved...
        tutor_id = bookingObject.time_slot.tutor.tutor_id
        start_time = bookingObject.time_slot.start_time
        end_time = bookingObject.time_slot.end_time
        fee = bookingObject.book_fee
        newBalance = -1

        # Checking 24 hours time
        now = datetime.now()
        beforeStart = start_time + dt.timedelta(hours=-24)
        if now >= beforeStart:
            # Raise bad request response by booking falling in 24 hour range
            raise Exception(5, 'Booking cannot be cancelled within 24 hours before start time')

        # Mark the booking as canceled
        success = Booking.removeBooking(student_id, booking_id)
        if success == False:
            # Raise bad request response by unable to remove booking
            raise Exception(6, 'Failed to remove booking record')

        # Mark time slot as available and retrieve corrisponding time slot
        time_slot = TimeSlot.markCalendar(tutor_id, start_time, end_time, 'booked', 'available')
        if not time_slot:
            # Raise bad request response by release time slot
            raise Exception(7, 'Fail to release available time slot')

        # If removal succeeded, add the fee paid by the student back to his wallet
        new_balance = Wallet.incrementBalance(student_id, fee)

        # Create transaction record for student
        Transaction.createTransaction(student_id, \
                                        fee, \
                                        "Cancel Refund from MyTutor : time slot = " + \
                                        str(time_slot))
        # Create transaction record for mytutor
        Transaction.createTransaction(-1, \
                                        -fee, \
                                        "Cancel Session : student id = " + str(student_id) + \
                                        " cancel tutor id = " + str(tutor_id) + \
                                        " time slot = " + str(time_slot))

        # Send email to student
        print('(Student) You have cancelled a session:\n' + \
                'Booking ID: ' + str(booking_id) + '\n' + \
                'Start Time: ' + str(start_time) + '\n' + \
                'End Time: ' + str(end_time) + '\n' + \
                'Refund Fee: ' + str(fee) + '\n' + \
                'Wallet Remaining Balance: ' + str(new_balance) + '\n'
        )
        # Send email to tutor
        print('(Tutor) A session is cancelled:\n' + \
                'Booking ID: ' + str(booking_id) + '\n' + \
                'Start Time: ' + str(start_time) + '\n' + \
                'End Time: ' + str(end_time) + '\n' + \
                'Tutorial Fee: ' + str(fee) + '\n'
        )

        # Filling response body
        errno = 0
        msg = "Request succeeded"
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

def listTransactions(request):
    errno = -1
    msg = ''
    data = []

    try:
        try:
            # Retrieve request information 
            request_json = json.loads(request.body)
            days = request_json['days']
        except:
            # Raise bad request response
            raise Exception(1, 'Bad request')

        if not request.user.is_authenticated():
            # Raise bad request response by user not logged in
            raise Exception(2, 'User not logged in')

        user_id = request.user.id
        if user_id == '':
            # Raise bad request response by getting empty user id
            raise Exception(3, 'Interievable user id')

        # Retrieve the transaction records
        transactions = Transaction.retrieveTransactions(user_id, days)
        errno = 0
        msg = 'Request succeeded'
        # Generate data
        for t in transactions:
            info = {
                "amount": t.amount,
                "time": t.time,
                "detail": t.detail
            }
            data.append(info)
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
