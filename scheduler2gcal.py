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

import traceback


_GCALEVENT = {
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



class SchedulerParser:
	def __init__(self, string):
		if string == None or len(string) < 1: raise NameError('String cannot be empty')
		self._timeDelta = None # To calculate the start time

		try:
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

	def setDuration(self, timeDelta):
		self._timeDelta = timeDelta

	def getGcalFormat(self):
		_cd = CronDepersonalizer()
		_cd.depersonalize(self._cronEntry)
		_GCALEVENT['start']['dateTime'] = _cd.startDateTime.isoformat('T')
		if self._timeDelta: _GCALEVENT['end']['dateTime'] = (_cd.startDateTime + self._timeDelta).isoformat('T') 
		if _cd.rrule: _GCALEVENT['recurrence'].append(_cd.rrule) 		
		return _GCALEVENT



class CronDepersonalizer:
	def __init__(self):
		self.rrule = None
		self.startDateTime = None

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
					freq = 'DAILY'
					if entity == 'year':
						cronEntry[entity] = now.year
					elif entity == 'month':
						cronEntry[entity] = now.month
					elif entity == 'day':
						cronEntry[entity] = now.day
				else:
					raise NameError("Only * and ? cron expressions are implemented")

		if freq != None: self.rrule = "RRULE:FREQ=%s;" % freq
		self.startDateTime = datetime(cronEntry['year'], cronEntry['month'],cronEntry['day'],
			cronEntry['hour'], cronEntry['minute'], cronEntry['second'])
		#if cronEntry,
		#	cronEntry['hour'], cronEntry['minute'], cronEntry['second']).isoformat('T')
		print "Done personalizartion"