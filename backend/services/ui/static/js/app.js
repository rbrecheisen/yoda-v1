'use strict';

angular.module('app', ['ngRoute', 'controllers', 'services'])

    .constant('environ', window.environ)

    .config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {
        
            $routeProvider
                .when('/', {
                    templateUrl: 'partials/dashboard.html',
                    controller: 'DashboardController'
                })
                .when('/admin-dashboard', {
                    templateUrl: 'partials/admin-dashboard.html',
                    controller: 'AdminDashboardController'
                })
                .when('/login', {
                    templateUrl: 'partials/login.html',
                    controller: 'LoginController'
                })
                .when('/logout', {
                    templateUrl: 'partials/login.html',
                    controller: 'LogoutController'
                })
                .when('/users', {
                    templateUrl: 'partials/users.html',
                    controller: 'UsersController'
                })
                .when('/users/:userId?',  {
                    templateUrl: 'partials/user.html',
                    controller: 'UserController'
                })
                .when('/user-groups', {
                    templateUrl: 'partials/user-groups.html',
                    controller: 'UserGroupsController'
                })
                .when('/permissions', {
                    templateUrl: 'partials/permissions.html',
                    controller: 'PermissionsController'
                });

            $locationProvider.html5Mode(false);
    }]);
