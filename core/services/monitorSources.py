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

import lastQuery, schedReport, sizeBySources, freshness, lastStatus
import logging
logger = logging.getLogger(__name__)
from copy import deepcopy

def main():
	logger.info('monitorSources.main launched')
	try:
		lastQueryReport = lastQuery.main()
		sched_Report = schedReport.main()
		sizeBySourceReport = sizeBySources.main()
		freshnessReport = freshness.main()
		lastStatusReport = lastStatus.main()
		
		report = dict_merge(lastQueryReport, sched_Report)	
		report = dict_merge(report, sizeBySourceReport)	
		report = dict_merge(report, freshnessReport)
		report = dict_merge(report, lastStatusReport)
		
		logger.info('monitorSources.main end')
		return report
	except Exception as e:
		logger.error('monitorSources.main failed, no idea where it came from...', exc_info = True)
		response = dict()
		response['error'] = str(e)
		return response

def dict_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

if __name__ == '__main__':
	main()
