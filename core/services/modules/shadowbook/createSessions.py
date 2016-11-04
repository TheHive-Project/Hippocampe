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

import os, sys
app_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
#path to getConf function
getConfPath = app_dir + 'services/modules/common'
sys.path.insert(0, getConfPath)
from getConf import getConf
import requests
from copy import deepcopy
import logging
logger = logging.getLogger(__name__)

def createSessions():
	logger.info('createSessions.createSession launched')
	authConfPath = app_dir + 'conf/auth/auth.conf'
	cfg = getConf(authConfPath)
        listSessions = list()
        element = dict()

        '''
        a session is represented by a JSON object named element:
                {
                        'sessionName': '<top_level_url>',
                        'session': objectSession
                }
        this JSON object is then put into a list: listSessions

        [
                {
                        'session': <requests.sessions.Session object at 0x7f388408b810>,
                        'sessionName': 'default'
                },
                {
                        'session': <requests.sessions.Session object at 0x7f38865c1f90>,
                        'sessionName': u'https://top_level_url.foo'
                }
        ]
        '''

        #create default session element
        element['sessionName'] = 'default'
        element['session'] = requests.Session()
        #adding the default session element to the listSessions
        #deepcopy is used because we need a complete copy and not a reference
        listSessions.append(deepcopy(element))

        #creating session for each top_level_url to be authenticated
        #each section is the top_level_url
        for section in cfg.sections():

                # retrieving username and password from conf file
                username = cfg.get(section, 'username')
                password = cfg.get(section, 'password')

                #naming the session with the top_level_url
                element['sessionName'] = section
                element['session'] = requests.Session()
                #authenticating the session
                element['session'].auth=(username, password)

                logger.info('Authenticated session created for: %s', section)

                #adding the new session element to the list
                listSessions.append(deepcopy(element))
	logger.info('createSessions.createSessions end')
        return listSessions

if __name__ == '__main__':
	createSessions()
