(function() {
    'use strict';

    var sizeByType = angular.module('sizeByType', ['ui.router', "chart.js"]);

    sizeByType.controller('SizeByTypeCtrl', function($scope, SizeByTypeSrv) {
		$scope.labelsDonut = [];
		$scope.dataDonut = [];

		function getDonutData() {
			for (var intelType in $scope.reportSize){
				$scope.labelsDonut.push(intelType);
				$scope.dataDonut.push($scope.reportSize[intelType]["size"]);
			}
		};
			

		function processSizeByType() {
			SizeByTypeSrv.list().then(
				function(response) {
					$scope.reportSize = response.data;
					getDonutData();
				},
				function(rejection) {
					console.log(rejection.data);
				}
			);
		};

		processSizeByType();
    });


    sizeByType.service('SizeByTypeSrv', function($http) {
        return {
            list: function() {
                return $http.get('hippocampe/api/v1.0/sizeByType');
            }
        };
    });

})();
