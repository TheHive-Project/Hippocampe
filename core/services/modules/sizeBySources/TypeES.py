#!/usr/bin/env python
# -*- coding: utf8 -*-


"""
	This module contains ObjToIndex class.
	======================================
"""

import os, sys
install_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
getESpath = install_dir + 'services/modules/common'
sys.path.insert(0, getESpath)
from ES import getES
from getConf import getHippoConf

class TypeES(object):
	"""
		ObjToIndex class represents any object that can be indexed in elasticsearch.

		This class is kind of an abstract class, because is is the common base
		of Source and Ioc classes.
	"""

	def __init__(self, typeNameES):
		"""
			ObjToIndex class' constructor.
		"""
		cfg = getHippoConf()
		self.es = getES()
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
		self.typeNameES = typeNameES
		self.docSearch = dict()
		self.size = int()

	def forgeDocSearch(self):
		self.docSearch = {
			'query' : {
				'match_all' : {}
			}
		}

	def getSize(self):
		self.forgeDocSearch()
		res = self.es.count(index=self.indexNameES, doc_type=self.typeNameES, body = self.docSearch)
		#res looks like:
		#{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5}, u'count': 45}
		self.size = res['count']
		return self.size
		
