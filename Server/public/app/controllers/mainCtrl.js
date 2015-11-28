angular.module('mainCtrl', ['uiGmapgoogle-maps', 'buildingService'])

.controller('mainController', function($scope, uiGmapGoogleMapApi, Building) {

	var vm = this;

	//vm.processing  = true;

	// uiGmapGoogleMapApi is a promise.
    // The "then" callback function provides the google.maps object.
    uiGmapGoogleMapApi.then(function(maps) {

    	$scope.map = {
	  		center: { latitude: 33.7753, longitude: -84.3965 },
	  		zoom: 16
		};

		Building.all()
			.success(function(data) {
				vm.buildings = data;
				
				Building.getOccupancy(vm.buildings[0].bid)
					.success(function(data1) {
						vm.buildings[0].occupancy = data1.total_occupancy;
					});
				
				Building.getOccupancy(vm.buildings[1].bid)
					.success(function(data2) {
						vm.buildings[1].occupancy = data2.total_occupancy;
					});

			});
    });	
});