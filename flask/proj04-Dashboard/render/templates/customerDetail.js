<script>
  setInterval(function() { queryCustKPI() }, 3000);


  function updateKPI(myCust, result) {
    ans=JSON.parse(result);
    var aLength = ans.length;
    for (var i = 0; i < aLength; i++) {
      $( "#"+ans[i].id).text(ans[i].value);
      if (ans[i].age>30){
        $( "#"+ans[i].id).addClass("text-muted");
      } else {
        $( "#"+ans[i].id).removeClass("text-muted");
      }
    }
  }

  function queryCustKPI() {
      url="/api/v1/byCust?cust="+custId;
      console.log(url)

      $.ajax({
            url: url,
            myCust: custId,
            success: function tmpUpdateKPI(result) {
                      updateKPI(this.myCust,result)
                    }
                 });

      }



  function queryKPI() {
    var arrayLength = vKPI.length;
    for (var i = 0; i < arrayLength; i++) {
        url="/api/v1/id?id="+vKPI[i].id;
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
