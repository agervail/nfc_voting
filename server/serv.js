var http = require('http');
var express = require('express');
var mongoose = require('mongoose');
var mqtt = require('mqtt')
var Schema = mongoose.Schema;
var restify = require('express-restify-mongoose')
 
///////////////////////////////////
/////// MONGODB  //////////////////
//////////////////////////////////
//Connection to the a mongodb database path localhost:port/nameOfCollection
mongoose.connect("mongodb://localhost:27017/nfcDB", function(err) {
    if (err) {
        throw err;
    }
});
 
//Definition of a schema
var Temperature = new Schema({
    _id: Number,
    vote: Number
});
//Creation of the model
var TemperatureModel = mongoose.model('vote3', Temperature);
 
 
///////////////////////////////////
/////// MQTT  //////////////////
//////////////////////////////////
 
client = mqtt.createClient(1883, '192.168.1.20');
client2 = mqtt.createClient(1883, '127.0.0.1');
client.subscribe('vote');
 
var i = 0;
client.on('message', function(topic, message) {
    console.log(message);
    var s = message.split(' ');
//	  console.log('fdsk' + s[1]);
    var myTemperatureModel = new TemperatureModel({_id: s[0], vote: s[1]});
    myTemperatureModel.save(function(err) {
        if (err) {
				  if (err.err.indexOf("duplicate key" != -1)){
						console.log('La personne a deja vote');
				  } else {
						console.log('Erreur inconnue');
						console.log(err.err);
				  }
        } else {
					client2.publish('success', s[1]);
        	console.log('Le vote a été ajouté avec succès');
				}
    });
});
 
 
var app = express();
app.configure(function() {
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    restify.serve(app, TemperatureModel);
});
 
 
//Run the server
http.createServer(app).listen(4242, function() {
    console.log("Express server listening on port 4242");
});
