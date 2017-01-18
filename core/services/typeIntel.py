#!/usr/bin/env python
# -*- coding: utf8 -*-


from  modules.distinct.Field import Field
import logging
logger = logging.getLogger(__name__)
def main():
	logger.info('typeIntel.main launched')
	try:
		response = dict()
		#type service is actually a distinct with the field "coreIntelligence"
		#that's why Field object is used
		allType = Field('coreIntelligence')
		allType.getDistinct()
		response['type'] = allType.distinctList
		logger.info('typeIntel.main end')
		return response
	except Exception as e:
		logger.error('typeIntel.main failed, no idea where it came from...', exc_info = True)
		report = dict()
		report['error'] = str(e)
		return report
if __name__ == '__main__':
	main()
