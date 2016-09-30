'use strict';

angular.module('services')

    .service('TokenService', ['$http', '$cookies', '$location', 'environ',

        function($http, $cookies, $location, environ) {

            var tokensUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/auth/tokens';

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
        }]);