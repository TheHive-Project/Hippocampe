#!/usr/bin/env python
# -*- coding: utf8 -*-


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
