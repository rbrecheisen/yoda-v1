'use strict';

angular.module('services')

    .service('PermissionService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var permissionsUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/auth/permissions';

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