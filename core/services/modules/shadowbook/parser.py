#!/usr/bin/env python
# -*- coding: utf8 -*-

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
