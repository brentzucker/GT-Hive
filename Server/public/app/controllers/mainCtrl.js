angular.module('mainCtrl', ['uiGmapgoogle-maps'])

.controller('mainController', function($scope, uiGmapGoogleMapApi) {

	var vm = this;

	vm.processing  = true;

	// uiGmapGoogleMapApi is a promise.
    // The "then" callback function provides the google.maps object.
    uiGmapGoogleMapApi.then(function(maps) {

    	$scope.map = {
	  		center: { latitude: 33.7758, longitude: -84.3947 },
	  		zoom: 16
		};

		vm.processing = false;
    });	
});