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
	This module contains the class IndexSource.
	===========================================
"""
from Index import Index
import os, sys
install_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../../'
getConfPath = install_dir + 'services/modules/common'
sys.path.insert(0, getConfPath)
from getConf import getHippoConf

class IndexSource(Index):
	"""
		IndexIOC class represents an elasticsearch's index. And more precisely 
		an index storing source.

		The class inherits from Index class.
	"""

	def __init__(self, cfgPath):
		"""
			IndexSource class' constructor.

			:param source: shadowBook process's configuration
			:type config: Config object instance
		"""
		conf = getHippoConf()

		super(IndexSource, self).__init__()
		self.indexNameES = conf.get('elasticsearch', 'indexNameES')
		self.typeNameES = conf.get('elasticsearch', 'typeNameESSource')
	

	def forgeDocMapping(self):
		"""
			Forges the elasticsearch's mappings for IndexSource.
		"""
		self.docMapping = {
		        self.typeNameES: {
		            "properties": {
				"lastStatus": {
					"type": "string",
					"index": "not_analyzed"
				},
		                "link": {
		                    "type": "string",
		                    "index": "not_analyzed"
		                },
		                "type": {
		                    "type": "string",
		                    "index": "not_analyzed"
		                },
		                "firstQuery": {
		                    "type": "date",
		                    "format": "basic_date_time_no_millis"
		                },
		                "lastQuery": {
		                    "type": "date",
		                    "format": "basic_date_time_no_millis"
		                },
		                "description": {
		                    "type": "string"
		                },
		                "score": {
		                    "type": "integer"
		                },
		                "coreIntelligence": {
		                    "type": "string"
		                }
		            }
		        }
		    }

	def createIndexSource(self):
		self.forgeDocMapping()
		self.create()
