// This code was taken from
// https://gist.github.com/viniciusmelquiades/66ed8039e3709b126e52

(function () {
    'use strict';

    angular
        .module('app')
        .directive('select', materialSelect);

    materialSelect.$inject = ['$timeout'];

    function materialSelect($timeout) {
        var directive = {
            link: link,
            restrict: 'E',
            require: '?ngModel'
        };

        function link(scope, element, attrs, ngModel) {
            if (ngModel) {
                ngModel.$render = create;
            } else {
                $timeout(create);
            }

            function create() {
                element.material_select();
            }

            //if using materialize v0.96.0 use this
            element.one('$destroy', function () {
                element.material_select('destroy');
            });

            //not required in materialize v0.96.0
            element.one('$destroy', function () {
                var parent = element.parent();
                if (parent.is('.select-wrapper')) {
                    var elementId = parent.children('input').attr('data-activates');
                    if (elementId) {
                        $('#' + elementId).remove();
                    }
                    parent.remove();
                    return;
                }

                element.remove();
            });
        }

        return directive;
    }

})();