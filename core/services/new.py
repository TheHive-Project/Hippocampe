#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.new.BagOfNew import BagOfNew
import logging
logger = logging.getLogger(__name__)
def main():
	logger.info('new.main launched')
	try:
		bag = BagOfNew()
		result = bag.getMatchDict()
		logger.info('new.main end')
		return result
	except Exception as e:
		logger.error('new.main failed, no idea where it came from', exc_info = True)
		report = dict()
		report['error'] = str(e)
