'use strict';

angular.module('services')

    .service('UserService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var usersUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/auth/users';
            var currentUser = null;

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

                create: function(username, password, email, first_name, last_name, is_admin, is_active) {
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
                            'is_admin': is_admin,
                            'is_active': is_active
                        }
                    })
                },

                update: function(id, username, password, password_new, email, first_name, last_name, is_admin, is_active) {
                    return $http({
                        method: 'PUT',
                        url: usersUri + '/' + id,
                        headers: TokenService.header(),
                        data: {
                            'username': username,
                            'password': password,
                            'password_new': password_new,
                            'email': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'is_admin': is_admin,
                            'is_active': is_active
                        }
                    })
                },

                delete: function(id) {
                    return $http({
                        method: 'DELETE',
                        url: usersUri + '/' + id,
                        headers: TokenService.header()
                    })
                },

                getCurrentUser: function() {
                    return currentUser;
                },

                setCurrentUser: function(user) {
                    currentUser = user;
                }
            }
        }]);