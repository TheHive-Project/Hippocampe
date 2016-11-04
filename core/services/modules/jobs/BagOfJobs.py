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
pathModule = app_dir + 'services/modules/common'
sys.path.insert(0, pathModule)
from ES import getES
from getConf import getHippoConf

class BagOfJobs:
	"""
		class that will retrieve all jobs
		it seems that a match all query and a scan scroll does not work
		together, that's why a match all query is used
		however only 10 matches are returned by elasticsearch.
		To go beyond that number, the number of document in source index
		is determined and indicated in the match all query	
	"""		
	def __init__(self):
		cfg = getHippoConf()
		self.docSearch = str()
		self.matchResponse = str()
		self.matchDict = dict()
		self.es = getES()
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
		self.typeNameES = cfg.get('elasticsearch', 'typeNameESJobs')
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

	def forgeDocSearchLastJob(self):
		self.docSearch = {
			'query' : {
				'bool' : {
					'must': [
							{
							'match': {
								'status': 'done'
								}
							}
					]
				}
			},
			'size' : 1,
			'sort' : [
				{
					'endTime': {
						'order': 'desc'
					}
				}
			]
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
		#the match all query returns all documents, however there is
		#no key, only value
		#so the field source is setted as key and the all document
		#as value
		for element in self.matchResponse['hits']['hits']:
			self.matchDict[element['_id']] = element['_source']

	def getMatchList(self):
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

	def getLastJob(self):
		self.forgeDocSearchLastJob()
		self.search()	
		report = self.matchResponse['hits']['hits'][0]['_source']
		return report
