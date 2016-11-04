(function() {
	'use strict';

	var type = angular.module('type', ['ui.router', "chart.js"]);

	type.controller('TypeCtrl', function($scope, TypeSrv) {

		$scope.listTypes = [];
		$scope.selectedType;

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
		$scope.selectTypeMore = function(selectedType) {
			$scope.selectedType = selectedType;
		};

		init();
	});

	type.service('TypeSrv', function($http) {
		return {
			list: function() {
				return $http.get('hippocampe/api/v1.0/type');
			}
		};
	});
})();
