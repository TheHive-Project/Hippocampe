#!/usr/bin/env python
# -*- coding: utf8 -*-


from  modules.typeIntel.Type import Type
import logging
logger = logging.getLogger(__name__)
def main():
	logger.info('typeIntel.main launched')
	try:
		response = dict()
		allType = Type()
		allType.getType()
		response['type'] = allType.distinctList
		logger.info('typeIntel.main end')
		return response
	except Exception as e:
		logger.error('typeIntel.main failed, no idea where it came from...', exc_info = True)
		report = dict()
		report['error'] = str(e)
if __name__ == '__main__':
	main()
