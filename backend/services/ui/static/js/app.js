'use strict';

angular.module('controllers', []);

angular.module('services', ['ngResource', 'ngCookies']);

// Upload library
// https://github.com/danialfarid/ng-file-upload

angular.module('app', ['ngRoute', 'ngFileUpload', 'controllers', 'services'])

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
                .when('/users/:id?',  {
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
                })
                .when('/repositories', {
                    templateUrl: 'partials/repositories.html',
                    controller: 'RepositoriesController'
                })
                .when('/repositories/:id?', {
                    templateUrl: 'partials/repository.html',
                    controller: 'RepositoryController'
                })
                .when('/repositories/:id?/files', {
                    templateUrl: 'partials/files.html',
                    controller: 'FilesController'
                })
                .when('/repositories/:id?/files/:fileId?', {
                    templateUrl: 'partials/file.html',
                    controller: 'FileController'
                });

            $locationProvider.html5Mode(false);
    }]);