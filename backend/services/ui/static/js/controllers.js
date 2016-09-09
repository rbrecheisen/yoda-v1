'use strict';

angular.module('controllers', [])

    .controller('DashboardController', ['$scope', '$location', 'TokenService',
        function($scope, $location, TokenService) {
            TokenService.check();
            $scope.breadcrumbs = [
                {url: '#/', text: 'Dashboard'}
            ];
        }])
    
    .controller('AdminController', ['$scope', '$location', 'TokenService',
        function($scope, $location, TokenService) {
            TokenService.check();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'}
            ];
        }])

    .controller('LoginController', ['$scope', '$cookies', '$location', 'TokenService',
        function($scope, $cookies, $location, TokenService) {

            // TODO: Remove this
            $scope.username = 'root';
            $scope.password = 'secret';
            
            $scope.login = function() {
                TokenService.create($scope.username, $scope.password).then(function(response) {
                    TokenService.update(response.data.token);
                    if(response.data.is_admin) {
                        $location.path('/admin');
                    } else {
                        $location.path('/');
                    }
                }, function(error) {
                    $scope.message = JSON.stringify(error);
                });
            };
        }])
    
    .controller('LogoutController', ['$location', 'TokenService',
        function($location, TokenService) {
            TokenService.delete();
            $location.path('/login');
        }])

    .controller('UsersController', ['$scope', '$location', 'TokenService', 'UserService',
        function($scope, $location, TokenService, UserService) {

            TokenService.check();

            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/users', text: 'Users'}
            ];

            // TODO: Remove this hack, there should be no DOM manipulation inside controllers
            $('.collapsible').collapsible({
                accordion: true
            });

            UserService.getAll().then(function(response) {
                $scope.users = response.data;
            }, function(error) {
                $scope.message = JSON.stringify(error);
            });

            $scope.editUser = function(user) {
                $location.path('/users/' + user.id);
            };

            $scope.saveUser = function(user) {
                UserService.update(user).then(function(response) {
                    UserService.getAll().then(function(response) {
                        $scope.users = response.data
                    }, function(error) {
                        $scope.message = JSON.stringify(error);
                    });
                })
            };

            Materialize.updateTextFields();
        }])

    .controller('UserController', ['$scope', '$routeParams', 'TokenService', 'UserService',
        function($scope, $routeParams, TokenService, UserService) {

            TokenService.check();

            $scope.password_old = '';
            $scope.password_new = '';

            UserService.get($routeParams.userId).then(function(response) {
                $scope.name = response.data.first_name + ' ' + response.data.last_name;
                $scope.username = response.data.username;
                $scope.email = response.data.email;
                $scope.first_name = response.data.first_name;
                $scope.last_name = response.data.last_name;
                $scope.is_admin = response.data.is_admin;
            }, function(error) {
                $scope.message = JSON.stringify(error);
            });

            $scope.saveUser = function() {
                console.log('Saving user ' + $scope.username + ', ' +
                    $scope.email + ', ' + $scope.first_name + ', ' + $scope.last_name + ', ' + $scope.is_admin);
            };
        }])
    
    .controller('UserGroupsController', ['$scope', 'TokenService',
        function($scope, TokenService) {
            TokenService.check();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/user-groups', text: 'User groups'}
            ];
        }])

    .controller('PermissionsController', ['$scope', 'TokenService',
        function($scope, TokenService) {
            TokenService.check();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/permissions', text: 'Permissions'}
            ];
        }]);
