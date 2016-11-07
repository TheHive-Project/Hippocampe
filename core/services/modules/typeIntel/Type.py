#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
pathModule = app_dir + 'services/modules/common'
sys.path.insert(0, pathModule)
from ES import getES
from getConf import getHippoConf

class Type:
	def __init__(self):
		cfg = getHippoConf()
		#each ioc has a field named coreIntelligence wiche indicates the ioc's type
		self.field = 'coreIntelligence'
		self.es = getES()
		self.docMatch = dict()
		self.matchResponse = dict()
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
		#contains every distinct value from a field
		self.distinctList = list()

	def forgeDocMatch(self):
		#size=0 means not limit the number of terms
		self.docMatch = {
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
			index = self.indexNameES,
			body = self.docMatch,
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

	def getType(self):
		self.forgeDocMatch()
		self.search()
		self.processMatchResponse()
