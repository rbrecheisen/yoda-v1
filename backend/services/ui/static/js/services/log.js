'use strict';

angular.module('services')

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
        }]);