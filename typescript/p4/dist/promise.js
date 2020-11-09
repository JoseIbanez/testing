"use strict";
const promise = new Promise((resolve, reject) => {
    reject(new Error("Something awful happened"));
});
promise.then((res) => {
    // This is never called
});
promise.catch((err) => {
    console.log('I get called:', err.message); // I get called: 'Something awful happened'
});
