var express = require('express');
var router = express.Router();
var env = require('../env');
var request = require('request');

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Getter' });
});

router.get('/spotify/authorize', function(req, res, next) {
	var authString = new Buffer(env.getSpotifyClientId() + ':' + env.getSpotifyClientSecret()).toString('base64');	
	var options = {
		url: 'https://accounts.spotify.com/api/token',
		path: '/api/token',
		method: 'POST',
		headers: {
			'Authorization': 'Basic ' + authString
		},
		form: {
			'grant_type': 'client_credentials'
		},
		json: true
	};
	request.post(options, function(err, res_, body) {
		if (err || res_.statusCode !== 200) {
			res.sendStatus(500);
			return;
		}
		res.send(body);
	});
});

module.exports = router;
