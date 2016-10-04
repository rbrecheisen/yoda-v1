'use strict';

angular.module('controllers')
    .controller('MainController', ['$scope', 'BackgroundService',
        function($scope, BackgroundService) {
            $scope.background = BackgroundService;
        }]);