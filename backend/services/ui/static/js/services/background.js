'use strict';

angular.module('services')
    .service('BackgroundService', [function() {
        var currentBackgroundClass = 'admin-dashboard';
        return {
            setClass: function(backgroundClass) {
                currentBackgroundClass = backgroundClass;
            },
            getClass: function() {
                return currentBackgroundClass;
            }
        }
    }]);