#!/usr/bin/env python
# -*- coding: utf8 -*-


import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../'
pathModule = app_dir + 'services/modules/common'
sys.path.insert(0, pathModule)
from ES import getES
from getConf import getHippoConf

import logging
logger = logging.getLogger(__name__)
class Field:
	def __init__(self, field):
		cfg = getHippoConf()
		self.field = field
		self.es = getES()
		self.docSearch = dict()
		self.matchResponse = dict()
		self.indexName = cfg.get('elasticsearch', 'indexNameES')
		#contains every distinct value from a field
		self.distinctList = list()
		#number of distinct values
		self.size = int()

	def forgeDocSearch(self):
		self.docSearch = {
			"size": 0,
			"aggs": {
				"distinct": {
					"terms": {
						"field": self.field,
						"size": self.size
					}
				}
			}
		}



	def forgeDocSearchSize(self):
		self.docSearch = {
			"query": {
				"bool": {
					"must": [
						{"exists": {"field": self.field}}
					]
				}
			},
			"aggs": {
				"distinct": {
					"cardinality": {
						"field": self.field,
					}
				}
			}
		}


	def search(self):
		#request_timeout value to avoid ConnectionTimeout exception
		self.matchResponse = self.es.search(
			index = self.indexName,
			body = self.docSearch,
			request_timeout=60)

	def processMatchResponse(self):
		'''
		raw matchResponse looks like:

		{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
		 u'aggregations': {u'distinct': {u'buckets': [{u'doc_count': 1,
		                                               u'key': u'192.168.1.67'}],
		                                 u'doc_count_error_upper_bound': 0,
		                                 u'sum_other_doc_count': 0}},
		 u'hits': {u'hits': [], u'max_score': 0.0, u'total': 4},
		 u'timed_out': False,
		 u'took': 9}

		'''

		for element in self.matchResponse['aggregations']['distinct']['buckets']:
			self.distinctList.append(element['key'])

	def getSize(self):
		self.forgeDocSearchSize()
		self.search()
		'''
		matchResponse looks like:

		{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
		 u'aggregations': {u'distinct': {u'value': 446}},
		 u'hits': {u'hits': [{u'_id': u'AVmJp90mcUY7Hd0SG5cP',
		                      u'_index': u'hippocampe',
		                      u'_score': 1.0,
		                      u'_source': {u'domain': u'03bbec4.netsolhost.com',
		                                   u'firstAppearance': u'20170110T193316+0100',
		                                   u'idSource': u'AVmJp9c2cUY7Hd0SG5VN',
		                                   u'lastAppearance': u'20170110T193316+0100',
		                                   u'source': u''},
		'''
		self.size = self.matchResponse['aggregations']['distinct']['value']



	def getDistinct(self):
		#since Elasticsearch does not allow the "size=0" parameters
		#we must get the number of all distinct doc according a specific field
		self.getSize()
		#then we execute the search with the exact size
		self.forgeDocSearch()
		self.search()
		self.processMatchResponse()
