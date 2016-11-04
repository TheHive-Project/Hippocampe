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
