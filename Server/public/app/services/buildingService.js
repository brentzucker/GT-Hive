angular.module('buildingService', [])

.factory('Building', function($http) {

	var buildingFactory = {};

	buildingFactory.all = function() {
		var buildings = [
			{
				"name": "Clough Undergraduate Learning Commons",
				"occupancy": "50"
			},

			{
				"name": "Campus Recreation Center",
				"occupancy": "40"
			},

			{
				"name": "Library",
				"occupancy": "30"
			}
		];

		return buildings;
	};

	return buildingFactory;
});