const express = require('express');
var blogController = require('../controllers/blog.server.controller');



module.exports = function(app) {
    app.use(express.json());

    var baseUrl = '/api/';
    var currentVersion = 'v1/';
    var url = baseUrl+currentVersion;


    app.get(url + 'blogs/', blogController.list);

    app.get(url + 'blogs/:id/', blogController.get)

    app.post(url + 'blogs/', blogController.create);

    app.put(url + 'blogs/:id/', blogController.update);

    app.delete(url + 'blogs/:id/', blogController.delete);


};