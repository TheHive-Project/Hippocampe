(function() {
    'use strict';

    var monitor = angular.module('monitor', ['ui.router', "chart.js"]);

    monitor.controller('MonitorCtrl', function($scope, MonitorSrv) {
        $scope.reportMonitor = {};
        $scope.reportSize = {};
        $scope.columnNames = [];

        function getColumnNames() {
			//get a key (which is an url)
			var someKey = Object.keys($scope.reportMonitor)[0];
			
			for (var columnName in $scope.reportMonitor[someKey]) {
				if($scope.reportMonitor[someKey].hasOwnProperty(columnName)) {
					$scope.columnNames.push(columnName);
				}
			}
		};

        function processMonitorSources() {
			//get monitorSource's report
            MonitorSrv.list().then(
                function(response) {
                    $scope.reportMonitor = response.data;
                    getColumnNames();
                },
                function(rejection) {
                    console.log(rejection.data);
                }
            );
        };


        processMonitorSources();
    });

    monitor.service('MonitorSrv', function($http) {
        return {
            list: function() {
                return $http.get('hippocampe/api/v1.0/monitorSources');
            }
        };
    });

})();
