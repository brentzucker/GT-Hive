// To run: node server.js

global.hostname = require('os').hostname();
global.port = 8080;

/* Configure Express with Node */

var express = require('express');
var app = express();

/* Run App */

app.listen(global.port);

/* * * * * * * * * * * * *
 * API End Points 
 * * * * * * * * * * * * */

// import http module
global.http = require('http'); 

// Array of all Buildings (b_id, name)
app.get('/api/buildings', function (request, response) {
	// cached from http://m.gatech.edu/widget/gtplaces/content/api/buildings
	var json = getBuildingsTextFile();
	response.send(json);
});

// Location info of All Buildings
app.get('/api/locationinfo/buildings', function (request, response) {
	
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
				var json = '"' + b_id + '" : {';
				json += '"b_id": "' + b_id + '", ';
				json += '"occupancy": ' + occ + ', ';
				json += '"name": "' + global.buildings['b_id: ' + b_id] + '"';
				json += '}';

				// Push building object to global array
				global.occupancies.push(json);
				global.count++;

				// Return json string when all occupancy requests have terminated
				if (global.count >= global.buildings_length) {

					var final_json = '{"occupancies": {' + global.occupancies + '}}'; 
					response.send(final_json);
				}
			});
		});
	}
});

// Location info of All Buildings
app.get('/api/locationinfo/rooms', function (request, response) {

	// Get Building/Room ids [b_id-room, ...]
	var buildings = (JSON.parse(getBuildingRoomsTextFile())).buildings;
	
	var rooms_list = [];
	for (var i = 0; i < buildings.length; i++) {
		for (var j = 0; j < buildings[i].rooms.length; j++) {
			rooms_list.push(buildings[i].b_id + '-' + buildings[i].rooms[j]);
		}
	}

	// API for locations
	var gtwhereami = 'http://gtwhereami.herokuapp.com';
	var uri = '/locationinfo?';
	var bid = 'bid=';
	var room = '&room=';

	for (var i = 0; i < rooms_list.length; i++) {
		var b_id = rooms_list[i].split("-")[0];
		var room_no = rooms_list[i].split("-")[1];
		var url = gtwhereami + uri + bid + b_id + room + room_no;
		
		// Global Variables to keep track of asynchronous calls
		global.occupancies = [];
		global.count = 0;

		global.http.get(url, function(gtwhereami_response) {

			// Get building id from the socket of the asynchronous call (really struggled trying to figure this out, probably a better way)
			var raw_b_id_room = gtwhereami_response.socket._httpMessage.path.substring('/locationinfo?bid='.length).split("&");
			var b_id = raw_b_id_room[0];
			var room = raw_b_id_room[1].substring('room='.length);

			var occupancy = '';
			gtwhereami_response.on('data', function (chunk) {
				occupancy += chunk;
			});

			gtwhereami_response.on('end', function () {

				// Occupancy returned, count until all are returned
				var occ = '';
				try {
				    occ = (JSON.parse(occupancy)).occupancy;
				} catch(err) {
				    occ = '';
				    console.log('Bad Request: ' + b_id + '-' + room);
				}

				var json_obj = {};
				json_obj.ap = b_id + '-' + room;
				json_obj.b_id = b_id;
				json_obj.room = room;
				json_obj.occupancy = occ;

				// Push building object to global array
				global.occupancies.push(json_obj);
				global.count++;

				// Return json string when all occupancy requests have terminated
				if (global.count >= rooms_list.length) {

					var final_json = '{"occupancies": ' + JSON.stringify(global.occupancies) + '}'; 
					response.send(final_json);
					console.log('done');
				}
			});
		});
	}
});

app.get('/api/locationinfo/:str', function (request, response) {
	var str = request.params.str;

	/* Parse Input String */
	var buildings = parseBuildingString(str);

	/* Request Location Info for each building
	 * TODO: Reuqest location info for room */
	var uri = '/api/locationinfo/buildings';
	var url = 'http://' + global.hostname + ':' + global.port + uri;

	global.http.get(url, function(res) {

		var data = '';
		res.on('data', function (chunk) {
			data += chunk;
		});

		res.on("end", function() {
			var occ_list = JSON.parse(data);

			var occupancies = [];
			var total_occupancy = 0;
			for (var i = 0; i < buildings.length; i++) {

				var b_id = buildings[i].b_id;
				var occupancy = occ_list.occupancies[buildings[i].b_id].occupancy
				var json = {b_id : occupancy};
				occupancies.push(json);

				total_occupancy += occupancy;
			}
			var final_json = {};
			final_json['total_occupancy'] = total_occupancy;
			final_json['occupancies'] = occupancies;
			response.send(final_json);
		});
	});
});

/* * * * * * * * * * * * *
 * Helper Functions 
 * * * * * * * * * * * * */

function readFromTextFile(filename) {
	var fs  = require("fs");
	var txt = fs.readFileSync(filename).toString();
	return txt;	
}

function getBuildingsTextFile() {
	var filename = 'building_ids_names.txt';
	var json = readFromTextFile(filename);
	return json;
}

function getBuildingRoomsTextFile() {
	var filename = 'buildings_rooms.txt';
	var json = readFromTextFile(filename);
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

// Parse dynamic endpoint return array of buildings (i.e. b_id=81&b_id=33 => [b_id: 81, b_id: 33])
function parseBuildingString(str) {
	var tokens = str.split("&");
	var buildings = [];
	for (var i = 0; i < tokens.length; i++) {
		if (tokens[i].split("=").length === 2 && tokens[i].split("=")[0] === "b_id") {

			// i.e. [b_id, 81-337] or [b_id, 81]
			var b_id_raw_array = tokens[i].split("=");

			// i.e. [81] or [81, 337]
			var b_id_array = b_id_raw_array[1].split("-");

			if (b_id_array.length == 1 && b_id_array[0] != '') {
				// request just b_id
				var building = {'b_id': b_id_array[0]};
				buildings.push(building);
			} else if (b_id_array.length == 2) {
				// request b_id and room
				var building = {'b_id': b_id_array[0],
								'room': b_id_array[1]};
				buildings.push(building);
			} else {
				// bad request
			}
		} else {
			// bad request
			response.send('Bad Request: ' + str);
			buildings = [];
			break;
		}
	}
	console.log(buildings);
	return buildings;
}