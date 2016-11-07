#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../'
modulePath = app_dir + 'services/modules/common'
sys.path.insert(0, modulePath)
from ES import getES
from getConf import getHippoConf

class ObjToEnrich:
	def __init__(self, typeIntel, ioc):
		cfg = getHippoConf()
		self.typeIntel = typeIntel
		self.value = ioc
		self.docMatch = str()
		self.matchResponse = str()
		self.matchList = list()
		self.es = getES()

		#data stored in index hippocampe, so search is only in this index
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES') 

	def forgeDocMatch(self):
		self.docMatch = {
			 'query' : {
				 'bool' : {
					 'must' : [
					 {'match' : {self.typeIntel : self.value}}
					 ]
				 }
			 }
		 }

	def forgeDocMatchInIpNetwork(self):
		self.docMatch = {
			"query" : {
				"bool" : {
					"must": [
					{"range" :  {"ip.from" : {"from": "0.0.0.0", "to" : self.value}}},
					{"range" : {"ip.to" : {"from" : self.value, "to" : "255.255.255.255"}}}
					]
				}
			}
		}
	
	
	def search(self):
		self.matchResponse = self.es.search(
				index = self.indexNameES,
				body = self.docMatch)
		if self.matchResponse['hits']['total'] > 0:
			return True
		elif  self.matchResponse['hits']['total'] == 0:
			return False
	
	def processMatchResponse(self):
		for element in self.matchResponse['hits']['hits']:
			self.matchList.append(element['_source'])

	def getDetailsIP(self):
		self.forgeDocMatchInIpNetwork()
		if self.search():
			self.processMatchResponse()
			return self.matchList
		else:
			return []
	 
	def getDetails(self):
		self.forgeDocMatch()
		if self.search():
			self.processMatchResponse()
			return self.matchList
		else:
			return []
