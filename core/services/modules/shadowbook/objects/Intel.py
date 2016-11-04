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
from ObjToIndex import ObjToIndex
import os, sys
install_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../../'
getConfPath = install_dir + 'services/modules/common'
sys.path.insert(0, getConfPath)
import getConf
from IndexIntel import IndexIntel
from time import strftime
from NewIntel import NewIntel
class Intel(ObjToIndex):
	def __init__(self, intelligence, cfgPath, idSource):

		#intelligence is a dict:
		#{'blank': '',
		# 'domain': 'uploadersonline.com',
		# u'extra': ['20160229'],
		# 'nextvalidation': '',
		# 'original_reference-why_it_was_listed': 'zeustracker.abuse.ch',
		# 'type': 'zeus'}
		super(Intel, self).__init__()
		self.cfgPath = cfgPath
		conf = getConf.getConf(cfgPath)
		self.indexNameES = conf.get('elasticsearch', 'indexIOC')
		self.typeNameES = conf.get('elasticsearch', 'typeIntel')
		self.idSource = idSource
		self.firstAppearance = str()
		self.lastAppearance = str()
		self.coreIntelligence = conf.get('source', 'coreIntelligence')
		self.dictData = intelligence
		self.source= conf.get('source', 'url')

	def indexIntelInES(self):
		#create the index
		index = IndexIntel(self.cfgPath)
		index.buildConfMapping()
		index.forgeDocMapping()
		index.create()
		#search the coreIntelligence in the index/type ONLY
		nbMatch = self.littleSearch()
		if nbMatch > 0:
			#match, so update last appearance date
			self.updateIntel()
		elif nbMatch == 0:
			#no match, so index
			self.forgeDocIndex()
			self.indexInES()
			#at this point, we are sure that there's no match in the index/type
			#have to check in the whole index hippocampe
			nbMatch = self.bigSearch()
			if nbMatch == 0:
				newIntel = NewIntel(self.coreIntelligence, self.dictData[self.coreIntelligence])
				#indexing the new intel in the index/type hippocampe/new
				newIntel.indexNewIntel()
					
	def bigSearch(self):
		self.es.indices.refresh(index = self.indexNameES)
		#searching in the index hippocampe
		self.resSearch = self.es.search(index = self.indexNameES, body = self.docSearch)
		return self.resSearch['hits']['total']


	def littleSearch(self):
		self.forgeDocSearch()
		return self.search()

	def forgeDocSearch(self):
		self.docSearch = {
			"query": {
				"bool": {
					"must": [
						{
							"match": {
								self.coreIntelligence : self.dictData[self.coreIntelligence] 
							}
						}
					]
				}
			}
		}
	
	def forgeDocUpdate(self):
		self.docUpdate = {
			"script": "ctx._source.lastAppearance = lastAppearance",
			"params": {
				"lastAppearance": self.lastAppearance
			}
		}

	def forgeDocIndex(self):
		#the dictData is already well-formed for index queries
		#however, sometimes, it can have a blank field, which is useless
		#and will be deleted
		self.dictData.pop('blank', None)
		self.docIndex = self.dictData
		#adding the meta data
		#new intelligence, so lastAppearance and first appearance are setted to today
		self.lastAppearance = strftime("%Y%m%dT%H%M%S%z")
		self.firstAppearance = strftime("%Y%m%dT%H%M%S%z")
		self.docIndex ['lastAppearance'] = self.lastAppearance
		self.docIndex['firstAppearance'] = self.firstAppearance
		self.docIndex['idSource'] = self.idSource
		self.docIndex['source'] = self.source

	def updateIntel(self):
		self.lastAppearance = strftime("%Y%m%dT%H%M%S%z")
		self.forgeDocUpdate()
		self.update()
