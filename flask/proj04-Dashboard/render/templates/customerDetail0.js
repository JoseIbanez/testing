<script>
  onload=function() { queryGraph() };
  setInterval(function() { queryKPI() }, 3000);


  function updateKPI(myKPI, result) {
            ans=JSON.parse(result);
            $( "#"+myKPI ).text(ans.value);
  }

  function queryKPI() {
    var arrayLength = vKPI.length;
    for (var i = 0; i < arrayLength; i++) {
        url="/api/v1/kpi?cust="+vKPI[i].cust+"&kpi="+vKPI[i].kpi+"&domain="+vKPI[i].domain;
        console.log(url)

        $.ajax({
          url: url,
          myKPI: vKPI[i].id,
          success: function tmpUpdateKPI(result) {
                      updateKPI(this.myKPI,result)
                   }
        });

    }

  }




  function updateGraph(myKPI, result) {
            ans=JSON.parse(result);
            myG[myKPI.toString()].setData(ans);
  }


  function queryGraph() {
    var arrayLength = gKPI.length;
    for (var i = 0; i < arrayLength; i++) {
        url="/api/v1/log?cust="+gKPI[i].cust+"&kpi="+gKPI[i].kpi+"&domain="+gKPI[i].domain;
        console.log(url)

        $.ajax({
          url: url,
          myKPI: gKPI[i].id,
          success: function tmpUpdateKPI(result) {
                      updateGraph(this.myKPI,result)
                   }
        });

    }

  }

</script>
