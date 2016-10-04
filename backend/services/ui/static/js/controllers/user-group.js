'use strict';

angular.module('controllers')

    .controller('UserGroupsController', ['$scope', 'TokenService', 'UserService', 'BackgroundService',

        function($scope, TokenService, UserService, BackgroundService) {

            BackgroundService.setClass('user-group');

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/user-groups', text: 'User groups'}
            ];
        }]);