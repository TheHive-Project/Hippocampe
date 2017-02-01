#!/usr/bin/env python
# -*- coding: utf8 -*-

from flask import Flask, jsonify, abort, request, render_template
from services import shadowbook, hipposcore, more, distinct, typeIntel, new, sources, hipposched, freshness, schedReport, lastQuery, sizeBySources, sizeByType, monitorSources, jobs, lastStatus
from services.modules.common.ES import checkES, checkData
from services.modules.common.getConf import getHippoConf
import os
import logging
from logging.handlers import RotatingFileHandler
import threading

app_dir = os.path.dirname(os.path.abspath(__file__))

#create logger
logger = logging.getLogger('services')
if not logger.handlers:
	logger.setLevel(logging.DEBUG)
	#log format as: 2013-03-08 11:37:31,411 :: WARNING :: Testing foo
	formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
	#handler writes into , limited to 1Mo in append mode
	if not os.path.exists('logs'):
		#create logs directory if does not exist (tipically at first start)
		os.makedirs('logs')
	pathLog = app_dir + '/logs/hippocampe.log'
	file_handler = RotatingFileHandler(pathLog, 'a', 1000000, 1)
	#level debug
	file_handler.setLevel(logging.DEBUG)
	#using the format defined earlier
	file_handler.setFormatter(formatter)
	#Adding the file handler
	logger.addHandler(file_handler)

app = Flask(__name__, static_url_path='')
@app.route('/hippocampe/api/v1.0/more', methods=['POST'])
def moreService():
	logger.info('more service requested')
	if not request.json:
		logger.error('no JSON request sent to more')
		abort(400)
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		#ES type sources is needed for hipposcore
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = more.main(request.json)
	#result is a list of dict of matches
	#if fail, the dict contains an 'error' key valued with the corresponding error
	#[
	#	{
  	#	"123.57.64.148": {
    	#		"error": "ConnectionError[...]"
  	#		}
	#	},
	#	{"1.1.1.1": {
	#		"error" : "[..]"
	#	}
	#]
	#
	for requested in result.values():
		if 'error' in requested:
			logger.error('more failed')
			#in case of error, result is built according the following
			return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/sources', methods=['GET'])
