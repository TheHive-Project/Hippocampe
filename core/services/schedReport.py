#!/usr/bin/env python
# -*- coding: utf8 -*-


import sources
import dateutil.parser
import time
from modules.common.getConf import getHippoConf
import logging
from configparser import NoOptionError, NoSectionError
logger = logging.getLogger(__name__)

def main():
	logger.info('schedReport.main launched')

	cfg = getHippoConf()
	#threshold defined in conf file
	#by default equals to 7
	#if a source is not querryed for 7 days or more, an alert is sent

	#JSON dict reporting data freshness for all sources
	report = dict()

	try:
		threshold = cfg.getint('schedReport', 'threshold')

		#retrieve all source
		dictSource = sources.main()
		#dictSource looks like:
		#{
		#  "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist": {
		#    "coreIntelligence": "ip",
		#    "description": "The Feodo Tracker Feodo IP Blocklist contains IP addresses (IPv4) used as C&C communication channel by the Feodo Trojan. This lists contains two types of IP address: Feodo C&C servers used by version A, version C and version D of the Feodo Trojan (these IP addresses are usually compromised servers running an nginx daemon on port 8080 TCP or 7779 TCP that is acting as proxy, forwarding all traffic to a tier 2 proxy node) and Feodo C&C servers used by version B which are usually used for the exclusive purpose of hosting a Feodo C&C server.",
		#    "firstQuery": "20160222T233556+0100",
		#    "lastQuery": "20160224T134833+0100",
		#    "score": -100,
		#    "source": "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist",
		#    "type": "source"
		#  }
		#}
		if 'error' in dictSource:
			logger.error('sources.main for schedReport.main failed')
			return dictSource

		now = time.strftime("%Y%m%dT%H%M%S%z")

		#converting to dateutil
		now = dateutil.parser.parse(now)
		for url, dictData in dictSource.items():
			report[url] =dict()
			lastQuery =dictData['lastQuery']
			lastQuery = dateutil.parser.parse(lastQuery)
			
			#delta is the time difference in days between now and lastQuery
			delta = (now - lastQuery).days
			#converting in hours
			delta = delta * 24
			if (delta > threshold):
				report[url]['schedReport'] = 'NOK'
			else:
				report[url]['schedReport'] = 'OK'
		logger.info('schedReport.main end')
		return report
	except NoSectionError as e:
		logger.error('parsing hippo.conf failed', exc_info = True)
		report['error'] = str(e)
	except NoOptionError as e:
		logger.error('parsing hippo.conf failed', exc_info = True)
		report['error'] = str(e)
	except Exception as e:
		logger.error('schedReport.main failed, no idea where it came from...', exc_info = True)
		report['error'] = str(e)
	
if __name__ == '__main__':
	main()
			
