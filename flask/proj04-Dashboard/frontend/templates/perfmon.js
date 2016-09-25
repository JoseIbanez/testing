<script>
  var i = 0;
  setInterval(function() { query() }, 3000);

  function query() {
    $.ajax({
      url: "/list?cust=Cust16&kpi=RegisteredPhones&domain=%2FUK",
      success: function updatePage(result) {
        console.log(result);
        ans=JSON.parse(result);
        console.log(ans.length);
  
        for (index = 0; index < ans.length; ++index) {
          console.log(ans[index]);
	  wi=ans[index].value/50


	  $( "#"+ans[index].id ).text(ans[index].value)
          $( "#"+ans[index].id ).width( wi + "%")

        }

        }
    });
  }


</script>

