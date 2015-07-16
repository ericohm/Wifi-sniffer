var MongoClient = require('mongodb').MongoClient,
	request		= require('request'),
	fs 			= require('fs');
/*
var re = /^\d+.\s([GPS_RAW_INT]+)\s(.*)$/;

fs.readFile('gps.txt', 'utf8', function (err,data) {
	if (err) {
		return console.log(err);
	}
	MongoClient.connect('mongodb://admin:password@ds047672.mongolab.com:47672/wifisniff', function(err, db) {
		if(err) {
			console.log(err);
		}
		var dataArray = data.split('\n');
		dataArray.forEach(function(entry) {

			if(entry.match(re)){
				var match = entry.match(re)[2];
				var json = eval('(' + match + ')');

				console.log(match);

				db.collection('gpsdata').insert(json, function(err, records) {
					if (err) throw err;
					console.log("inserted data");
				});
			}
		});
	});
});*/

/*MongoClient.connect('mongodb://admin:password@ds053312.mongolab.com:53312/near', function(err, db) {
	if(err) {
		console.log(err);
	} else {
		console.log("succesfully connected");

		fs.readFile('signals.txt', 'utf8', function(err, data) {
			if(err)
				console.log(err);
			json = JSON.parse(data);
			//console.log(json);

			for(var key in json) {
				//console.log(json[key]);
				var writeObj = {
					mac: key,
					properties: json[key]
				};

				console.log(writeObj);

				db.collection('droneentries').insert(writeObj, function(err, recors) {
					if(err) throw err;
					console.log("inserted data");
				});
			};
		});	
	}
	// weird shit happens but yolo 
	// db.close();
}); */

var headers = {
    'User-Agent':       'Super Agent/0.0.1',
    'Content-Type':     'application/x-www-form-urlencoded',
    'x-access-token': 	'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiT3NjYXIgQWxzaW5nIiwidXNlcm5hbWUiOiJvc2Npc3BybyIsImlkIjoiNTU5YTUyNWFhMzU5Njg5M2QwNTliNDZhIiwiaWF0IjoxNDM2OTY5NTY1LCJleHAiOjE0MzcwNTU5NjV9.6fEpgIO2B0NzTRJfoV3dbwc-3dREgroPqIilJUIY_7Y'
}

fs.readFile('signals.txt', 'utf8', function(err, data) {
			if(err)
				console.log(err);
			json = JSON.parse(data);
			//console.log(json);

			for(var key in json) {
				//console.log(json[key]);
				var writeObj = {
					mac: key,
					properties: json[key]
				};

				writeObj.properties.forEach(function(entry) {
					// Configure the request
					var options = {
					    url: 'https://quiet-citadel-6617.herokuapp.com/api/droneentry/',
					    method: 'POST',
					    headers: headers,
					    form: {
					    	'mac': key, 
					    	'lng': entry.Longitude,
					    	'lat': entry.Latitude,
					    	'signal': entry.Signal,
					    	'time': 	entry.Time
					    }
					};

									// Start the request
				request(options, function (error, response, body) {
				    if (!error && response.statusCode == 200) {
				        // Print out the response body
				        console.log(body);
				    } else {
				    	console.log(error);
				    }
				});

				})

				console.log(writeObj);

				
			};
		});	
