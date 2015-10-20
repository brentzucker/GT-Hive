// To run: node server.js

/* Configure Express with Node */

var express = require('express');
var app = express();

/* Run App */

app.listen(8080);

/* * * * * * * * * * * * *
 * API End Points 
 * * * * * * * * * * * * */

// All Building Id's and Names (could definitely cache this initial request into a text file or database)
app.get('/api/building_ids_names.json', function (request, response) {

	/* Request GT Places API */
	
	var http = require('http'); // import http module
	var gtplaces_url = 'http://m.gatech.edu/widget/gtplaces/content/api/buildings';
	
	http.request(gtplaces_url, function(res) {
		
		var buildings_info = '';

		res.on('data', function (chunk) {
			buildings_info += chunk;
		});

		res.on('end', function () {
			
			// console.log(buildings_info); // Print out request to gtplaces

			// Parse JSON, pull out building id's and names
			buildings = parseBuildingsInfo(buildings_info);

			// Return to /api/building_ids.json
			json = '{"buildings": ' + buildings + '}';
			response.send(json);
		});		
	}).end();	
});

/* * * * * * * * * * * * *
 * Helper Functions 
 * * * * * * * * * * * * */

// Returns building id's and names [{"b_id": <id-(String)>, "name": <name-(String)>},...]
function parseBuildingsInfo(buildings_info) {

	buildings_info_obj = JSON.parse(buildings_info);

	json = '{[';
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