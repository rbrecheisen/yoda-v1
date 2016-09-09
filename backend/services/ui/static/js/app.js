'use strict';

$(document).ready(function() {
    // For some reason we need to call this, otherwise the <select> element
    // will not even render. Found SO post here:
    // http://stackoverflow.com/questions/28258106/materialize-css-select-doesnt-seem-to-render
    $('select').material_select();

    // TODO: Look at this solution:
    // https://gist.github.com/viniciusmelquiades/66ed8039e3709b126e52
});

angular.module('app', ['ngRoute', 'controllers', 'services'])

    .constant('environ', window.environ)

    .config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {
        
            $routeProvider
                .when('/', {
                    templateUrl: 'partials/dashboard.html',
                    controller: 'DashboardController'
                })
                .when('/admin', {
                    templateUrl: 'partials/admin.html',
                    controller: 'AdminController'
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
