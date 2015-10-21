// To run: node server.js

var hostname = require('os').hostname();
var port = 8080;

/* Configure Express with Node */

var express = require('express');
var app = express();

/* Run App */

app.listen(port);

/* * * * * * * * * * * * *
 * API End Points 
 * * * * * * * * * * * * */

// import http module
global.http = require('http'); 

// All Building Id's and Names (could definitely cache this initial request into a text file or database)
app.get('/api/building_ids_names', function (request, response) {

	/* Request GT Places API */
	
	var gtplaces_url = 'http://m.gatech.edu/widget/gtplaces/content/api/buildings';

	global.http.get(gtplaces_url, function(res) {
		
		var buildings_info = '';
		res.on('data', function (chunk) {
			buildings_info += chunk;
		});

		res.on('end', function () {
			
			// Parse JSON, pull out building id's and names
			var buildings = parseBuildingsInfo(buildings_info);

			// Return to /api/building_ids.json
			var json = '{"buildings": ' + buildings + '}';
			response.send(json);
		});		
	}).end();
});

// Reads archived /api/building_ids_names from text file
app.get('/api/building_ids_names_local', function (request, response) {

	var json = getBuildingsTextFile();
	response.send(json);
});

// Location info of All Buildings
app.get('/api/locationinfo_allbuildings', function (request, response) {
	
	// Get Building ids
	var building_ids_names_obj = (JSON.parse(getBuildingsTextFile())).buildings;
	var buildings = building_ids_names_obj;

	// API for locations
	var gtwhereami = 'http://gtwhereami.herokuapp.com/';
	var endpoint = 'locationinfo?bid=';

	// Generate Global Associative Array for reference in Asynch call
	global.buildings = [];
	for (var i = 0; i < buildings.length; i++) {
		global.buildings['b_id: ' + buildings[i].b_id] = buildings[i].name;
	}

	// Loop through all building id's and request locationinfo
	for (var i = 0; i < buildings.length; i++) {

		// Global Variables to keep track of asynchronous calls
		global.occupancies = [];
		global.count = 0;
		global.buildings_length = buildings.length;
		
		// Custom URL for each building
		var building_occupation_url = gtwhereami + endpoint + buildings[i].b_id;

		global.http.get(building_occupation_url, function(gtwhereami_response) {

			// Get building id from the socket of the asynchronous call (really struggled trying to figure this out, probably a better way)
			var b_id = gtwhereami_response.socket._httpMessage.path.substring(endpoint.length + 1);

			var occupancy = '';
			gtwhereami_response.on('data', function (chunk) {
				occupancy += chunk;
			});

			gtwhereami_response.on('end', function () {

				// Occupancy returned, count until all are returned
				var occ = (JSON.parse(occupancy)).occupancy;
				var json = '{';
				json += '"b_id": "' + b_id + '", ';
				json += '"occupancy": ' + occ + ', ';
				json += '"name": "' + global.buildings['b_id: ' + b_id] + '"';
				json += '}';

				// Push building object to global array
				global.occupancies.push(json);
				global.count++;

				// Return json string when all occupancy requests have terminated
				if (global.count >= global.buildings_length) {

					var final_json = '{"occupancies": [' + global.occupancies + ']}'; 
					response.send(final_json);
				}
			});
		});
	}
});

/* * * * * * * * * * * * *
 * Helper Functions 
 * * * * * * * * * * * * */

function getBuildingsTextFile() {
	var fs  = require("fs");
	var json = fs.readFileSync('building_ids_names.json').toString();
	return json;
}

// Returns building id's and names [{"b_id": <id-(String)>, "name": <name-(String)>},...]
function parseBuildingsInfo(buildings_info) {

	var buildings_info_obj = JSON.parse(buildings_info);

	var json = '{[';
	for (var i = 0 ; i < buildings_info_obj.length; i++) {

		json += '{';
		json += '"b_id": "' + buildings_info_obj[i].b_id + '"';
		json += ', ';
		json += '"name": "' + buildings_info_obj[i].name + '"';
		json += '}';
		if (i + 1 < buildings_info_obj.length) json += ', ';
	}
	json += ']}';

	return json;
}