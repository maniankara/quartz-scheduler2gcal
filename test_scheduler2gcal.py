#!/usr/bin/env python
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

import unittest
from scheduler2gcal import SchedulerParser
from datetime import timedelta  # Setting Duration


class TestSchedulerParser(unittest.TestCase):
    _basicTime = '10 20 10 * * *'
    _basicTimeGcal = {'recurrence': ['RRULE:FREQ=DAILY;'], 
                        'start': {'dateTime': '2014-06-05T10:20:10+03:00'}, 
                        'end': {'dateTime': None}}

    def setUp(self):
        print 'setup'

    def test_basic_cron_expression(self):	
        parser = SchedulerParser(self._basicTime)
        self.assertEqual(parser.getGcalFormat(), self._basicTimeGcal)

    def test_basic_cron_expression_with_duration(self):	
        parser = SchedulerParser(self._basicTime)
        parser.setDuration(timedelta(hours=2))
        self._basicTimeGcal['end']['dateTime'] = '2014-06-05T12:20:10+03:00'
        self.assertEqual(parser.getGcalFormat(), self._basicTimeGcal)


if __name__ == '__main__':
    unittest.main()    	