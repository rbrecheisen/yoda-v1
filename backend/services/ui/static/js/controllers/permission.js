'use strict';

angular.module('controllers')

    .controller('PermissionsController', ['$scope', 'TokenService', 'UserService',

        function($scope, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/permissions', text: 'Permissions'}
            ];
        }]);
