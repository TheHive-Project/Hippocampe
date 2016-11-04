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
import requests
from copy import deepcopy

def simpleDownload(url, listSessions):
	#listSessions is a list with authenticated sessions for feed which need to be authenticate

	#Before retrieving feed's data, we have to determine which session to use
	#by using listSessions[1:] we do not choose the first element which is the default session
	#in case that the top_level_url contains 'default'
	for session in listSessions[1:]:
	        if session['sessionName'] in url:
	                selectedSession = deepcopy(session)
	        else:
	                #the default session is always the first element in the list
	                selectedSession = listSessions[0]
	
	raw_page = selectedSession['session'].get(url, stream = True)
	#requests does not raise exception if status is not 200 by default
	#that's why we use raise_for_status()
	raw_page.raise_for_status()
	#returning raw content and not text to avoid encoding issues
	return raw_page.content

class EmptyFeedException(Exception):
	def __init__(self,url):
		Exception.__init__(self, 'Feed {0} is empty'.format(url))
		self.url = url


if __name__ == '__main__':
	main()
