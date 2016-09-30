'use strict';

angular.module('services')

    .service('RepositoryService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var repositoriesUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/repositories';

            return {

                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: repositoriesUri,
                        headers: TokenService.header()
                    })
                },

                get: function(id) {
                    return $http({
                        method: 'GET',
                        url: repositoriesUri + '/' + id,
                        headers: TokenService.header()
                    })
                },

                getByName: function(name) {
                    return $http({
                        method: 'GET',
                        url: repositoriesUri + '?name=' + name,
                        headers: TokenService.header()
                    })
                },

                create: function(name) {
                    return $http({
                        method: 'POST',
                        url: repositoriesUri,
                        headers: TokenService.header(),
                        data: {
                            'name': name
                        }
                    })
                },

                update: function(id, name) {
                    return $http({
                        method: 'PUT',
                        url: repositoriesUri + '/' + id,
                        headers: TokenService.header(),
                        data: {
                            'name': name
                        }
                    })
                },

                delete: function(id) {
                    return $http({
                        method: 'DELETE',
                        url: repositoriesUri + '/' + id,
                        headers: TokenService.header()
                    })
                }
            }
        }]);