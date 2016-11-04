(function() {
	'use strict';

	var hipposcore = angular.module('hipposcore', ['ui.router', 'ui-notification'])
		.config(function(NotificationProvider) {
	        NotificationProvider.setOptions({
	            delay: 10000,
	            startTop: 55,
	            startRight: 10,
	            verticalSpacing: 20,
	            horizontalSpacing: 20,
	            positionX: 'right',
	            positionY: 'top'
	        });
	    });

	hipposcore.controller('HipposcoreCtrl', function($scope, TypeSrv, HipposcoreSrv, Notification) {
		$scope.textValue;
		$scope.observable;
		$scope.listTypes = [];
		$scope.selectedType;
		$scope.score;


		$scope.closeAlert = function(index) {
			$scope.alerts.splice(index, 1);
		};

		$scope.hipposcore = function() {
			if ($scope.textValue) {
				$scope.observable = this.textValue;
				$scope.textValue = '';
			}
			
			HipposcoreSrv.list($scope.selectedType, $scope.observable).then(
				function(response) {
					$scope.score = response.data[$scope.observable]['hipposcore'];

					if ($scope.score === 0) {
						//var msg = $scope.selectedType.concat(': ').concat($scope.observable).concat(' Unknown'); 
						var msg = $scope.observable.concat(' Unknown'); 
						Notification.warning({message: msg});
					}
					else if ($scope.score > 0) {
						var msg = $scope.observable.concat(' : ').concat($scope.score);
						Notification.info({message: msg});
					}
					else if ($scope.score < 0) {
						var msg = $scope.observable.concat(' : ').concat($scope.score);
						Notification.error({message: msg});
					}
				},
				function(rejection) {
					console.log(rejection.data);
				}
			);
		};

		//dropdown toggle stuff
	    function init() {
	    //retrieve type for dropdown toggle
		    TypeSrv.list().then(
		      function(response) {
		        $scope.listTypes = response.data['type'];
		      },
		      function(rejection) {
		        console.log(rejection.data);
		      }
		    );
	    };

	    // change dropdown toggle label according to selected type
	    $scope.selectTypeHipposcore = function(selectedType) {
	      $scope.selectedType = selectedType;
	    };

	    init();
	});

	hipposcore.service('TypeSrv', function($http) {
	    return {
	      list: function() {
	        return $http.get('hippocampe/api/v1.0/type');
	      }
	    };
	});

	hipposcore.service('HipposcoreSrv', function($http) {
		return {
			list: function(selectedType, observable) {
				var requestBody = {};
				var subBody = {};
				subBody['type'] = selectedType;

				requestBody[observable] = subBody;

				return $http.post('hippocampe/api/v1.0/hipposcore', requestBody);
			}
		};   
    });

})();