#!/usr/bin/env python
# -*- coding: utf8 -*-

from time import strftime

def metadata(idSource, source, data):
	#data is a list of dict
	#each element is a dict representing a feed's parsed line
	for element in data:
		element.pop('blank', None)
		element['lastAppearance'] = strftime("%Y%m%dT%H%M%S%z")
		element['firstAppearance'] = strftime("%Y%m%dT%H%M%S%z")
		element['idSource'] = idSource
		element['source'] = source

	return data	
if __name__ == '__main__':
	main()
