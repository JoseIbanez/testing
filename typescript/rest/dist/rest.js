var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { HttpClient } from './httpClient';
const httpClient = new HttpClient();
function fetchItems() {
    return __awaiter(this, void 0, void 0, function* () {
        // prepare our request parameters
        const parameters = {
            url: 'https://jsonplaceholder.typicode.com/todos',
            requiresToken: false
        };
        // just return httpClient.get (which is a promise) or again use async/await if you prefer
        return httpClient.get(parameters);
    });
}
const data = fetchItems();
data.then((res) => {
    console.log("ok");
    console.log(res[0]);
});
