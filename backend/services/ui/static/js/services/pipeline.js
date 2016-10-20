'use strict';

angular.module('services')

    .service('PipelineService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var pipelinesUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/pipelines';

            return {

                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: pipelinesUri,
                        headers: TokenService.header()
                    })
                },

                get: function(id) {
                    return $http({
                        method: 'GET',
                        url: pipelinesUri + '/' + id,
                        headers: TokenService.header()
                    })
                }
            }
        }]);