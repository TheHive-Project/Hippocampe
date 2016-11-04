(function() {
	'use strict';

	var home = angular.module('home', 
		['ui.router', 
		'chart.js',
		'sizeByType',
		'sizeBySource',
		'monitor'
		]);

	home.config(function($stateProvider, $urlRouterProvider) {
		$stateProvider
		.state('main.home', {
			url: "/home",
			views: {
				"": { templateUrl: "app/home/home.html"},
				"monitor@main.home": {
					templateUrl: "app/monitor/monitor.html",
					controller: "MonitorCtrl"},
				"sizeByType@main.home": {
					templateUrl: "app/sizeByType/donutSizeByType.html",
					controller : "SizeByTypeCtrl"},
				"sizeBySource@main.home": {
					templateUrl: "app/sizeBySource/donutSizeBySource.html",
					controller: "SizeBySourceCtrl"}
			}
		})
	});
})();