def sourcesService():
	logger.info('sources service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = sources.main()
	if 'error' in result:
		logger.error('source failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/jobs', methods=['GET'])
def jobsService():
	logger.info('jobs service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['jobsType']):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = jobs.main()
	if 'error' in result:
		logger.error('jobs failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/new', methods=['GET'])
def newService():
	logger.info('new service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['newType']):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = new.main()
	#result is a list of new intelligence, never seen before
	if 'error' in result:
		logger.error('new failed')
		return jsonify(response), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/hipposcore', methods=['POST'])
def hipposcoreService():
	logger.info('hipposcore service requested')
	if not request.json:
		logger.error('no JSON request sent to hipposcore')
		abort(400)
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		#ES type source is needed to retrieve source's score
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	logger.info('more for hipposcore started')
	result = more.main(request.json)

	#check if there's error in more response
	for requested in result.values():
		if 'error' in requested:
			logger.error('more for hipposcore failed')
			return jsonify(result), 500
	else:
		hippodict = hipposcore.calcHipposcore(result)
		if 'error' in hippodict:
			#hippodict looks like {'error': '<error_name>'}
			logger.error('hipposcore failed')
			return jsonify(hippodict), 500
		else:
			return jsonify(hippodict), 200

@app.route('/hippocampe/api/v1.0/shadowbook', methods=['GET'])
def shadowbookService():
	logger.info('shadowbook service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	reportJob = shadowbook.initJob()

	if 'error' in reportJob:
		logger.error('shadowbook failed')
		return jsonify(reportJob), 500
	else:
		threading.Thread(target = shadowbook.manageJob).start()
		return jsonify(reportJob), 200
	#reportAllFeeds = shadowbook.startJob()
	#if 'error' in reportAllFeeds:
	#	#unknown error catch by Exception
	#	logger.error('shadowbook failed')
	#	return jsonify(reportAllFeeds), 500
	#else:
	#	#does not mean that there's no error
	#	#it may be catched/handled errors
	#	for status in reportAllFeeds.values():
	#		if status['error']:
	#			#means that the list status['error'] is not empty
	#			#so there is error
	#			logger.error('shadowbook failed')
	#			return jsonify(reportAllFeeds), 500
	#	return jsonify(reportAllFeeds), 200

@app.route('/hippocampe/api/v1.0/hipposched', methods=['POST'])
def hipposchedService():
	logger.info('hipposched service requested')
	if not request.json:
		logger.error('no JSON request sent to hipposched')
		abort(400)
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	report = hipposched.main(request.json)
	if 'error' in report:
		logger.error('hipposched failed')
		return jsonify(report), 500
	else:
		return jsonify(report), 202

@app.route('/hippocampe/api/v1.0/distinct', methods=['POST'])
def distinctService():
	logger.info('distinct service requested')
	if not request.json:
		logger.error('no JSON request sent to distinct')
		abort(400)
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData([]):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = distinct.main(request.json)
	if 'error' in result:
		logger.error('distinct failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/type', methods=['GET'])
def typeIntelService():
	logger.info('type service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData([]):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = typeIntel.main()
	if 'error' in result:
		logger.error('type service failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/freshness', methods=['GET'])
def freshnessService():
	logger.info('freshness service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		#ES type source needed to calc freshness
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = freshness.main()
	if 'error' in result:
		logger.error('freshness failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/schedReport', methods=['GET'])
def schedReportService():
	logger.info('schedReport service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		#ES type source needed to determine if threshold is respected
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = schedReport.main()
	if 'error' in result:
		logger.error('schedReport failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/lastQuery', methods=['GET'])
def lastQueryService():
	logger.info('lastQuery service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		#lastQuery is in source
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = lastQuery.main()
	if 'error' in result:
		logger.error('lastQuery failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/sizeBySources', methods=['GET'])
def sizeBySourcesService():
	logger.info('sizeBySources service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = sizeBySources.main()
	if 'error' in result:
		logger.error('sizeBySources failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/sizeByType', methods=['GET'])
def sizeByTypeService():
	logger.info('sizeByType service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		#need to retrieve all sources
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = sizeByType.main()
	if 'error' in result:
		logger.error('sizeByType failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/monitorSources', methods=['GET'])
def monitorSourcesService():
	logger.info('monitorSources service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = monitorSources.main()
	if 'error' in result:
		logger.error('monitorSources failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe/api/v1.0/lastStatus', methods=['GET'])
def lastStatusService():
	logger.info('lastStatus service requested')
	if not checkES():
		logger.error('elasticsearch not available')
		return jsonify(
			{'error':'elasticsearch not available'}), 500
	if not checkData(['sourceType']):
		logger.error('no data')
		return jsonify(
			{'error':'no data available'}), 500
	result = lastStatus.main()
	if 'error' in result:
		logger.error('lastStatus failed')
		return jsonify(result), 500
	else:
		return jsonify(result), 200

@app.route('/hippocampe', methods=['GET'])
def index():
	if not checkES():
		return render_template('error.html')
	else:
		return render_template('index.html')

if __name__ == '__main__':

	##accessing Werkzeug’s logger and writing logs to file
	##snippet from https://docstrings.wordpress.com/2014/04/19/flask-access-log-write-requests-to-file/
	#loggerWerkzeug = logging.getLogger('werkzeug')
	##accessing Werkzeug’s logger and writing logs to file
	#pathLogWerkzeug = app_dir + '/logs/werkzeug.log'
	#handlerWerkzeug = logging.FileHandler(pathLogWerkzeug)
	#loggerWerkzeug.addHandler(handlerWerkzeug)
	## Also add the handler to Flask's logger for cases
	##  where Werkzeug isn't used as the underlying WSGI server.
	#app.logger.addHandler(handlerWerkzeug)

	#loading general configuration file
	cfg = getHippoConf()

	app.run(debug = cfg.getboolean('api', 'debug'), host = cfg.get('api', 'host'),
		port = cfg.getint('api', 'port'), threaded = cfg.getboolean('api', 'threaded'))
