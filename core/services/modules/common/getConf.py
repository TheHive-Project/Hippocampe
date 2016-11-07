#!/usr/bin/env python
# -*- coding: utf8 -*-

from configparser import ConfigParser
import os

def getConf(confPath):
	cfg = ConfigParser()
	cfg.read(confPath)
	return cfg

def getHippoConf():
	current_dir = os.path.dirname(os.path.abspath(__file__))
	app_dir = current_dir + '/../../../'
	
	confPath = app_dir + 'conf/hippo/hippo.conf'
	return getConf(confPath)
	
if __name__ == '__main__':
	getHippoConf()
