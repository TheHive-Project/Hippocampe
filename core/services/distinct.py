#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.distinct.Field import Field
import logging
logger = logging.getLogger(__name__)
def main(jsonRequest):
	logger.info('distinct.main launched')
	response = dict()
	#jsonRequest looks like:
	#{
	#	'field': ['ip', 'domain', 'url']
	#}
	try:
		for field in jsonRequest['field']:
			logger.info('All %s requested', field)
			fieldToRequest = Field(field)
			fieldToRequest.getDistinct()
			response[field] = fieldToRequest.distinctList
		logger.info('distinct.main end')
		return response
	except Exception as e:
		logger.error('distinct.main failed, no idea where it came from...', exc_info = True)
		response['error'] = str(e)
		return response
if __name__ == '__main__':
	main()
