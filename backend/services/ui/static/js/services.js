'use strict';

var TOKENS_URI = 'http://192.168.99.100/auth/tokens';
var USERS_URI  = 'http://192.168.99.100/auth/users';


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

    .service('TokenService', ['$http', '$cookies', '$location',
        function($http, $cookies, $location) {
            return {
                get: function() {
                    return $cookies.get('token');
                },
                create: function(username, password) {
                    return $http({
                        method: 'POST', url: TOKENS_URI,
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

    .service('UserService', ['$http', 'TokenService',
        function($http, TokenService) {
            return {
                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: USERS_URI,
                        headers: TokenService.header()
                    })
                },
                get: function(id) {
                    return $http({
                        method: 'GET',
                        url: USERS_URI + '/' + id,
                        headers: TokenService.header()
                    })
                },
                getByUsername: function(username) {
                    return $http({
                        method: 'GET',
                        url: USERS_URI + '?username=' + username,
                        headers: TokenService.header()
                    })
                },
                getByEmail: function(email) {
                    return $http({
                        method: 'GET',
                        url: USERS_URI + '?email=' + email,
                        headers: TokenService.header()
                    })
                },
                create: function(username, password, email) {
                    return $http({
                        method: 'POST',
                        url: USERS_URI,
                        headers: TokenService.header(),
                        data: {
                            'username': username,
                            'password': password,
                            'email': email
                        }
                    })
                },
                update: function(id, username, password, email) {
                    return $http({
                        method: 'PUT',
                        url: USERS_URI + '/' + id,
                        headers: TokenService.header(),
                        data: {
                            'username': username,
                            'password': password,
                            'email': email
                        }
                    })
                },
                delete: function(id) {
                    return $http({
                        method: 'DELETE',
                        url: USERS_URI + '/' + id,
                        headers: TokenService.header()
                    })
                }
            }
        }]);

    // .service('UserGroupService', ['$http', 'TokenService',
    //     function($http, TokenService) {
    //         return {
    //             getAll: function() {
    //                 return $http({
    //                     method: 'GET',
    //                     url: USER_GROUPS_URI,
    //                     headers: TokenService.header()
    //                 })
    //             },
    //             get: function(id) {
    //                 return $http({
    //                     method: 'GET',
    //                     url: USER_GROUPS_URI + '/' + id,
    //                     headers: TokenService.header()
    //                 })
    //             },
    //             getByName: function(name) {
    //                 return $http({
    //                     method: 'GET',
    //                     url: USER_GROUPS_URI + '?name=' + name,
    //                     headers: TokenService.header()
    //                 })
    //             },
    //             create: function(name) {
    //                 return $http({
    //                     method: 'POST',
    //                     url: USER_GROUPS_URI,
    //                     headers: TokenService.header(),
    //                     data: {
    //                         'name': name
    //                     }
    //                 })
    //             },
    //             update: function(id, name) {
    //                 return $http({
    //                     method: 'PUT',
    //                     url: USER_GROUPS_URI + '/' + id,
    //                     headers: TokenService.header(),
    //                     data: {
    //                         'name': name
    //                     }
    //                 })
    //             },
    //             delete: function(id) {
    //                 return $http({
    //                     method: 'DELETE',
    //                     url: USER_GROUPS_URI + '/' + id,
    //                     headers: TokenService.header()
    //                 })
    //             },
    //             addUser: function(id, userId) {
    //                 return $http({
    //                     method: 'PUT',
    //                     url: USER_GROUPS_URI + '/' + id + '/users/' + userId,
    //                     headers: TokenService.header()
    //                 })
    //             },
    //             removeUser: function(id, userId) {
    //                 return $http({
    //                     method: 'DELETE',
    //                     url: USER_GROUPS_URI + '/' + id + '/users/' + userId,
    //                     headers: TokenService.header()
    //                 })
    //             }
    //         }
    //     }])
    //
    // .service('PermissionService', ['$http', 'TokenService',
    //     function($http, TokenService) {
    //         return {
    //             create: function(action, principal_id, principal_type, resource_id, granted) {
    //                 return $http({
    //                     method: 'POST',
    //                     url: PERMISSIONS_URI,
    //                     headers: TokenService.header(),
    //                     data: {
    //                         'action': action,
    //                         'principal_id': principal_id,
    //                         'principal_type': principal_type,
    //                         'resource_id': resource_id,
    //                         'granted': granted
    //                     }
    //                 })
    //             },
    //             delete: function(id) {
    //                 return $http({
    //                     method: 'DELETE',
    //                     url: PERMISSIONS_URI + '/' + id,
    //                     headers: TokenService.header()
    //                 })
    //             }
    //         }
    //     }]);
