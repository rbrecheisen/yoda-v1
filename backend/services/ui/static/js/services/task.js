'use strict';

angular.module('services')

    .service('TaskService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var tasksUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/tasks';

            return {

                getByUsername: function(username) {
                    return $http({
                        method: 'GET',
                        url: tasksUri + '?username=' + username,
                        headers: TokenService.header()
                    })
                },

                get: function(id) {
                    return $http({
                        method: 'GET',
                        url: tasksUri + '/' + id,
                        headers: TokenService.header()
                    })
                },

                create: function(pipeline_name, params) {
                    return $http({
                        method: 'POST',
                        url: tasksUri,
                        headers: TokenService.header(),
                        data: {
                            'pipeline_name': pipeline_name,
                            'params': params
                        }
                    })
                }
            }
        }]);