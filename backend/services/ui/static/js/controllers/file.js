'use strict';

angular.module('controllers')

    .controller('FilesController', [
        '$scope', '$location', '$routeParams', 'TokenService', 'UserService', 'RepositoryService', 'FileService',

        function($scope, $location, $routeParams, TokenService, UserService, RepositoryService, FileService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'},
                {url: '#/repositories/' + $routeParams.id, text: $routeParams.id},
                {url: '#/repositories/' + $routeParams.id + '/files', text: 'Files'}];

            $scope.repository = {};
            $scope.repository.id = $routeParams.id;
            $scope.repository.name = '';
            $scope.files = [];

            if($scope.repository.id > 0) {
                RepositoryService.get($scope.repository.id).then(function(response) {
                    $scope.repository = response.data;
                    $scope.breadcrumbs = [
                        {url: '#/admin-dashboard', text: 'Dashboard'},
                        {url: '#/repositories', text: 'Repositories'},
                        {url: '#/repositories/' + $routeParams.id, text: $scope.repository.name},
                        {url: '#/repositories/' + $routeParams.id + '/files', text: 'Files'}];
                    FileService.getAll($scope.repository.id).then(function(response) {
                        $scope.files = response.data;
                    }, function(error) {
                        alert(JSON.stringify(error));
                    })
                }, function(error) {
                    alert(JSON.stringify(error));
                });
            }
        }]);
