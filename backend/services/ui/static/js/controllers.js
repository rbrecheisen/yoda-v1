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

    .controller('LoginController', ['$scope', '$cookies', '$location', 'TokenService', 'environment',
        function($scope, $cookies, $location, TokenService, environment) {

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

    .controller('UsersController', ['$scope', 'TokenService', 'UserService', 
        function($scope, TokenService, UserService) {

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
                $scope.users = response.data
            }, function(error) {
                $scope.message = JSON.stringify(error);
            });

            Materialize.updateTextFields();
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
