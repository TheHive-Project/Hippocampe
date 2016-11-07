#!/usr/bin/env python
# -*- coding: utf8 -*-


from elasticsearch import helpers
import logging
logger = logging.getLogger(__name__)
from time import strftime
import os, sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../../'
getESpath = app_dir + 'services/common'
sys.path.insert(0, getESpath)
from ES import getES
from getConf import getConf
from getConf import getHippoConf
from objects.IndexNew import IndexNew
from objects.IndexIntel import IndexIntel

def update(typeNameES, listId):
	logger.info('bulkOp.update launched')
	hippoCfg = getHippoConf()
	es = getES()
	now = strftime("%Y%m%dT%H%M%S%z")
	indexNameES = hippoCfg.get('elasticsearch', 'indexNameES')
	# k is a generator expression that produces
	# dict to update every doc wich id is in listId
	k = ({'_op_type': 'update', '_index':indexNameES, '_type':typeNameES, 'doc':{'lastQuery': now}, '_id': id}
		for id in listId)

	res = helpers.bulk(es, k)
	logger.info('bulkOp.update res: %s', res)
	#res looks like
	#(2650, [])  
	logger.info('bulkOp.update end')
	return res[0]

def index(cfgPath, listData):
	logger.info('bulkOp.index launched')
	hippoCfg = getHippoConf()
	indexNameES = hippoCfg.get('elasticsearch', 'indexNameES')

	cfg = getConf(cfgPath)
	typeNameES = cfg.get('elasticsearch', 'typeIntel')
	
	#creating the index, only if does not exist
	index = IndexIntel(cfgPath)
	index.createIndexIntel()

	es = getES()
	k = ({'_op_type': 'index', '_index':indexNameES, '_type':typeNameES, '_source': data}
		for data in listData)
	res = helpers.bulk(es,k, raise_on_error=False)
	#res = helpers.bulk(es,k, raise_on_exception=False)
	#res = helpers.bulk(es,k)
	logger.info('bulkOp.index res: %s', res)
	logger.info('bulkOp.index end')
	return res

def indexNew(coreIntelligence, listData):
	logger.info('bulkOp.indexNew launched')

	hippoCfg = getHippoConf()
	indexNameES = hippoCfg.get('elasticsearch', 'indexNameES')
	typeNameES = hippoCfg.get('elasticsearch', 'typeNameESNew')

	indexNew = IndexNew()
	indexNew.createIndexNew()
	
	es = getES()
	k = ({'_op_type': 'index', '_index':indexNameES, '_type':typeNameES, '_source': {'type': coreIntelligence, 'toSearch': data[coreIntelligence]}}
		for data in listData) 
	#k.next() gives:
	#{'_op_type': 'index', '_index':'hippocampe', '_type':'new', '_source': {'typeIntel': 'ip', 'intelligence': '1.1.1.1'}
	res = helpers.bulk(es,k)
	logger.info('bulkOp.index res: %s', res)
	logger.info('bulkOp.indexNew end')	
	return res[0]
if __name__ == '__main__':
	main()
