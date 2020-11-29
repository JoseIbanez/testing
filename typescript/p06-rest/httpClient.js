"use strict";
exports.__esModule = true;
exports.HttpClient = void 0;
var axios_1 = require("axios");
var HttpClient = /** @class */ (function () {
    function HttpClient() {
    }
    // ... implementation code will go here
    HttpClient.prototype.get = function (parameters) {
        var _this = this;
        return new Promise(function (resolve, reject) {
            // extract the individual parameters
            var url = parameters.url, requiresToken = parameters.requiresToken;
            // axios request options like headers etc
            var options = {
                headers: {}
            };
            // if API endpoint requires a token, we'll need to add a way to add this.
            if (requiresToken) {
                var token = _this.getToken();
                options.headers.RequestVerificationToken = token;
            }
            // finally execute the GET request with axios:
            axios_1["default"]
                .get(url, options)
                .then(function (response) {
                resolve(response.data);
            })["catch"](function (response) {
                reject(response);
            });
        });
    };
    HttpClient.prototype.post = function (parameters) {
        var _this = this;
        return new Promise(function (resolve, reject) {
            var url = parameters.url, payload = parameters.payload, requiresToken = parameters.requiresToken;
            // axios request options like headers etc
            var options = {
                headers: {}
            };
            // if API endpoint requires a token, we'll need to add a way to add this.
            if (requiresToken) {
                var token = _this.getToken();
                options.headers.RequestVerificationToken = token;
            }
            // finally execute the GET request with axios:
            axios_1["default"]
                .post(url, payload, options)
                .then(function (response) {
                resolve(response.data);
            })["catch"](function (response) {
                reject(response);
            });
        });
    };
    return HttpClient;
}());
exports.HttpClient = HttpClient;
