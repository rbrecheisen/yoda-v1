'use strict';

angular.module('controllers')

    .controller('FilesController', [
        '$scope', '$location', '$routeParams', '$route', 'Upload', 'TokenService', 'UserService', 'RepositoryService', 'FileService',

        function($scope, $location, $routeParams, $route, Upload, TokenService, UserService, RepositoryService, FileService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'},
                {url: '#/repositories/' + $routeParams.id, text: $routeParams.id},
                {url: '#/repositories/' + $routeParams.id + '/files', text: 'Files'}];

            // TODO: Remove this hack, there should be no DOM manipulation inside controllers
            $('.collapsible').collapsible({
                accordion: true
            });

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

            $scope.uploadFile = function() {
                $location.path('/repositories/' + $scope.repository.id + '/files/0');
            };

            $scope.deleteFile = function(file) {
                FileService.delete($scope.repository.id, file.id).then(function(response) {
                    $route.reload();
                }, function(error) {
                    alert(JSON.stringify(error));
                })
            };
        }])

    .controller('FileController', [
        '$scope', '$location', '$routeParams', 'Upload', 'TokenService', 'UserService', 'RepositoryService', 'FileService', 'FileTypeService', 'ScanTypeService',

        function($scope, $location, $routeParams, Upload, TokenService, UserService, RepositoryService, FileService, FileTypeService, ScanTypeService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'},
                {url: '#/repositories/' + $routeParams.id, text: $routeParams.id},
                {url: '#/repositories/' + $routeParams.id + '/files', text: $routeParams.fileId}];

            $scope.repository = {};
            $scope.repository.id = $routeParams.id;
            $scope.repository.name = '';

            $scope.file = {};
            $scope.file.id = $routeParams.fileId;
            $scope.file.name = '';
            $scope.file.storage_id = '';
            $scope.file.storage_path = '';
            $scope.file.file_type = 0;
            $scope.file.file_type = 0;
            $scope.file.content_type = '';
            $scope.file.size = 0;

            $scope.file_types = [];
            $scope.scan_types = [];
            $scope.selected_file_type = 'binary';
            $scope.selected_scan_type = 'none';

            if($scope.repository.id > 0) {

                RepositoryService.get($scope.repository.id).then(function(response) {

                    $scope.repository = response.data;
                    $scope.breadcrumbs = [
                        {url: '#/admin-dashboard', text: 'Dashboard'},
                        {url: '#/repositories', text: 'Repositories'},
                        {url: '#/repositories/' + $routeParams.id, text: $scope.repository.name},
                        {url: '#/repositories/' + $routeParams.id + '/files', text: $routeParams.fileId}];

                    FileTypeService.getAll().then(function(response) {
                        $scope.file_types = response.data;
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });

                    ScanTypeService.getAll().then(function(response) {
                        $scope.scan_types = response.data;
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });

                    if($scope.file.id > 0) {
                        FileService.get($scope.repository.id, $scope.file.id).then(function(response) {
                            $scope.file = response.data;
                            $scope.breadcrumbs = [
                                {url: '#/admin-dashboard', text: 'Dashboard'},
                                {url: '#/repositories', text: 'Repositories'},
                                {url: '#/repositories/' + $routeParams.id, text: $scope.repository.name},
                                {url: '#/repositories/' + $routeParams.id + '/files', text: $scope.file.name}];
                        }, function(error) {
                            alert(JSON.stringify(error));
                        });
                    }
                }, function(error) {
                    alert(JSON.stringify(error));
                });
            }

            $scope.uploadFile = function(file) {
                FileService.upload($scope.repository.id, file, 11, 18).then(function(response) {
                    $location.path('/repositories/' + $scope.repository.id + '/files');
                }, function(error) {
                    alert(error);
                }, function(evt) {
                    var progress = parseInt(100.0 * evt.loaded / evt.total);
                    console.log('Uploaded: ' + progress + '%');
                });
            };

            $scope.cancelUpload = function() {
                $location.path('/repositories/' + $scope.repository.id + '/files');
            };
        }]);
