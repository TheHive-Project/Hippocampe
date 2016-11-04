(function() {
	// Create an application
	var app = angular.module('hippocampe',
		['ui.router', 
		'chart.js', 
		'ui.bootstrap',
		'main'
		]);

	app.config(function($stateProvider, $urlRouterProvider) {
		$urlRouterProvider.otherwise('/home');

		// $stateProvider
		// 	.state('sources', {
		// 		url: "/sources",
		// 		templateUrl: "app/sources/sources.html",
		// 		controller: "app/sources/module.js"
		// 	})
	});

	app.filter('toArray', function() {
		return function(input) {
			var out = [];
			// check if input is array
			for (key in input) {
				var value = input[key];
				value["id"] = key;
				out.push(value);
			}
		return out;
		};
	});

})();
