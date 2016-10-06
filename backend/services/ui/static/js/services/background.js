'use strict';

angular.module('services')

    .service('BackgroundService', [function() {

        var currentBackgroundClass = '';

        return {

            getClass: function() {
                return currentBackgroundClass;
            },

            setClass: function(backgroundClass) {
                currentBackgroundClass = backgroundClass;
            }
        }
    }]);