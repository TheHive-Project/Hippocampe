#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.countType.BagOfIntel import BagOfIntel
import typeIntel
import logging
logger = logging.getLogger(__name__)
def main():
	logger.info('sizeByType.main launched')
	try:
		report = dict()
		#retrieving all intelligences's types available
		typeReport = typeIntel.main()
		for typeIntelligence in typeReport['type']:
			bagOfIntel = BagOfIntel(typeIntelligence)
			size = bagOfIntel.getSize()
			report[typeIntelligence] = dict()
			report[typeIntelligence]['size'] = size
		logger.info('sizeByType.main end')
		return report
	except Exception as e:
		logger.error('sizeByType.main failed, no idea where it came from...', exc_info = True)
		response = dict()
		response['error'] = str(e)
		return response

if __name__ == '__main__':
	main()
