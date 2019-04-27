//Raspberry Pi Client

var io = require('socket.io-client');
var config = require("./config.json");

var serverAddress = "http://localhost:8080";
//var serverAddress = config.serverAddress;
var pi = config.pi;

var socket = io.connect(serverAddress);

socket.on('reconnecting', function(attempt) {
	if(attempt < 3)
		return;

	console.log("error: failed to connect");
	process.exit();
});

socket.on('disconnect', function() {
	console.log("disconnected");
	process.exit();
});

socket.on('loginPi', function(res) {
	if(res.error) {
		console.log("error: failed to login : "+res);
		process.exit();
	}

	socket.on('command', function(req) {
		console.log(req.config);

		req.error = "";

		socket.emit('command', req);
	});

	//console.log("successfull login");
	//console.log("waiting for commands...");
});

socket.emit('loginPi', pi);
