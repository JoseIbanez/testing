import { HttpClient, IHttpClientRequestParameters } from './httpClient';


const httpClient = new HttpClient()


export interface IItem {
  userId: number
  id: number
  title: string
  completed2: boolean
}

async function fetchItems(): Promise<IItem[]> {
    // prepare our request parameters
    const parameters: IHttpClientRequestParameters<IItem> = {
      url: 'https://jsonplaceholder.typicode.com/todos',
      requiresToken: false
    }
  
    // just return httpClient.get (which is a promise) or again use async/await if you prefer
    return httpClient.get<IItem,IItem[]>(parameters)
  }
 
const data = fetchItems();
data.then((res) => {
  console.log("ok");
  console.log(res[0]);
});
