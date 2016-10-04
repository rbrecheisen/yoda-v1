'use strict';

angular.module('controllers')

    .controller('DashboardController', ['$scope', '$location', 'TokenService', 'UserService', 'BackgroundService',

        function($scope, $location, TokenService, UserService, BackgroundService) {

            BackgroundService.setClass('dashboard');

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/', text: 'Dashboard'}
            ];
        }])

    .controller('AdminDashboardController', ['$scope', '$location', 'TokenService', 'UserService', 'BackgroundService',

        function($scope, $location, TokenService, UserService, BackgroundService) {

            BackgroundService.setClass('dashboard');

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'}
            ];
        }]);