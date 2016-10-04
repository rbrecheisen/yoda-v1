'use strict';

angular.module('controllers')

    .controller('PermissionsController', ['$scope', 'TokenService', 'UserService', 'BackgroundService',

        function($scope, TokenService, UserService, BackgroundService) {

            BackgroundService.setClass('permission');

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/permissions', text: 'Permissions'}
            ];
        }]);
