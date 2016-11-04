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
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
pathModule = app_dir + 'services/modules/common/ES'
sys.path.insert(0, pathModule)
from ES import getES
from getConf import getHippoConf

pathModule = app_dir + 'services'
sys.path.insert(0, pathModule)
import typeIntel

class BagOfNew:
	def __init__(self):
		cfg = getHippoConf()
		self.docSearch = str()
		self.matchResponse = str()
		self.matchDict = dict()
		self.es = getES()
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
		self.typeNameES = cfg.get('elasticsearch', 'typeNameESNew')
		self.nbDoc = int() 


	def forgeDocSearch(self):
		self.docSearch = {
			'query' : {
				'match_all' : {}
			}
		}

	def forgeDocSearchAll(self):
		self.docSearch = {
			'size': self.nbDoc,
			'query' : {
				'match_all' : {}
			}
		}

    	def search(self):
    	    self.matchResponse = self.es.search(
    	        body = self.docSearch, index= self.indexNameES,
		doc_type = self.typeNameES)
    	    if self.matchResponse['hits']['total'] > 0:
    	        return True
    	    elif  self.matchResponse['hits']['total'] == 0:
    	        return False

	def processMatchResponse(self):
                #{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
                # u'hits': {u'hits': [{u'_id': u'AVMLH_9WhQvX6w62oQJL',
                #                      u'_index': u'hippocampe',
                #                      u'_score': 1.0,
                #                      u'_source': {u'intelligence': u'113.53.234.218',
                #                                   u'originalId': u'AVMLH_9LhQvX6w62oQJK',
                #                                   u'typeIoc': u'ip'},
                #                      u'_type': u'new'},
                #                     {u'_id': u'AVMLH_ynhQvX6w62oQIj',
                #                      u'_index': u'hippocampe',
                #                      u'_score': 1.0,
                #                      u'_source': {u'intelligence': u'google.com',
                #                                   u'originalId': u'AVMLH_yZhQvX6w62oQIi',
                #                                   u'typeIoc': u'domain'},

		for element in self.matchResponse['hits']['hits']:
			self.matchDict[element['_id']] = element['_source']

	def getMatchDict(self):
		#because elasticsearch only returns 10 results
		#w have to search in two phase, first determine the nb of docs
		#and then retrieve all docs
		#matchAll query
		self.forgeDocSearch()
		#retrieve nb doc
		res = self.es.count(index=self.indexNameES, doc_type=self.typeNameES, body = self.docSearch)
		#res looks like:
		#{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5}, u'count': 45}
		self.nbDoc = res['count']
		self.forgeDocSearchAll()
		self.search()
		self.processMatchResponse()
		return self.matchDict	
