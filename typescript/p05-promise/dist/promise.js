"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.http = void 0;
const promise = new Promise((resolve, reject) => {
    reject(new Error("Something awful happened"));
    //resolve("ee");
});
promise.then((res) => {
    // This is never called
    console.log('OK:', res);
});
promise.catch((err) => {
    console.log('I get called:', err.message); // I get called: 'Something awful happened'
});
console.log('last line');
//let result = await Promise.resolve('this is a sample promise');
console.log('after timeout');
async function http(request) {
    const response = await fetch(request);
    const body = await response.json();
    return body;
}
exports.http = http;
// example consuming code
const data = http("https://jsonplaceholder.typicode.com/todos");
