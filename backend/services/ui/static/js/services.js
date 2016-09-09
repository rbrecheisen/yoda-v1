'use strict';

angular.module('services', ['ngResource', 'ngCookies'])

    .service('Log', [
        function() {
            return {
                now: function() {
                    var t = Date.now();
                    return t.getDay() + '-' + t.getMonth() + '-' + t.getYear() + ' ' +
                        t.getHours() + ':' + t.getMinutes() + ':' + t.getSeconds() + '.' + t.getMilliseconds();
                },
                info: function(caller, message) {
                    console.log('[INFO] ' + this.now() + ' ' + caller + ' ' + message);
                },
                error: function(caller, message) {
                    console.log('[ERROR] ' + this.now() + ' ' + caller + ' ' + message);
                }
            }
        }])

    .service('TokenService', ['$http', '$cookies', '$location', 'environ',
        function($http, $cookies, $location, environ) {
            var tokensUri = 'http://' + environ.UI_SERVICE_HOST + '/auth/tokens';
            return {
                get: function() {
                    return $cookies.get('token');
                },
                create: function(username, password) {
                    return $http({
                        method: 'POST', url: tokensUri,
                        headers: {'Authorization': 'Basic ' + btoa(username + ':' + password)}
                    })
                },
                update: function(token) {
                    $cookies.put('token', token);
                },
                delete: function() {
                    $cookies.remove('token');
                },
                header: function() {
                    return {'Authorization': 'Basic ' + btoa(this.get() + ':unused')}
                },
                check: function() {
                    var token = this.get();
                    if(token === undefined || token === "") {
                        $location.path('/login');
                    }
                }
            }
        }])

    .service('UserService', ['$http', 'TokenService', 'environ',
        function($http, TokenService, environ) {
            var usersUri = 'http://' + environ.UI_SERVICE_HOST + '/auth/users';
            return {
                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: usersUri,
                        headers: TokenService.header()
                    })
                },
                get: function(id) {
                    return $http({
                        method: 'GET',
                        url: usersUri + '/' + id,
                        headers: TokenService.header()
                    })
                },
                getByUsername: function(username) {
                    return $http({
                        method: 'GET',
                        url: usersUri + '?username=' + username,
                        headers: TokenService.header()
                    })
                },
                getByEmail: function(email) {
                    return $http({
                        method: 'GET',
                        url: usersUri + '?email=' + email,
                        headers: TokenService.header()
                    })
                },
                create: function(username, password, email, first_name, last_name, is_admin) {
                    return $http({
                        method: 'POST',
                        url: usersUri,
                        headers: TokenService.header(),
                        data: {
                            'username': username,
                            'password': password,
                            'email': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'is_admin': is_admin
                        }
                    })
                },
                update: function(user) {
                    return $http({
                        method: 'PUT',
                        url: usersUri + '/' + user.id,
                        headers: TokenService.header(),
                        data: {
                            'username': user.username,
                            'password': user.password,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'is_admin': user.is_admin
                        }
                    })
                },
                delete: function(user) {
                    return $http({
                        method: 'DELETE',
                        url: usersUri + '/' + user.id,
                        headers: TokenService.header()
                    })
                }
            }
        }])

    .service('UserGroupService', ['$http', 'TokenService', 'environ',
        function($http, TokenService, environ) {
            var userGroupsUri = 'http://' + environ.UI_SERVICE_HOST + '/auth/user-groups';
            return {
                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: userGroupsUri,
                        headers: TokenService.header()
                    })
                },
                get: function(id) {
                    return $http({
                        method: 'GET',
                        url: userGroupsUri + '/' + id,
                        headers: TokenService.header()
                    })
                },
                getByName: function(name) {
                    return $http({
                        method: 'GET',
                        url: userGroupsUri + '?name=' + name,
                        headers: TokenService.header()
                    })
                },
                create: function(name) {
                    return $http({
                        method: 'POST',
                        url: userGroupsUri,
                        headers: TokenService.header(),
                        data: {
                            'name': name
                        }
                    })
                },
                update: function(id, name) {
                    return $http({
                        method: 'PUT',
                        url: userGroupsUri + '/' + id,
                        headers: TokenService.header(),
                        data: {
                            'name': name
                        }
                    })
                },
                delete: function(id) {
                    return $http({
                        method: 'DELETE',
                        url: userGroupsUri + '/' + id,
                        headers: TokenService.header()
                    })
                },
                addUser: function(id, userId) {
                    return $http({
                        method: 'PUT',
                        url: userGroupsUri + '/' + id + '/users/' + userId,
                        headers: TokenService.header()
                    })
                },
                removeUser: function(id, userId) {
                    return $http({
                        method: 'DELETE',
                        url: userGroupsUri + '/' + id + '/users/' + userId,
                        headers: TokenService.header()
                    })
                }
            }
        }])

    .service('PermissionService', ['$http', 'TokenService', 'environ',
        function($http, TokenService, environ) {
            var permissionsUri = 'http://' + environ.UI_SERVICE_HOST + '/auth/permissions';
            return {
                create: function(action, principal_id, principal_type, resource_id, granted) {
                    return $http({
                        method: 'POST',
                        url: permissionsUri,
                        headers: TokenService.header(),
                        data: {
                            'action': action,
                            'principal_id': principal_id,
                            'principal_type': principal_type,
                            'resource_id': resource_id,
                            'granted': granted
                        }
                    })
                },
                delete: function(id) {
                    return $http({
                        method: 'DELETE',
                        url: permissionsUri + '/' + id,
                        headers: TokenService.header()
                    })
                }
            }
        }]);
