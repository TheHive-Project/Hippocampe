(function() {
	'use strict';

	var shadowbook = angular.module('shadowbook', ['ui.router', 'ui.bootstrap'])
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

	shadowbook.controller('ShadowbookCtrl', function($scope, ShadowbookSrv, Notification) {
		$scope.alerts;
		var response;


		$scope.shadowbook = function() {
			//clean out the alerts list, one alert at a time
			$scope.alerts = [];

			$scope.closeAlert = function(index) {
				$scope.alerts.splice(index, 1);
			};

			ShadowbookSrv.list().then(
				function(response) {
					//job launched with success
					response = JSON.parse(JSON.stringify(response.data));
					if (response.hasOwnProperty('job')) {
						var idJobList = Object.keys(response['job']);
						//there's only one element in idJobList => idJobList[0]
						var msg = 'Job '.concat(idJobList[0]).concat(' sucessfully launched');
						Notification.success({message: msg});
					}
				},
				function(rejection) {
					//one job already running
					var msg = rejection.data['error'];
					Notification.error({message: msg});
				}
			);			
		};

	});

	shadowbook.service('ShadowbookSrv', function($http) {
		return {
			list: function() {
				return $http.get('hippocampe/api/v1.0/shadowbook');
			}
		};
	});


})();