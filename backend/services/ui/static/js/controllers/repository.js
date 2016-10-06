'use strict';

angular.module('controllers')

    .controller('RepositoriesController', ['$scope', '$location', '$route', 'TokenService', 'UserService', 'RepositoryService',

        function ($scope, $location, $route, TokenService, UserService, RepositoryService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'}
            ];

            // TODO: Remove this hack, there should be no DOM manipulation inside controllers
            $('.collapsible').collapsible({
                accordion: true
            });

            RepositoryService.getAll().then(function(response) {
                $scope.repositories = [];
                for(var i = 0; i < response.data.length; i++) {
                    $scope.repositories.push(response.data[i]);
                }
            }, function(error) {
                    alert(JSON.stringify(error));
            });

            $scope.createRepository = function() {
                $location.path('/repositories/0');
            };

            $scope.editRepository = function(repository) {
                $location.path('/repositories/' + repository.id);
            };

            $scope.deleteRepository = function(repository) {
                RepositoryService.delete(repository.id).then(function(response) {
                    $route.reload();
                }, function(error) {
                    alert(JSON.stringify(error));
                })
            };

            $scope.viewFiles = function(repository) {
                $location.path('/repositories/' + repository.id + '/files');
            };
        }])

    .controller('RepositoryController', ['$scope', '$location', '$routeParams', 'TokenService', 'UserService', 'RepositoryService', 'BackgroundService',

        function($scope, $location, $routeParams, TokenService, UserService, RepositoryService, BackgroundService) {

            // BackgroundService.setClass('repository');

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'},
                {url: '#/repositories/' + $routeParams.id, text: $routeParams.id}];

            $scope.repository = {};
            $scope.repository.id = $routeParams.id;
            $scope.repository.name = '';

            if($scope.repository.id > 0) {
                RepositoryService.get($scope.repository.id).then(function(response) {
                    $scope.repository = response.data;
                    $scope.breadcrumbs = [
                        {url: '#/admin-dashboard', text: 'Dashboard'},
                        {url: '#/repositories', text: 'Repositories'},
                        {url: '#/repositories/' + $routeParams.id, text: $scope.repository.name}]
                }, function(error) {
                    alert(JSON.stringify(error));
                });
            }

            $scope.saveRepository = function() {
                if($scope.repository.id > 0) {
                    RepositoryService.update($scope.repository.id, $scope.repository.name).then(function(response) {
                        $location.path('/repositories');
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });
                } else {
                    if(isNull($scope.repository.name))
                        alert('Name is empty');
                    RepositoryService.create($scope.repository.name).then(function(response) {
                        $location.path('/repositories');
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });
                }
            };

            $scope.cancelSave = function() {
                $location.path('/repositories');
            };
        }]);