#!/usr/bin/env python
# -*- coding: utf8 -*-

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
