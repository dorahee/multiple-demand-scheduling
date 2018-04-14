#! /usr/bin/env node
// app.js:
var express = require('express');
var app = express();
var hbs = require('hbs');
var fs = require('fs');

app.set('view engine', 'html');
app.set('views', __dirname);
app.use(express.static('./'));
app.engine('html', hbs.__express);

// define various routes:
app.get('/', function (req, res) {
    res.render('index', {title: 'Home'});
});

app.get('/dates', function (req, res) {
    fs.readdir("./results", function (err, items) {

        items = items.filter(function (x) {
            return !x.startsWith(".")
        });

        items = items.reverse();

        res.send(items);
    });
});

app.get('/times', function (req, res) {
    var date = req.query['date'];
    fs.readdir("./results/" + date, function (err, items) {

        items = items.filter(function (x) {
            return !x.startsWith(".") && !x.endsWith(".csv") && !x.endsWith(".lock")
        }).sort();

        items = items.reverse();

        res.send(items);
    });
});

console.log("Listening on http://127.0.0.1:3000");
app.listen(3000);
