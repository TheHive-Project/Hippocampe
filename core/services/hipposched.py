#!/usr/bin/env python
# -*- coding: utf8 -*-

#Hippocampe: Intel aggregator
#@author 2015 CERT-BDF <cert@banque-france.fr>
#@see The GNU Public License (GPL)
#
#This file is part of Hippocampe.
#
#Hippocampe is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#Hippocampe is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License along
#with Hippocampe; if not, write to the Free Software Foundation, Inc.,
#59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#or see <http://www.gnu.org/licenses/>.
#

from apscheduler.schedulers.background import BackgroundScheduler
import shadowbook
import logging
logger = logging.getLogger(__name__)
def main(request):
	logger.info('hipposched.main launched')
	try:
		jobId = 'shadowbook'
		time = request['time']
		logger.info('schedule submitted as: ' + str(time))
		#processing time to isolate each field
		tabTime = time.split(' ')
		#tabTime
		#	[0] min
		#	[1] hour
		#	[2] day of month
		#	[3] month
		#	[4] day of week
		sched = BackgroundScheduler()
		#always erase the previous schedule
		#because of replace_existing = True
		#logger.info('creating job')
		sched.add_job(shadowbook.hipposchedVersion,
			'cron',
			minute = tabTime[0],
			hour = tabTime[1],
			day = tabTime[2],
			month = tabTime[3],
			day_of_week = tabTime[4],
			replace_existing = True,
			id = jobId)
		sched.start()
		logger.info('job succesfully schedulled as: ' + str(time))
		report = dict()
		report['schedule'] = time
		logger.info('hipposched.main end')
		return report
	except Exception as e:
		logger.error('hipposched.main failed, no idea where it came from', exc_info = True)
		report = dict()
		report['error'] = str(e)
		return report


