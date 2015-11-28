angular.module('buildingService', [])

.factory('Building', function($http) {

	var buildingFactory = {};

	buildingFactory.all = function() {
		return $http.get('/api/angular/buildings');
	};

	buildingFactory.getOccupancy = function(bid) {
		return $http.get('/api/locationinfo/b_id=' + bid);
	};

	return buildingFactory;
});