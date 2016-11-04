#!/usr/bin/env python
# -*- coding: utf8 -*-

#Hippocampe: Intel aggregator
#@author 2015 CERT-BDF <cert@banque-france.fr>
#@see The GNU Public License (GPL)
#
#This file is part of Hippocampe.
#
#Hippocampe is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#Hippocampe is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License along
#with Hippocampe; if not, write to the Free Software Foundation, Inc.,
#59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#or see <http://www.gnu.org/licenses/>.
#

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
