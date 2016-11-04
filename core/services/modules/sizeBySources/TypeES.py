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
		
