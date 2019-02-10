System = require('console')

var Mustache = require('mustache');


var view = [
    {title: "Mr", name: "Jose"},
    {title: "Mr", name: "John"},
    {title: "Mrs", name: "Srar", last:true}
];

tpl = `{
    {{name}}
    {{#.}}
    {
     name:  "{{name}}",
     title: "{{title}}"
    }{{^last}},{{/last}}
    {{/.}}
}`;

//tpl = JSON.stringify(template);
  
//var output = Mustache.render(tpl, view, '-', ["<<", ">>"]);
var output = Mustache.render(tpl, view);

System.log(output);

