#!/usr/bin/env python
# -*- coding: utf8 -*-


import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
pathModule = app_dir + 'services/modules/common'
sys.path.insert(0, pathModule)
from ES import getES
from getConf import getHippoConf

class BagOfSources:
	"""
		class that will retrieve all sources
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
		self.typeNameES = 'source'
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
		#the match all query returns all documents, however there is
		#no key, only value
		#so the field source is setted as key and the all document
		#as value
		for element in self.matchResponse['hits']['hits']:
			self.matchDict[element['_source']['link']] = element['_source']

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
