
import * as Mustache from 'mustache';
import { Employee } from "../src/Employee";


interface Link {
  url: string;
  name: string;
}

function filterByTerm(input: Array<Link>, searchTerm: string) {
    if (!searchTerm) throw Error("searchTerm cannot be empty");
    if (!input.length) throw Error("inputArr cannot be empty");
    const regex = new RegExp(searchTerm, "i");
    return input.filter(function(arrayElement) {
      return arrayElement.url.match(regex);
    });
  }
  
var result = filterByTerm([ {"url":"input string", "name":"i"}, 
                            {"url":"input java", "name": "java"} ], 
                            "java");

console.log(result);

/////////////


var view = {
  title: "Joe",
  calc: function () {
    return 2 + 4;
  }
};

var output = Mustache.render("{{title}} spends {{calc}}", view);
console.log(output);


/////////////

let empObj = new Employee("Steve Jobs", 1);
empObj.displayEmployee();

empObj.empName="Peter P."
empObj.displayEmployee();

