from Wallet.models import Wallet
from Bookings.models import Booking
from Bookings.models import Transaction

from datetime import datetime
from decimal import *

# End all session tasks
def endSession():
	# Get time of invoke
	now = datetime.now()
	# Get all ending sessions
	ending_sessions = Booking.filterByEndTime(now)
	for session in ending_sessions:
		# Gather information of each party in the booking
		tutor = session.time_slot.tutor
		student = session.student

		if not session.coupon:
			# Calculate the amounts to be transferred
			tutor_fee = round(session.book_fee / Decimal(1.05), 1)
			commission = round(session.book_fee - Decimal(tutor_fee), 1)
			# Transfer Money, log the transaction and send notification
			# Tutor
			tutor_new_balance = Wallet.incrementBalance(tutor.user_profile.user.id, tutor_fee)
			Transaction.createTransaction(-1, \
									-tutor_fee, \
									"Payment to tutor : tutor id = " + str(session.time_slot.tutor.user_profile.user.id) + \
									" time slot = " + str(session.time_slot))
			Transaction.createTransaction(session.time_slot.tutor.user_profile.user.id, \
									tutor_fee, \
									"Tutorial fee from MyTutor : time slot = " + \
									str(session.time_slot))
			print(
				'(Tutor) An amount of tutorial fee has been transferred to you:\n' + \
					'Booking ID: ' + str(session.booking_id) + '\n' + \
					'Transferred Tutorial Fee: ' + str(tutor_fee) + '\n'
					'New wallet balance: ' + str(tutor_new_balance) + '\n'
			)
			# MyTutor
			mytutor_new_balance = Wallet.incrementBalance(-1, commission)
			Transaction.createTransaction(-1, \
									commission, \
									"Commission : student id = " + str(session.student.user_profile.user.id) + \
									" book tutor id = " + str(session.time_slot.tutor.user_profile.user.id) + \
									" time slot = " + str(session.time_slot))
			print(
				'(MyTutor) An amount of commision has been transferred to you:\n' + \
					'Booking ID: ' + str(session.booking_id) + '\n' + \
					'Transferred Commssion: ' + str(commission) + '\n' + \
					'New wallet balance: ' + str(mytutor_new_balance) + '\n'
			)
		else:
			# Calculate the amounts to be transferred
			tutor_fee = session
			commission = 0
			# Transfer Money, log the transaction and send notification
			# Tutor
			tutor_new_balance = Wallet.incrementBalance(tutor.user_profile.user.id, tutor_fee)
			Transaction.createTransaction(-1, \
									-tutor_fee, \
									"Payment to tutor : tutor id = " + str(session.time_slot.tutor.user_profile.user.id) + \
									" time slot = " + str(session.time_slot))
			Transaction.createTransaction(session.time_slot.tutor.user_profile.user.id, \
									tutor_fee, \
									"Tutorial fee from MyTutor : time slot = " + \
									str(session.time_slot))
			print(
				'(Tutor) An amount of tutorial fee has been transferred to you:\n' + \
					'Booking ID: ' + str(session.booking_id) + '\n' + \
					'Transferred Tutorial Fee: ' + str(tutor_fee) + '\n'
					'New wallet balance: ' + str(tutor_new_balance) + '\n'
			)

		# Invite student to make review
		print(
			'(Student) You have completed a tutorial session with the following tutor:\n' + \
			str(session.time_slot.tutor) + '\n' + \
			'Please go to his/her profile to leave a review!\n'
		)
	# Summary of this end all session task
	print(now, ':', len(ending_sessions), 'sessions have ended.\n')

# Scheduled task for time slot creation
def scheduledBatchCreation():
	# Define start time
	start_time = datetime.now()
	start_time = start_time.replace(second=0, microsecond=0)
	# Define end time
	end_time = start_time + dt.timedelta(days=7)
	# Batch create time slots for all tutor
	TimeSlot.rangeCreateAll(start_time, end_time, 'available')

# Shorthand method for easier manual access
def run():
	endSession()
	scheduledBatchCreation()