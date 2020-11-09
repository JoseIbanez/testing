import axios from "axios";
export class HttpClient {
    get(parameters) {
        return new Promise((resolve, reject) => {
            // extract the individual parameters
            const { url, requiresToken } = parameters;
            // axios request options like headers etc
            const options = {
                headers: {}
            };
            // finally execute the GET request with axios:
            axios
                .get(url, options)
                .then((response) => {
                resolve(response.data);
            })
                .catch((response) => {
                reject(response);
            });
        });
    }
    post(parameters) {
        return new Promise((resolve, reject) => {
            const { url, payload, requiresToken } = parameters;
            // axios request options like headers etc
            const options = {
                headers: {}
            };
            // finally execute the GET request with axios:
            axios
                .post(url, payload, options)
                .then((response) => {
                resolve(response.data);
            })
                .catch((response) => {
                reject(response);
            });
        });
    }
}
