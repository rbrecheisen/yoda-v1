'use strict';

angular.module('services')

    .service('UserGroupService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var userGroupsUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/auth/user-groups';

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
        }]);