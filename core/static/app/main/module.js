(function() {
    // Create an application
    var main = angular.module('main',
    	['ui.router', 
    	'chart.js', 
    	'ui.bootstrap',
		'home',
		'sizeByType',
		'sizeBySource',
		'monitor',
		'jobs',
		'more',
		'sources',
        'type',
        'hipposcore',
        'shadowbook'
    	]);

    main.config(function($stateProvider, $urlRouterProvider) {

    	$stateProvider
    		.state('main', {
                views: {
                    "": {templateUrl: 'app/main/main.html'},
                    "hipposcore@main": {
                        templateUrl: 'app/hipposcore/hipposcore.html',
                        controller: 'HipposcoreCtrl'
                    },
                    "shadowbook@main": {
                        templateUrl: 'app/shadowbook/shadowbook.html',
                        controller: 'ShadowbookCtrl'
                    }
                }
    		})
    		.state('main.more', {
    			url: '/more',
    			templateUrl: 'app/more/more.html',
    			controller: 'MoreCtrl'
    		})
    		.state('main.jobs', {
    			url: '/jobs',
    			templateUrl: 'app/jobs/jobs.html',
    			controller: 'JobsCtrl'
    		})
    		.state('main.sources', {
    			url: '/sources',
    			templateUrl: 'app/sources/sources.html',
    			controller: 'SourcesCtrl'
    		})
            // .state('main.hipposcore', {
            //     url: '/hipposcore',
            //     templateUrl: 'app/hipposcore/hipposcore.html',
            //     controller: 'HipposcoreCtrl'
            // })
            // .state('main.shadowbook', {
            //     url: '/shadowbook',
            //     templateUrl: 'app/shadowbook/shadowbook.html',
            //     controller: 'ShadowbookCtrl'
            // })
    });

})();