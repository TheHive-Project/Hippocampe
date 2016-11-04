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
        This module contains Ioc class.
        ===============================
"""
from ObjToIndex import ObjToIndex
from IndexNew import IndexNew
import os, sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../../'
getConfPath = app_dir + 'services/modules/common'
sys.path.insert(0, getConfPath)
from getConf import getHippoConf

class NewIntel(ObjToIndex):
        """

                It inherits from ObjToIndex class.
        """

        def __init__(self, typeIntel, intelligence):
                """
                        Ioc class' constructor.

                        :param config: Config object that contains informations about the ioc.
                        :type config: Config object instance.
                        :param source: Ioc's Source object.
                        :type source: Source object instance.
                """

                super(NewIntel, self).__init__()
		cfg = getHippoConf()
                self.indexNameES = cfg.get('elasticsearch', 'indexNameES')
                self.typeNameES = 'new'
		self.typeIntel = typeIntel
		self.intelligence = intelligence

	def forgeDocIndex(self):
		self.docIndex['typeIntel'] = self.typeIntel
		self.docIndex['intelligence'] = self.intelligence

	def indexNewIntel(self):
		index = IndexNew()
		index.createIndexNew()
		self.forgeDocIndex()
		self.indexInES()
