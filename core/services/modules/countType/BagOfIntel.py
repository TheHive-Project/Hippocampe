#!/usr/bin/env python
# -*- coding: utf8 -*-


import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
pathModule = app_dir + 'services/modules/common'
sys.path.insert(0, pathModule)
from ES import getES
from getConf import getHippoConf

import logging
logger = logging.getLogger(__name__)
class BagOfIntel:
	def __init__(self, typeIntel):

		cfg = getHippoConf()
		self.typeIntel = typeIntel
		self.es = getES()
		self.docSearch = dict()
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
		#contains every distinct value from a field
		self.size = int()

	def forgeDocSearch(self):
		#size=0 means "no limit to the number of terms"
		self.docSearch = {
			"aggs": {
				"distinct": {
					"cardinality": {
						"field": self.typeIntel
					}
				}
			}
		}

	def getSize(self):
		self.forgeDocSearch()
		res = self.es.search(index=self.indexNameES, body = self.docSearch)
		#res looks like:
		#{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
		# u'aggregations': {u'distinct': {u'value': 3055}},
		# u'hits': {u'hits': [{u'_id': u'AVOpOpfHUw7jx-ihWUHM',
		#                      u'_index': u'hippocampe',
		#                      u'_score': 1.0,
		#                      u'_source': {u'firstAppearance': u'20160324T162502+0100',
		#                                   u'idSource': u'AVOpOpBxUw7jx-ihWUGb',
		#                                   u'ip': u'144.76.162.245',
		#                                   u'lastAppearance': u'20160324T162502+0100',
		#                                   u'source': u'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist'},
		#                      u'_type': u'abuseFree_zeustrackerIP'},		
		self.size = res['aggregations']['distinct']['value']
		return self.size
