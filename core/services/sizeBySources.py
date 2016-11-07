#!/usr/bin/env python
# -*- coding: utf8 -*-


from modules.sizeBySources.TypeES import TypeES
import sources
import logging
logger = logging.getLogger(__name__)
def main():
	logger.info('sizeBySources.main launched')
	try:
		sourcesReport = sources.main()
		report = dict()
		for url, dictAttributes in sourcesReport.items():
			typeES = TypeES(dictAttributes['type'])
			report[url] = dict()
			report[url]['size'] = typeES.getSize()
		logger.info('sizeBySources.main end')
		return report
	except Exception as e:
		logger.error('distinct.main failed, no idea where it came from...', exc_info = True)
		response = dict()
		response['error'] = str(e)
		return response

if __name__ == '__main__':
	main()
