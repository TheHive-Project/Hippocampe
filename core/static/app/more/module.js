(function() {
  'use strict';

  var more = angular.module('more', ['ui.router', 'ui.bootstrap']);

  // more.config(function($stateProvider, $urlRouterProvider) {
  //   $stateProvider
  //     .state('main.more', {
  //       url: '/more',
  //       views: {
  //         "": {
  //           templateUrl: "app/more/more.html",
  //           controller: "MoreCtrl"
  //         },
  //         "type@main.more": {
  //           templateUrl: "app/type/type.html",
  //           controller: "TypeCtrl"
  //         }
  //       }
  //     })
  // });

  more.controller('MoreCtrl', function($scope, MoreSrv, TypeSrv) {
    $scope.list = [];
    $scope.textareaValue = '';
    $scope.observables = '';
    $scope.listObservables = [];
    $scope.listTypes = [];
    $scope.selectedType;
    $scope.moreResult = {};

    $scope.submit = function() {

      if ($scope.textareaValue) {
        $scope.observables=this.textareaValue;
        $scope.textareaValue = '';
      }

      $scope.listObservables = $scope.observables.split('\n');

      MoreSrv.list($scope.selectedType, $scope.listObservables).then(
        function(response) {
          //alert(JSON.stringify(response.data));
          $scope.moreResult = JSON.parse(JSON.stringify(response.data));
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
    $scope.selectTypeMore = function(selectedType) {
      $scope.selectedType = selectedType;
    };

    init();
  });

  more.service('MoreSrv', function($http) {
    return {
      list: function(selectedType, listObservables) {
        var requestBody = {};
        var subBody = {};
        subBody['type'] = selectedType;
        var observable;

        listObservables.forEach(function(observable) {
          requestBody[observable] = subBody;
        });

        //alert(JSON.stringify(requestBody));
        return $http.post('hippocampe/api/v1.0/more', requestBody);
      }
    };
  });

  more.service('TypeSrv', function($http) {
    return {
      list: function() {
        return $http.get('hippocampe/api/v1.0/type');
      }
    };
  });

})();
