#!/usr/bin/env python
# -*- coding: utf8 -*-


from elasticsearch import Elasticsearch
import os
import sys
install_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../'
pathModule = install_dir + 'modules/ES'
sys.path.insert(0, pathModule)
from ES import getES

class ExistingSource:
	"""
		ExistingSource represents a source indexed in elasticsearch
		It is constructed with the id of the source document in elasticsearch
	"""
	def __init__(self, idSource):
		self.idSource = idSource
		self.docMatch = str()
		self.matchResponse = str()
		self.scoreSource = float()
		self.es = getES() 

	def forgeDocMatch(self):
		"""
			Forging the document to search the source, according to its
			id in elasticsearch
		"""
		self.docMatch = {
			'query' : {
				'bool' : {
					'must' : [
						{'match' : {'_id' : self.idSource}}
						]
					}
				}
			}

	def search(self):
		"""
			Searching the document
		"""
		self.matchResponse = self.es.search(body = self.docMatch)
		if self.matchResponse['hits']['total'] > 0 :
			return True
		elif self.matchResponse['hits']['total'] == 0:
			return False

	def processMatchResponse(self):
		"""
			Retrieving the source's score
		"""
		self.scoreSource = self.matchResponse['hits']['hits'][0]['_source']['score']

	def getScore(self):
		return self.scoreSource
