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
import argparse
from quartzscheduler2py import SchedulerParser


parser = argparse.ArgumentParser(description='Example Quartz Scheduler parser')
parser.add_argument('string', metavar='<secs> <minutes> <hours> <day of month> <month> <day of week> <year>', type=str, nargs=1,
                   help='string in Quartz Scheduler crontab syntax')

args = parser.parse_args()
#print(args.string)

parser = SchedulerParser(args.string[0])
print parser.getGcalFormat()