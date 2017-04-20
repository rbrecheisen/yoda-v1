'use strict';

angular.module('controllers')

    .controller('UsersController', ['$scope', '$location', '$route', 'TokenService', 'UserService',

        function($scope, $location, $route, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/users', text: 'Users'}
            ];

            // TODO: Remove this hack, there should be no DOM manipulation inside controllers
            $('.collapsible').collapsible({
                accordion: true
            });

            UserService.getAll().then(function(response) {
                $scope.users = [];
                for(var i = 0; i < response.data.length; i++) {
                    var user = response.data[i];
                    if(user.is_visible) {
                        // Convert the boolean variables to string values because the <select>
                        // element does not handle booleans
                        user.is_admin = user.is_admin ? 'true' : 'false';
                        user.is_active = user.is_active ? 'true': 'false';
                        $scope.users.push(user);
                    }
                }
            }, function(error) {
                $scope.message = JSON.stringify(error);
                alert($scope.message);
            });

            $scope.createUser = function() {
                // Redirect to user page providing ID = 0 so it knows we're trying
                // to create a new user.
                $location.path('/users/0');
            };

            $scope.editUser = function(user) {
                $location.path('/users/' + user.id);
            };

            $scope.deleteUser = function(user) {
                UserService.delete(user.id).then(function(response) {
                    $route.reload();
                }, function(error) {
                    $scope.message = JSON.stringify(error);
                    alert($scope.message);
                })
            };

            Materialize.updateTextFields();
        }])

    .controller('UserController', ['$scope', '$location', '$routeParams', 'TokenService', 'UserService', 'BackgroundService',

        function($scope, $location, $routeParams, TokenService, UserService, BackgroundService) {

            // BackgroundService.setClass('user');

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/users', text: 'Users'},
                {url: '#/users/' + $routeParams.id, text: 'User'}
            ];

            $scope.user = {};
            $scope.user.id = $routeParams.id;
            $scope.user.password1 = '';
            $scope.user.password2 = '';
            $scope.user.name = '';
            $scope.user.username = '';
            $scope.user.email = '';
            $scope.user.first_name = '';
            $scope.user.last_name = '';
            $scope.user.is_admin = 'false';
            $scope.user.is_active = 'true';

            if($scope.user.id > 0) {

                UserService.get($scope.user.id).then(function (response) {

                    var user = response.data;

                    // Just in case the user jumped to the URI directly, we check whether the
                    // user entry is visible or not.
                    // TODO: Handle invisible users at server side?
                    if (user.is_visible) {

                        $scope.user.name = user.first_name + ' ' + user.last_name;
                        $scope.user.username = user.username;
                        $scope.user.email = user.email;
                        $scope.user.first_name = user.first_name;
                        $scope.user.last_name = user.last_name;
                        $scope.user.is_admin = user.is_admin ? 'true': 'false';
                        $scope.user.is_active = user.is_active ? 'true': 'false';
                        $scope.breadcrumbs = [
                            {url: '#/admin-dashboard', text: 'Dashboard'},
                            {url: '#/users', text: 'Users'},
                            {url: '#/users/' + $routeParams.id, text: $scope.name}
                        ];
                    }
                    else {
                        $scope.message = 'User invisible';
                        alert($scope.message);
                    }
                }, function (error) {
                    $scope.message = JSON.stringify(error);
                    alert($scope.message);
                });
            }

            $scope.saveUser = function() {

                $scope.message = null;

                if($scope.user.id > 0) {

                    // We're saving an existing user. Make sure to convert 'is_admin' and
                    // 'is_active' values back to booleans
                    UserService.update(
                        $scope.user.id,
                        $scope.user.username,
                        $scope.user.password1,
                        $scope.user.password2,
                        $scope.user.email,
                        $scope.user.first_name,
                        $scope.user.last_name,
                        $scope.user.is_admin === 'true',
                        $scope.user.is_active === 'true')
                    .then(function (response) {
                        $location.path('/users');
                    }, function (error) {
                        $scope.message = JSON.stringify(error);
                        alert($scope.message);
                    })
                }
                else {

                    // Check that user provided all required fields
                    if(isNull($scope.user.username))
                        $scope.message = 'Username is empty';
                    if(isNull($scope.user.email))
                        $scope.message = 'Email is empty';
                    if(isNull($scope.user.password2))
                        $scope.message = 'Password confirmation is empty';
                    if(isNull($scope.user.first_name))
                        $scope.message = 'First name is empty';
                    if(isNull($scope.user.last_name))
                        $scope.message = 'Last name is empty';

                    // Make sure the user confirms her password
                    if($scope.user.password1 != $scope.user.password2) {
                        $scope.message = 'Passwords do not match';
                    }

                    if(!isNull($scope.message)) {
                        alert($scope.message);
                        return;
                    }

                    // Save the new user. Make sure to convert 'is_admin' and 'is_active'
                    // variables back to booleans
                    UserService.create(
                        $scope.user.username,
                        $scope.user.password1,
                        $scope.user.email,
                        $scope.user.first_name,
                        $scope.user.last_name,
                        $scope.user.is_admin === 'true',
                        $scope.user.is_active === 'true')
                    .then(function() {
                        $location.path('/users');
                    }, function(error) {
                        $scope.message = JSON.stringify(error);
                        alert($scope.message);
                    })
                }
            };

            $scope.cancelSave = function() {
                $location.path('/users');
            };
        }]);