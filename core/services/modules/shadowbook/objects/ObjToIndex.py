#!/usr/bin/env python
# -*- coding: utf8 -*-


"""
	This module contains ObjToIndex class.
	======================================
"""

from elasticsearch import Elasticsearch
import os, sys
install_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../../'
getESpath = install_dir + 'services/common'
sys.path.insert(0, getESpath)
from ES import getES
import traceback

class ObjToIndex(object):
	"""
		ObjToIndex class represents any object that can be indexed in elasticsearch.

		This class is kind of an abstract class, because is is the common base
		of Source and Ioc classes.
	"""

	def __init__(self):
		"""
			ObjToIndex class' constructor.
		"""
		
		self.es = getES()
		self.idInES = str()
		self.indexNameES = str()
		self.typeNameES = str()
		self.docIndex = dict()
		self.docSearch = dict()
		self.docUpdate = dict()
		self.resSearch = dict()

	def indexInES(self):
		"""
			Indexes the object in elasticsearch from the docIndex query.

			:raises: RequestError, it can happened when the mappings is misindicated.
					Especially for date type.

		"""
		try:
			qIndex = self.es.index(index = self.indexNameES, doc_type = self.typeNameES, body = self.docIndex)
			self.idInES = qIndex['_id']
		except Exception, e:
		 	exception_type = e.__class__.__name__
		 	output = 'index failed: ' + exception_type
			output = output + '\n' + traceback.format_exc()
			#self.logger.error(output)
			#self.logger.info(self.docIndex)

	def search(self):
		"""
			Searchs the object in elasticsearch from the docSearch query.
			If match, the match's id is setted to idES.

			:return: self.resSearch['hits']['total'] which is the number of matches.
			:rtype: int
		"""
		self.es.indices.refresh(index = self.indexNameES)
		self.resSearch = self.es.search(index = self.indexNameES, doc_type = self.typeNameES, body = self.docSearch)
		if (self.resSearch['hits']['total'] > 0):
			self.idES = self.resSearch['hits']['hits'][0]['_id']
		return self.resSearch['hits']['total']

	def update(self):
		"""
			Updates the object in elasticsearch from the docUpdate query.
		"""
		qUpdate = self.es.update(index = self.indexNameES, doc_type = self.typeNameES, id = self.idES, body = self.docUpdate)
		
