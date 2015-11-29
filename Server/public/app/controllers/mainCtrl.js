angular.module('mainCtrl', ['uiGmapgoogle-maps', 'buildingService'])

.controller('mainController', function($scope, uiGmapGoogleMapApi, Building, $log) {

	var vm = this;

	$scope.markers = [];

	vm.processing  = true;

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

				var bids = [];

				for (var i = 0; i < vm.buildings.length; i++) {
					bids.push(vm.buildings[i].bid);
				}

				Building.updateOccupancies(bids)
					.success(function(updated) {

						for (var i = 0; i < vm.buildings.length; i++) {
							vm.buildings[i].occupancy = updated.occupancies[vm.buildings[i].bid].occupancy;
						}

						vm.processing = false;
					});

				// var createMarker = function(i, title, latitude, longitude) {
				// 	var ret = {
				// 		title: title,
				// 		latitude: latitude,
				// 		longitude: longitude,
				// 		icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
				// 	};
				// 	ret["id"] = i;
				// 	return ret;
				// }

				// for (var i = 0; i < vm.buildings.length; i++) {
				// 	$scope.markers.push(createMarker(i, vm.buildings[i].name, vm.buildings[i].latitude, vm.buildings[i].longitude));
				// }
			});
    });	
});