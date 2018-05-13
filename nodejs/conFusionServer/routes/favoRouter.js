const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const Favorites = require('../models/favorite');

const favoRouter = express.Router();

var authenticate = require('../authenticate');

favoRouter.use(bodyParser.json());

favoRouter.route('/')
.get((req,res,next) => {
    Dishes.find({})
    .populate('comments.author')
    .then((dishes) => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.json(dishes);
    }, (err) => next(err))
    .catch((err) => next(err));
})
.post(authenticate.verifyUser, (req, res, next) => {
    Dishes.create(req.body)
    .then((dish) => {
        console.log('Dish Created ', dish);
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.json(dish);
    }, (err) => next(err))
    .catch((err) => next(err));
})
.put(authenticate.verifyUser, (req, res, next) => {
    res.statusCode = 403;
    res.end('PUT operation not supported on /favorites');
})
.delete(authenticate.verifyUser, (req, res, next) => {
    Favorites.remove({})
    .then((resp) => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.json(resp);
    }, (err) => next(err))
    .catch((err) => next(err));    
});



favoRouter.route('/:favoriteId')
.get((req,res,next) => {
    res.statusCode = 403;
    res.end('GET operation not supported on /favorites/'+ req.params.favoriteId);
})
.post(authenticate.verifyUser, (req, res, next) => {
    console.log("Current User ID: " + req.user._id);
    Favorites.findOne({user: profile.id})
    .then((favorites) => {
        if (favorites == null) {
            favorites = new Favorites({ user: profile.id });
        }
        if (!favorites.dishes.indexOf(favoriteId)) {
            favorites.dishes.push(favoriteId);
            favorites.save()
            .then((favorites) => {
                res.statusCode = 200;
                res.setHeader('Content-Type', 'application/json');
                res.json(favorites);
            }, (err) => next(err));
        }
    }, (err => next(err)))
    .catch((err) => next(err));
})
.put(authenticate.verifyUser, (req, res, next) => {
    res.statusCode = 403;
    res.end('GET operation not supported on /favorites/'+ req.params.favoriteId);
})
.delete(authenticate.verifyUser, (req, res, next) => {
    Favorites.findOne({user: profile.id})
    .then((favorites) => {
        if (favorites == null) {
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            res.json(favorites);
        }
        if (!favorites.dishes.indexOf(favoriteId)) {
            favorites.dishes.pop(favoriteId);
            favorites.save()
            .then((favorites) => {
                res.statusCode = 200;
                res.setHeader('Content-Type', 'application/json');
                res.json(favorites);
            }, (err) => next(err));
        }
    }, (err => next(err)))
    .catch((err) => next(err));
})


module.exports = favoRouter;