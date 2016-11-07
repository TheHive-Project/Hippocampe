#!/usr/bin/env python
# -*- coding: utf8 -*-


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
