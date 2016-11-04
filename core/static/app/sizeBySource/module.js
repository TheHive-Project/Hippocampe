(function() {
    'use strict';

    var sizeBySource = angular.module('sizeBySource', ['ui.router', "chart.js"]);

    sizeBySource.controller('SizeBySourceCtrl', function($scope, SizeBySourceSrv) {
		$scope.labelsDonut = [];
		$scope.dataDonut = [];

		function getDonutData() {
			for (var url in $scope.reportSize){
				$scope.labelsDonut.push(url);
				$scope.dataDonut.push($scope.reportSize[url]["size"]);
			}
		};
			

		function processSizeBySource() {
			SizeBySourceSrv.list().then(
				function(response) {
					$scope.reportSize = response.data;
					getDonutData();
				},
				function(rejection) {
					console.log(rejection.data);
				}
			);
		};

		processSizeBySource();
    });


    sizeBySource.service('SizeBySourceSrv', function($http) {
        return {
            list: function() {
                return $http.get('hippocampe/api/v1.0/sizeBySources');
            }
        };
    });

})();
