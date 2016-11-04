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

import logging
logger = logging.getLogger(__name__)

def littleSort(resMsearch, data):
	logger.info('processMsearch.littleSort launched')
	#data is a list of dict
	#each dict is a parsed line from the feed
	# resMsearch will look like
#{u'responses': [{u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
#                 u'hits': {u'hits': [{u'_id': u'AVOuC41q6EIAXcyxAFz0',
#                                      u'_index': u'hippocampe',
#                                      u'_score': 7.470799,
#                                      u'_source': {u'firstAppearance': u'20160325T145146+0100',
#                                                   u'idSource': u'AVOuCsBt6EIAXcyxAEn3',
#                                                   u'lastAppearance': u'20160325T145146+0100',
#                                                   u'source': u'https://openphish.com/feed.txt',
#                                                   u'url': u'https://www.myfridaygoodies.ch/sandbox/1/'},
#                                      u'_type': u'openphishFree_feedURL'}],
#                           u'max_score': 7.470799,
#                           u'total': 1},
#                 u'timed_out': False,
#                 u'took': 124},

#                {u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
#                 u'hits': {u'hits': [], u'max_score': None, u'total': 0},
#                 u'timed_out': False,
#                 u'took': 107},

#                {u'_shards': {u'failed': 0, u'successful': 5, u'total': 5},
#                 u'hits': {u'hits': [{u'_id': u'AVOuCxyD6EIAXcyxAFA0',
#                                      u'_index': u'hippocampe',
#                                      u'_score': 7.4480977,
#                                      u'_source': {u'firstAppearance': u'20160325T145117+0100',
#                                                   u'idSource': u'AVOuCsBt6EIAXcyxAEn3',
#                                                   u'lastAppearance': u'20160325T145117+0100',
#                                                   u'source': u'https://openphish.com/feed.txt',
#                                                   u'url': u'http://www.rutzcellars.com/dd-dd/art/'},
#                                      u'_type': u'openphishFree_feedURL'}],
#                           u'max_score': 7.4480977,
#                           u'total': 1},
#                 u'timed_out': False,
#                 u'took': 117}]}
	i = 0
	toIndex = list()
	toUpdate = list()
	while i < len(data):
		if len(resMsearch['responses'][i]['hits']['hits']) == 0:
			#we are in this case:
			#u'hits': {u'hits': []
			#it means that the intel at line i of the feed is unknown in ES
			#and we have to index it
			toIndex.append(data[i])
		if len(resMsearch['responses'][i]['hits']['hits']) > 0:
			#we are in this case:
#                 u'hits': {u'hits': [{u'_id': u'AVOuCxyD6EIAXcyxAFA0',
#                                      u'_index': u'hippocampe',
#                                      u'_score': 7.4480977,
#                                      u'_source': {u'firstAppearance': u'20160325T145117+0100',
#                                                   u'idSource': u'AVOuCsBt6EIAXcyxAEn3',
#                                                   u'lastAppearance': u'20160325T145117+0100',
#                                                   u'source': u'https://openphish.com/feed.txt',
#                                                   u'url': u'http://www.rutzcellars.com/dd-dd/art/'},
#                                      u'_type': u'openphishFree_feedURL'}],

			#retrieving ids to update the doc in ES
			for match in resMsearch['responses'][i]['hits']['hits']:
				toUpdate.append(match['_id']) 
		i += 1

	res = dict()
	res['toIndex'] = toIndex
	res['toUpdate'] = toUpdate
	logger.info('processMsearch.littleSort end')
	return res

def bigSort(resMsearch, data):
	logger.info('processMsearch.bigSort launched')
	i = 0
	toIndexInNew = list()
	while i < len(data):
		if len(resMsearch['responses'][i]['hits']['hits']) == 0:
			toIndexInNew.append(data[i])
		i += 1
	logger.info('processMsearch.bigSort end')
	return toIndexInNew
if __name__ == '__main__':
	main()
