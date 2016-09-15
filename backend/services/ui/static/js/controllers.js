'use strict';

angular.module('controllers', [])

    .controller('DashboardController', ['$scope', '$location', 'TokenService', 'UserService',
        function($scope, $location, TokenService, UserService) {
            TokenService.check();
            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/', text: 'Dashboard'}
            ];
        }])
    
    .controller('AdminController', ['$scope', '$location', 'TokenService', 'UserService',
        function($scope, $location, TokenService, UserService) {
            TokenService.check();
            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'}
            ];
        }])

    .controller('LoginController', ['$scope', '$cookies', '$location', 'TokenService', 'UserService',
        function($scope, $cookies, $location, TokenService, UserService) {

            // TODO: Remove this
            $scope.username = 'ralph';
            $scope.password = 'secret';
            
            $scope.login = function() {
                TokenService.create($scope.username, $scope.password).then(function(response) {

                    var data = response.data;
                    TokenService.update(data.token);

                    UserService.getByUsername($scope.username).then(function(response) {
                        var user = response.data[0];
                        UserService.setCurrentUser(user);
                    }, function(error) {
                        $scope.message = JSON.stringify(error);
                        alert($scope.message);
                    });

                    if(data.is_admin) {
                        $location.path('/admin');
                    } else {
                        $location.path('/');
                    }
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
        }])

    .controller('UsersController', ['$scope', '$location', 'TokenService', 'UserService',
        function($scope, $location, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
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

            Materialize.updateTextFields();
        }])

    .controller('UserController', ['$scope', '$location', '$routeParams', 'TokenService', 'UserService',
        function($scope, $location, $routeParams, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/users', text: 'Users'},
                {url: '#/users/' + $routeParams.userId, text: 'User'}
            ];

            $scope.userId = $routeParams.userId;
            $scope.password1 = '';
            $scope.password2 = '';
            $scope.name = '';
            $scope.username = '';
            $scope.email = '';
            $scope.first_name = '';
            $scope.last_name = '';
            $scope.is_admin = 'false';
            // $scope.admin = $scope.is_admin;
            $scope.is_active = 'true';
            // $scope.active = $scope.is_active;

            if($scope.userId > 0) {

                UserService.get($routeParams.userId).then(function (response) {

                    var user = response.data;

                    // Just in case the user jumped to the URI directly, we check whether the
                    // user entry is visible or not.
                    // TODO: Handle invisible users at server side?
                    if (user.is_visible) {

                        $scope.name = user.first_name + ' ' + user.last_name;
                        $scope.username = user.username;
                        $scope.email = user.email;
                        $scope.first_name = user.first_name;
                        $scope.last_name = user.last_name;

                        // For some reason we need to create a separate variable 'admin' otherwise
                        // we get strange selection behavior...
                        $scope.is_admin = user.is_admin ? 'true': 'false';
                        // $scope.admin = $scope.is_admin;
                        $scope.is_active = user.is_active ? 'true': 'false';
                        // $scope.active = $scope.is_active;

                        $scope.breadcrumbs = [
                            {url: '#/admin', text: 'Dashboard'},
                            {url: '#/users', text: 'Users'},
                            {url: '#/users/' + $routeParams.userId, text: $scope.name}
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

                if($scope.userId > 0) {

                    // We're saving an existing user
                    UserService.update(
                        $scope.userId,
                        $scope.username,
                        $scope.password1,
                        $scope.password2,
                        $scope.email,
                        $scope.first_name,
                        $scope.last_name,
                        $scope.is_admin === 'true',
                        $scope.is_active === 'true')
                    .then(function (response) {
                        $location.path('/users');
                    }, function (error) {
                        $scope.message = JSON.stringify(error);
                        alert($scope.message);
                    })
                }
                else {

                    // Check that user provided all required fields
                    if(isNull($scope.username))
                        $scope.message = 'Username is empty';
                    if(isNull($scope.email))
                        $scope.message = 'Email is empty';
                    if(isNull($scope.password2))
                        $scope.message = 'Password confirmation is empty';
                    if(isNull($scope.first_name))
                        $scope.message = 'First name is empty';
                    if(isNull($scope.last_name))
                        $scope.message = 'Last name is empty';

                    // If these fields were not specified, use defaults
                    if(isNull($scope.is_admin))
                        $scope.is_admin = false;
                    if(isNull($scope.is_active))
                        $scope.is_active = true;

                    // Make sure the user confirms her password
                    if($scope.password1 != $scope.password2) {
                        $scope.message = 'Passwords do not match';
                    }

                    if(!isNull($scope.message)) {
                        alert($scope.message);
                        return;
                    }

                    // Save the new user
                    UserService.create(
                        $scope.username,
                        $scope.password1,
                        $scope.email,
                        $scope.first_name,
                        $scope.last_name,
                        $scope.is_admin === 'true',
                        $scope.is_active === 'true')
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
        }])
    
    .controller('UserGroupsController', ['$scope', 'TokenService',
        function($scope, TokenService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/user-groups', text: 'User groups'}
            ];
        }])

    .controller('PermissionsController', ['$scope', 'TokenService',
        function($scope, TokenService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/permissions', text: 'Permissions'}
            ];
        }]);
