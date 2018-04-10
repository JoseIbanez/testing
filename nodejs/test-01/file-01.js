

// https://www.ibm.com/developerworks/ssa/opensource/library/os-nodejs/

var http = require("http");
var url = require("url");


var myServer = function(request, response) {
 
     response.writeHead(200, {"Content-Type": "text/plain"});
 
     var params = url.parse(request.url, true).query;
     var input = params.number;
 
     var numInput = new Number(input);
     var numOutput = new Number(Math.random() * numInput).toFixed(0);
      
     response.write("Input " + numInput + "\n");
     response.write("Output " + numOutput + "\n");
     console.log("Out " + numOutput)

     
     response.end();
}



//a = myServer( myRequest, myResponse)

http.createServer(myServer).listen(80);
 
console.log("Random Number Generator Running...");

