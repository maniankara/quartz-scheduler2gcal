# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Eday Solutions.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# References: 
# 	- Python2 datetime: https://docs.python.org/2/library/datetime.html#datetime-objects
# 	- Quartz scheduler: http://quartz-scheduler.org/documentation/quartz-2.2.x/tutorials/crontrigger

from datetime import datetime
#  Managing time zones
from datetime import tzinfo 
from datetime import timedelta
import time

import traceback





class SchedulerParser:


	def __init__(self, string):
		# gcalevent Template
		self._gcalevent = {           
		    'start': {
		      'dateTime': None
		    },
		    'end': {
		      'dateTime': None
		    },
			'recurrence': [
		  #"RRULE:FREQ=WEEKLY;UNTIL=20110701T160000Z",
		  # EXRULE, RDATE, EXDATE...
			]
		}	
		self._timeDelta = None # To calculate the start time
		if string == None or len(string) < 1: raise NameError('String cannot be empty')


		try:
			# Convert the given cli params as a dict
			quartzCronEntry = string.split()
			if len(quartzCronEntry) != 6: raise NameError('Wrong cron entry, check usage')
			self._cronEntry = {'second':quartzCronEntry[0],
							'minute':quartzCronEntry[1],
							'hour':quartzCronEntry[2],
							'day':quartzCronEntry[3],
							'month':quartzCronEntry[4],
							'year':quartzCronEntry[5]
							}

		except Exception, e:
			print "Error occured:", e
			traceback.print_exc()
			raise e

	# Optional definition to set the endtime
	def setDuration(self, timeDelta):
		self._timeDelta = timeDelta

	# Returns a compatible google calender format
	def getGcalFormat(self):
		_cd = CronDepersonalizer()
		_cd.depersonalize(self._cronEntry)
		self._gcalevent['start']['dateTime'] = _cd.startDateTime.isoformat('T')
		if self._timeDelta: self._gcalevent['end']['dateTime'] = (_cd.startDateTime + self._timeDelta).isoformat('T') 
		if _cd.rrule: self._gcalevent['recurrence'].append(_cd.rrule) 		
		return self._gcalevent



class CronDepersonalizer:
	def __init__(self):
		self.rrule 			= None
		self.startDateTime 	= None

	def depersonalize(self, cronEntry):
		freq = None
		now = datetime.now()
		for entity, value in cronEntry.items():
			try:
				cronEntry[entity] = int(value)
			except Exception:
				if entity in ['second', 'minute', 'hour']:
					raise NameError("Only numbers allowed for seconds, minute and hour entries")
				elif value in ['*', '?']:
					freq 		= 'DAILY'
					if entity 	== 'year':
						cronEntry[entity] = now.year
					elif entity == 'month':
						cronEntry[entity] = now.month
					elif entity == 'day':
						cronEntry[entity] = now.day
				else:
					raise NameError("Only * and ? cron expressions are implemented")

		if freq != None: self.rrule = "RRULE:FREQ=%s;" % freq
		self.startDateTime = datetime(cronEntry['year'], cronEntry['month'],cronEntry['day'],
			cronEntry['hour'], cronEntry['minute'], cronEntry['second'], tzinfo=LocalTimeZone())
		print "Done personalizartion"

# Handling Timezone, better not to rely on pytz
class LocalTimeZone(tzinfo):
	def utcoffset(self,dt): 
		return timedelta(hours=2) + self.dst()

	def tzname(self,dt): 
		return "GMT +5" 

	def dst(self, dt=None): 
		delta = dt if dt != None else time.daylight
		return timedelta(hours=delta)	
