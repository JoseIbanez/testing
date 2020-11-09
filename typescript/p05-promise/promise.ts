import fetch from 'node-fetch';


const promise = new Promise((resolve, reject) => {
    //reject(new Error("Something awful happened"));
    resolve("ee");
})
.then((res) => {
  console.log('1st OK:',res);    
})
.catch((err) => {
    console.log("1st catch:", err.message);
});



console.log('last line');
//let result = await Promise.resolve('this is a sample promise');



console.log('after timeout');

function delay(ms: number) {
  return new Promise( resolve => setTimeout(resolve, ms) );
}

export async function http(
    request: string
  ): Promise<any> {
    const response = await fetch(request);
    console.log("fetch ok");
    const body = await response.json();
    console.log("json ok");
    await delay(1000);
    console.log("delay ok");
    return body;
  }
  
// example consuming code
const data = http(
    "https://jsonplaceholder.typicode.com/todos"
  );

data.then((res) => {
  console.log(res[1]);

});