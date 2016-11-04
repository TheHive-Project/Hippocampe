(function() {
	'use strict';

	var jobs = angular.module('jobs', ['ui.router', 'chart.js', 'ui.bootstrap']);

	jobs.controller('JobsCtrl', function($scope, $log, JobsSrv) {
		$scope.reportJobsRAW = {};
		$scope.metadataRoot = [];
		$scope.metadataColumnNames = [];
		$scope.reportColumnNames = [];
		$scope.reportRoot = [];


		function getColumnNames() {
			//Process for metadata
			//get a key
			var someJobId = Object.keys($scope.metadataRoot)[0];
			var someConfFilename = Object.keys($scope.reportJobsRAW[someJobId]['report'])[0];

			for (var columnName in $scope.reportJobsRAW[someJobId]['report'][someConfFilename]) {
				if($scope.reportJobsRAW[someJobId]['report'][someConfFilename].hasOwnProperty(columnName)) {
					$scope.reportColumnNames.push(columnName);
				}
			}

			for (var columnName in $scope.metadataRoot[someJobId]) {
				if($scope.metadataRoot[someJobId].hasOwnProperty(columnName)) {
					$scope.metadataColumnNames.push(columnName);
				}
			}
		};

		function isolateMetadata() {
		/* copy reportJobsRAW into metadataRoot but without
		key value couple 'report'
		*/
		$scope.metadataRoot = JSON.parse(JSON.stringify($scope.reportJobsRAW));
			for (var idJobs in $scope.metadataRoot) {
				delete $scope.metadataRoot[idJobs]['report'];
			}
		};

		function isolateReport() {
		//$scope.dictReport = JSON.parse(JSON.stringify($scope.reportJobsRAW));
			for (var idJobs in $scope.reportJobsRAW) {
				$scope.reportRoot[idJobs] = $scope.reportJobsRAW[idJobs]['report'];
			}
		};

		function processJobsSources() {
		//get jobs's report
			JobsSrv.list().then(
				function(response) {
					$scope.reportJobsRAW = response.data;
					isolateMetadata();
					getColumnNames();
					isolateReport();
				},
				function(rejection) {
					console.log(rejection.data);
				}
			);
		};


		processJobsSources();
	});

	jobs.service('JobsSrv', function($http) {
		return {
			list: function() {
				return $http.get('hippocampe/api/v1.0/jobs');
			}
		};
	});

})();
