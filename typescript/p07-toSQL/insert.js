

list = [
    {"c1":11, "c2": "1-two", "c3":true},
    {"c1":21, "c2": "2-two", "c3":false},
    {"c1":31, "c2": "3-two", "c3":true},
]


bulkJsonInsert("demo_tmp","c1",list);


function bulkJsonInsert(table,key,list) {

    valueList = [];


    colNames = Object.keys(list[0]);

    console.log(colNames);

    for (idx in list) {
        item = list[idx];
        console.log(item);
        values = colNames.map( function (col) {
            return item[col];
        }); 
        console.log(values);

        valueList.push("('"+values.join("','")+"')");

    }

    console.log(valueList);

    query = "INSERT into "+table+" \n"
                + "("+colNames.join(',')+") \n"
                + "VALUES \n"
                + valueList.join(",\n") + ";"


    console.log(query);


}