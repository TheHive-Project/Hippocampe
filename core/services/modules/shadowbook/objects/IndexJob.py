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

from Index import Index
import os, sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../../'
getConfPath = app_dir + 'services/modules/common'
sys.path.insert(0, getConfPath)
from getConf import getHippoConf
from itertools import izip_longest
import ast
import logging

logger = logging.getLogger(__name__)
class IndexJob(Index):
	"""
		IndexIOC class represents an elasticsearch's index. And more precisely 
		an index storing IOC.

		The class inherits from Index class.
	"""

#	def __init__(self, cfgPath):
	def __init__(self):

		super(IndexJob, self).__init__()
		cfg = getHippoConf()
		self.indexNameES =  cfg.get('elasticsearch', 'indexNameES')
		self.typeNameES = cfg.get('elasticsearch', 'typeNameESJobs')

		#the mapping has to be indicated at the creation of the index
		#the confMapping, is the mapping indicated in conf file for each field
		#it has to be parsed bellow
		self.confMapping = dict()

	def forgeDocMapping(self):
		"""
			Forges the elasticsearch's mappings for IndexIOC.
		"""
		#mapping for the meta-data
		self.docMapping = {
			self.typeNameES : {
#				"dynamic": "strict",
				"properties" : {
#					"report": {
#						"type": "date",
#						"index": "not_analyzed"
#					},
					"status": {
						"type": "string",
						"index": "not_analyzed"
					},
					"startTime": {
						"type": "date",
						"format": "basic_date_time_no_millis"
					},
					"endTime": {
						"type": "date",
						"format": "basic_date_time_no_millis"
					},
					"duration": {
						"type": "float"
					}				 
				}
			}
		}

	def createIndexJob(self):
		self.forgeDocMapping()
		self.create()
