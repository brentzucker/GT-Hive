angular.module('mainCtrl', ['uiGmapgoogle-maps', 'buildingService'])

.controller('mainController', function($scope, uiGmapGoogleMapApi, Building) {

	var vm = this;

	vm.processing  = true;

	// uiGmapGoogleMapApi is a promise.
    // The "then" callback function provides the google.maps object.
    uiGmapGoogleMapApi.then(function(maps) {

    	$scope.map = {
	  		center: { latitude: 33.7753, longitude: -84.3965 },
	  		zoom: 16
		};

		vm.buildings = Building.all();

		vm.processing = false;
    });	
});