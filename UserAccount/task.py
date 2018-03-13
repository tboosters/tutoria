from UserAccount.models import TimeSlot

from datetime import datetime
import datetime as dt


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
	scheduledBatchCreation()