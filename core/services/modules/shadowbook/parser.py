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
import itertools
import csv
import os, sys
install_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
#path to getConf function
getConfPath = install_dir + 'services/modules/common'
sys.path.insert(0, getConfPath)
import getConf
import ast

def csvParser(feedPage, cfgPath):

	#retrieving parsing parameters
	conf = getConf.getConf(cfgPath)

	#start parsing from startAt
	startAt = conf.getint('source', 'startAt')

	#the line does not begin with '#' nor '/'
	parsedPage = itertools.ifilter(lambda x: len(x) > 1 and x[0] != '#' and x[0] != '/', feedPage.splitlines()[startAt:])

	#csv's delimiter, has to be str and not unicode
	delimiter = str(conf.get('source', 'delimiter'))
	#fields in the csv
	fields = conf.get('source', 'fields')
	#fields is string formated as a list, the instruction below convert it as a real list
        fields = [item.encode('ascii') for item in ast.literal_eval(fields)]
	#sometimes the first field is empty
	beginWithBlank = conf.getboolean('source', 'beginWithBlank')
	if beginWithBlank:
		#the feed parsed's first row is blank, to avoid discrepancy between fields and data
		#the first row is labelled as 'blank'
		fields.insert(0, 'blank')
	extraFields = conf.get('source', 'extraFields')

	#Can not use the variable delimiter as delimiter when it equals to '\t'
	#has to use dialect 'excel-tab'
	#Apparently, this is due to ConfigParser
	if delimiter != '\\t':
		parsedPage = csv.DictReader(parsedPage, fields, extraFields, delimiter = delimiter)
	
	if delimiter == '\\t':
		parsedPage = csv.DictReader(parsedPage, fields, extraFields, dialect = 'excel-tab')

	return parsedPage

if __name__ == '__main__':
	main()
