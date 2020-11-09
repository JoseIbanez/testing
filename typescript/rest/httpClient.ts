import axios, { AxiosRequestConfig, AxiosError, AxiosResponse } from "axios";

export interface IHttpClient {
    get<T>(parameters: IHttpClientRequestParameters<T>): Promise<T>
    post<T>(parameters: IHttpClientRequestParameters<T>): Promise<T>
}

export interface IHttpClientRequestParameters<T> {
    url: string
    requiresToken: boolean
    payload?: T
}


export class HttpClient implements IHttpClient {

  get<Q,R>(parameters: IHttpClientRequestParameters<Q>): Promise<R> {
    return new Promise<R>((resolve, reject) => {
      // extract the individual parameters
      const { url, requiresToken } = parameters 
  
      // axios request options like headers etc
      const options: AxiosRequestConfig = {
        headers: {}
      }
  
  
      // finally execute the GET request with axios:
      axios
        .get(url, options)
        .then((response: any) => {
          resolve(response.data as R)
        })
        .catch((response: any) => {
          reject(response)
        })
  
    })
  }


  post<T>(parameters: IHttpClientRequestParameters<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      const { url, payload, requiresToken } = parameters
  
      // axios request options like headers etc
      const options: AxiosRequestConfig = {
        headers: {}
      }
    
      // finally execute the GET request with axios:
      axios
        .post(url, payload, options)
        .then((response: any) => {
          resolve(response.data as T)
        })
        .catch((response: any) => {
          reject(response)
        })
    })
  }


}

