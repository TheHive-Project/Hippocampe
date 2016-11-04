(function() {
    'use strict';

    var sources = angular.module('sources', ['ui.router', "chart.js"]);

    sources.controller('SourcesCtrl', function($scope, SourcesSrv) {
		$scope.reportSources = {};
		$scope.columnNames = [];

		function getColumnNames() {
			//get a key (which is an url)
			var someKey = Object.keys($scope.reportSources)[0];
			
			for (var columnName in $scope.reportSources[someKey]) {
				if($scope.reportSources[someKey].hasOwnProperty(columnName)) {
					$scope.columnNames.push(columnName);
				}
			}
		};
		
		function cleanReportSources(){
			//reportSources has duplicates info (URL and link)
			//deleting link
			for (var url in $scope.reportSources){
				delete $scope.reportSources[url]['link'];
			}
		};

        function processSources() {
			//get sourcesSource's report
            SourcesSrv.list().then(
                function(response) {
                    $scope.reportSources = response.data;
					cleanReportSources();
					getColumnNames();
                },
                function(rejection) {
                    console.log(rejection.data);
                }
            );
        };

        processSources();
    });

    sources.service('SourcesSrv', function($http) {
        return {
            list: function() {
                return $http.get('hippocampe/api/v1.0/sources');
            }
        };
    });

})();
