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

class SchedulerParser:
	def __init__(self, string):
		if string == None or len(string) < 1: raise NameError('String cannot be empty')
		self.datetime = None # Datetime Object
		try:
			quartzCronEntry = string.split()
			if len(quartzCronEntry) != 6: raise NameError('Wrong cron entry, check usage')
			second, minute, hour, day, month, year = quartzCronEntry 
			self.datetime = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
		except Exception, e:
			print "Error occured:", e
			raise e

	def getIsoFormat(self):
		return self.datetime.isoformat('T')