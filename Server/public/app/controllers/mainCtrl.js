angular.module('mainCtrl', ['buildingService'])

.controller('mainController', function(Building) {

	var vm = this;

	// Set a processing variable to show loading things
	vm.processing = true;

	// Grab all buildings
	vm.buildings = Building.all();
		

	vm.processing = false;

					
});