#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.sources.BagOfSources import BagOfSources
import logging
logger = logging.getLogger(__name__)

def main():
	logger.info('sources.main launched')
	try:
		bag = BagOfSources()
		result = bag.getMatchList()
		logger.info('sources.main end')
		return result
	except Exception as e:
		logger.error('sources.main failed, no idea where it came from...', exc_info = True)
		report = dict()
		report['error'] = str(e)
		return report
