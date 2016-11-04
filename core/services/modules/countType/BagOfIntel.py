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

import logging
logger = logging.getLogger(__name__)
class BagOfIntel:
	def __init__(self, typeIntel):

		cfg = getHippoConf()
		self.typeIntel = typeIntel
		self.es = getES()
		self.docSearch = dict()
		self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
		#contains every distinct value from a field
		self.size = int()

	def forgeDocSearch(self):
		#size=0 means "no limit to the number of terms"
		self.docSearch = {
			"aggs": {
				"distinct": {
					"cardinality": {
						"field": self.typeIntel
					}
				}
			}
		}

	def getSize(self):
		self.forgeDocSearch()
		res = self.es.search(index=self.indexNameES, body = self.docSearch)
		#res looks like:
		#{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
		# u'aggregations': {u'distinct': {u'value': 3055}},
		# u'hits': {u'hits': [{u'_id': u'AVOpOpfHUw7jx-ihWUHM',
		#                      u'_index': u'hippocampe',
		#                      u'_score': 1.0,
		#                      u'_source': {u'firstAppearance': u'20160324T162502+0100',
		#                                   u'idSource': u'AVOpOpBxUw7jx-ihWUGb',
		#                                   u'ip': u'144.76.162.245',
		#                                   u'lastAppearance': u'20160324T162502+0100',
		#                                   u'source': u'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist'},
		#                      u'_type': u'abuseFree_zeustrackerIP'},		
		self.size = res['aggregations']['distinct']['value']
		return self.size
