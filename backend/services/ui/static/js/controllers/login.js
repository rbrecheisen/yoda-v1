'use strict';

angular.module('controllers')

    .controller('LoginController', ['$scope', '$cookies', '$location', 'TokenService', 'UserService', 'BackgroundService',

        function($scope, $cookies, $location, TokenService, UserService, BackgroundService) {

            BackgroundService.setClass('login');

            // TODO: remove username/password
            $scope.username = 'ralph';
            $scope.password = 'secret';

            $scope.login = function() {
                TokenService.create($scope.username, $scope.password).then(function(response) {

                    var data = response.data;
                    TokenService.update(data.token);

                    UserService.getByUsername($scope.username).then(function(response) {
                        var user = response.data[0];
                        UserService.setCurrentUser(user);
                        if(data.is_admin) {
                            $location.path('/admin-dashboard');
                        } else {
                            $location.path('/');
                        }
                    }, function(error) {
                        $scope.message = JSON.stringify(error);
                        alert($scope.message);
                    });
                }, function(error) {
                    $scope.message = JSON.stringify(error);
                    alert($scope.message);
                });
            };
        }])

    .controller('LogoutController', ['$location', 'TokenService', 'UserService',

        function($location, TokenService, UserService) {

            TokenService.delete();

            UserService.setCurrentUser(null);
            $location.path('/login');
        }]);