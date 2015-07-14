var MongoClient = require('mongodb').MongoClient,
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

MongoClient.connect('mongodb://admin:password@ds047672.mongolab.com:47672/wifisniff', function(err, db) {
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

				db.collection('gpsdata').insert(writeObj, function(err, recors) {
					if(err) throw err;
					console.log("inserted data");
				});
			};
		});	
	}
	// weird shit happens but yolo 
	// db.close();
});