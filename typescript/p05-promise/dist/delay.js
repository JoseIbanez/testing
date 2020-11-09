"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.delay = void 0;
function AsyncDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function delay(ms) {
    await AsyncDelay(5000);
}
exports.delay = delay;
