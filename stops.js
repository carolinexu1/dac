// import statements
var https = require('https');
const express = require('express');
var router = express.Router();
var fs = require('fs');


router.get('/stops_form', function(req,res) {
    console.log('stops')
    res.render('stops_form');
});

module.exports = router;

