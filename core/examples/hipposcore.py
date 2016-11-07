#!/usr/bin/env python
# -*- coding: utf8 -*-


import json
import urllib2
from pprint import pprint

def main():
	toRequest = {
		"niny.tk" : {"type": "domain"},
	} 
	
	req = urllib2.Request('http://localhost:5000/hippocampe/api/v1.0/hipposcore')
	req.add_header('Content-Type', 'application/json')
	
	response = urllib2.urlopen(req, json.dumps(toRequest))
	data = json.load(response)
	pprint(data)
if __name__ == '__main__':
	main()
