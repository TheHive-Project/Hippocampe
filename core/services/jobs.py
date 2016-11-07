#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.jobs.BagOfJobs import BagOfJobs
import logging
logger = logging.getLogger(__name__)

def main():
	logger.info('jobs.main launched')
	try:
		bag = BagOfJobs()
		result = bag.getMatchList()
		logger.info('jobs.main end')
		return result
	except Exception as e:
		logger.error('jobs.main failed, no idea where it came from...', exc_info = True)
		report = dict()
		report['error'] = str(e)
		return report
