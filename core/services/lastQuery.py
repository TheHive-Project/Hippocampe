#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.common.ES import getES
import sources
import logging
logger = logging.getLogger(__name__)
def main():
	logger.info('lastQuery.main launched')
	try:
		report = dict()
		#retrieving sources report
		sourcesReport = sources.main()
		#isolating lastQuery date for every type under hippocampe index
		for url, dictAttributes in sourcesReport.items():
			report[url] = dict()
			report[url]['lastQuery'] = dictAttributes['lastQuery']
		logger.info('lastQuery.main end')
		return report
	except Exception as e:
		logger.error('distinct.main failed, no idea where it came from...', exc_info = True)
		response = dict()
		response['error'] = str(e)
		return response

if __name__ == '__main__':
	main()
