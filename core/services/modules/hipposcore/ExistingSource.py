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
