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

	def forgeDocSearch(self):
		#size=0 means "no limit to the number of terms"
		self.docSearch = {
			"aggs": {
				"distinct": {
					"terms": {
						"field": self.field,
						"size": 0
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
		{
		    "_shards": {
		        "failed": 0,
		        "successful": 5,
		        "total": 5
		    },
		    "aggregations": {
		        "distinct": {
		            "buckets": [
		                {
		                    "doc_count": 3,
		                    "key": "http://larlingslotsen.se/wp-includes/css/tracking.php?l=_JeHFUq_VJOXK0QWHtoGYDw_Product-UserID&amp;userid=abuse@huawei.com"
		                },
		                {
		                    "doc_count": 2,
		                    "key": "http://aaronmaxdesign.com/wordpress/wp-content/netvigator/update/ainput/id.php?l=_JeHFUq_VJOXK0QWHtoGYDw_Product-UserID&amp;userid=abuse@aol.com"
		                },
		                {
                    "doc_count": 15882,
                    "key": 1359248160,
                    "key_as_string": "81.4.123.32"
                },

		'''
		if self.field != 'ip':
			for element in self.matchResponse['aggregations']['distinct']['buckets']:
				self.distinctList.append(element['key'])
		else:
			#if we are looking for all ips, the key is different
			for element in self.matchResponse['aggregations']['distinct']['buckets']:
				self.distinctList.append(element['key_as_string'])

	def getDistinct(self):
		self.forgeDocSearch()
		self.search()
		self.processMatchResponse()
