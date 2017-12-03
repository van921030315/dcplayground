//    Chart.defaults.global.showTooltips = false;
//
//    var balanceState = [];
//    var btcState = [];
//    var ltcState = [];
//    var ethState = [];
//    var type = 'minute'
//
//    var balanceChart
//    var lineChart1;
//    var lineChart2;
//    var lineChart3 ;
//
//    var lineChart1_p;
//    var lineChart2_p;
//    var lineChart3_p;

//    $( "#next-week" ).click(function() {
//        $(document).ready(function(){
//              var request;
//              request = $.ajax({
//                type: 'POST',
//                url: "mocktrade/getpredictionprice",
//                data:
//                {
//                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//                    blockchain: 'all',
//                    currency: 'usd',
//                    rate: 'daily',
//                },
//                datatype: "json"
//              });
//
//              request.done(function(msg) {
//                displayPrediction("daily", msg)
//              });
//           });
//    });
//
//    $( "#next-hour" ).click(function() {
//        $(document).ready(function(){
//              var request;
//              request = $.ajax({
//                type: 'POST',
//                url: "mocktrade/getpredictionprice",
//                data:
//                {
//                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//                    blockchain: 'all',
//                    currency: 'usd',
//                    rate: 'hourly',
//                },
//                datatype: "json"
//              });
//
//              request.done(function(msg) {
//                displayPrediction("hourly", msg)
//              });
//           });
//    });
//
//
//    function displayPrediction(rate, predictions) {
//
//        $( "#text-prediction-btc" ).empty();
//        $( "#text-prediction-eth" ).empty();
//        $( "#text-prediction-ltc" ).empty();
//        $( "#prediction-type" ).empty();
//        if(predictions['BTC'][1]-predictions['BTC'][0] > 0){
//            $( "#caption-btc").attr("style", "color:yellowgreen");
//        }else{
//            $( "#caption-btc").attr("style", "color:coral");
//        }
//
//        if(predictions['LTC'][1]-predictions['LTC'][0] > 0){
//            $( "#caption-ltc").attr("style", "color:yellowgreen");
//        }else{
//            $( "#caption-ltc").attr("style", "color:coral");
//        }
//
//        if(predictions['ETH'][1]-predictions['ETH'][0] > 0){
//            $( "#caption-eth").attr("style", "color:yellowgreen");
//        }else{
//            $( "#caption-eth").attr("style", "color:coral");
//        }
//
//        displayPredictionChart(predictions['BTC'], predictions['ETH'], predictions['LTC']);
//
//        if(rate == "daily") {
//          $( "#prediction-type" ).append("<h3> 6-day Prediction </h3><hr>");
//          $( "#text-prediction-btc" ).append("<hr>");
//          $( "#text-prediction-btc" ).append("<p>Predictions:</p>");
//
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-btc" ).append("<p>" + (i+1) + " day from now:" + predictions['BTC'][i] + "</p>");
//              }else{
//              $( "#text-prediction-btc" ).append("<p>" + (i+1) + " days from now:" + predictions['BTC'][i] + "</p>");}
//          }
//
//
//          /*
//          $( "#text-prediction-btc" ).append("<hr><p>Conservative Predictions:</p>");
//          for(var i = 6; i < 12; i++){
//              if( i == 6){
//                $( "#text-prediction-btc" ).append("<p>" + (i+1-6) + " day from now:" + predictions['BTC'][i] + "</p>");
//              }else{
//                $( "#text-prediction-btc" ).append("<p>" + (i+1-6) + " days from now:" + predictions['BTC'][i] + "</p>");
//              }
//          }
//          */
//
//          $( "#text-prediction-eth" ).append("<hr>");
//          $( "#text-prediction-eth" ).append("<p>Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-eth" ).append("<p>" + (i+1) + " day from now:" + predictions['ETH'][i] + "</p>");
//              }else{
//              $( "#text-prediction-eth" ).append("<p>" + (i+1) + " days from now:" + predictions['ETH'][i] + "</p>");}
//          }
//
//          /*
//          $( "#text-prediction-eth" ).append("<hr><p>Conservative Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-eth" ).append("<p>" + (i+1) + " day from now:" + predictions['ETH'][i] + "</p>");
//              }else{
//              $( "#text-prediction-eth" ).append("<p>" + (i+1) + " days from now:" + predictions['ETH'][i] + "</p>");}
//          }
//          */
//
//          $( "#text-prediction-ltc" ).append("<hr>");
//          $( "#text-prediction-ltc" ).append("<p>Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " day from now:" + predictions['LTC'][i] + "</p>");
//              }else{
//              $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " days from now:" + predictions['LTC'][i] + "</p>");}
//          }
//
//          /*
//          $( "#text-prediction-ltc" ).append("<hr><p>Conservative Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " day from now:" + predictions['LTC'][i] + "</p>");
//              }else{
//              $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " days from now:" + predictions['LTC'][i] + "</p>");}
//          }  */
//
//          }else{
//              $( "#prediction-type" ).append("<h3> 6-hour Prediction </h3><hr>");
//          $( "#text-prediction-btc" ).append("<hr>");
//          $( "#text-prediction-btc" ).append("<p>Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-btc" ).append("<p>" + (i+1) + " hous from now:" + predictions['BTC'][i] + "</p>");
//              }else{
//              $( "#text-prediction-btc" ).append("<p>" + (i+1) + " hous from now:" + predictions['BTC'][i] + "</p>");}
//          }
//          /*
//          $( "#text-prediction-btc" ).append("<hr><p>Conservative Predictions:</p>");
//          for(var i = 6; i < 12; i++){
//              if( i == 6){
//                $( "#text-prediction-btc" ).append("<p>" + (i+1-6) + " hour from now:" + predictions['BTC'][i] + "</p>");
//              }else{
//                $( "#text-prediction-btc" ).append("<p>" + (i+1-6) + " hours from now:" + predictions['BTC'][i] + "</p>");
//              }
//          }
//          */
//          $( "#text-prediction-eth" ).append("<hr>");
//          $( "#text-prediction-eth" ).append("<p>Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-eth" ).append("<p>" + (i+1) + " hour from now:" + predictions['ETH'][i] + "</p>");
//              }else{
//              $( "#text-prediction-eth" ).append("<p>" + (i+1) + " hours from now:" + predictions['ETH'][i] + "</p>");}
//          }
//          /*
//          $( "#text-prediction-eth" ).append("<hr><p>Conservative Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-eth" ).append("<p>" + (i+1) + " hour from now:" + predictions['ETH'][i] + "</p>");
//              }else{
//              $( "#text-prediction-eth" ).append("<p>" + (i+1) + " hours from now:" + predictions['ETH'][i] + "</p>");}
//          }
//          */
//
//          $( "#text-prediction-ltc" ).append("<hr>");
//          $( "#text-prediction-ltc" ).append("<p>Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " hour from now:" + predictions['LTC'][i] + "</p>");
//              }else{
//              $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " hours from now:" + predictions['LTC'][i] + "</p>");}
//          }
//          /*
//          $( "#text-prediction-ltc" ).append("<hr><p>Conservative Predictions:</p>");
//          for(var i = 0; i < 6; i++){
//              if(i == 0 ){
//                $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " hour from now:" + predictions['LTC'][i] + "</p>");
//              }else{
//              $( "#text-prediction-ltc" ).append("<p>" + (i+1) + " hours from now:" + predictions['LTC'][i] + "</p>");}
//          }
//          */
//
//        }
//    }
//
//    function displayPredictionChart(btc, eth, ltc) {
//
//      //console.log("pred!")
//      var data_eth = {
//          labels: [0,1,2,3,4,5],
//          datasets: [
//              {
//                  label: "eth",
//                  fillColor: "rgba(0, 38, 77,0.2)",
//                  strokeColor: "rgba(0, 38, 77,1)",
//                  pointColor: "rgba(0, 38, 77,1)",
//                  pointStrokeColor: "#fff",
//                  pointHighlightFill: "#fff",
//                  pointHighlightStroke: "rgba(220,220,220,1)",
//                  pointRadius: 0,
//                  data: eth
//              },
//          ],
//
//
//      };
//
//
//      var data_ltc = {
//          labels: [0,1,2,3,4,5],
//          datasets: [
//              {
//                  label: "ltc",
//                  fillColor: "rgba(0, 77, 153,0.2)",
//                  strokeColor: "rgba(0, 77, 153,1)",
//                  pointColor: "rgba(0, 77, 153,1)",
//                  pointStrokeColor: "#fff",
//                  pointHighlightFill: "#fff",
//                  pointHighlightStroke: "rgba(220,220,220,1)",
//                  pointRadius: 0,
//                  data: ltc
//              },
//          ],
//
//
//      };
//
//       var data_btc = {
//          type:'line',
//          labels: [0,1,2,3,4,5],
//          datasets: [
//              {
//                  label: "btc",
//                  fillColor: "rgba(0, 115, 230,0.2)",
//                  strokeColor: "rgba(0, 115, 230,1)",
//                  pointColor: "rgba(0, 115, 230,1)",
//                  pointStrokeColor: "#fff",
//                  pointHighlightFill: "#fff",
//                  pointHighlightStroke: "rgba(220,220,220,1)",
//                  pointRadius: 0,
//                  data: btc
//              },
//          ],
//
//
//      };
//
//      var options = {
//        tooltips: {
//        enabled: 'true',
//        },
//        responsive: true,
//         };
//
//      var ctx_btc = document.getElementById("btcPredChart").getContext("2d");
//      var ctx_eth = document.getElementById("ethPredChart").getContext("2d");
//      var ctx_ltc = document.getElementById("ltcPredChart").getContext("2d");
//
//      if (lineChart1_p) {
//          lineChart1_p.destroy();
//      }
//      if (lineChart2_p) {
//          lineChart2_p.destroy();
//      }
//      if (lineChart3_p) {
//          lineChart3_p.destroy();
//      }
//
//      lineChart1_p = new Chart(ctx_btc).Line(data_btc, options);
//      lineChart2_p = new Chart(ctx_eth).Line(data_eth, options);
//      lineChart3_p = new Chart(ctx_ltc).Line(data_ltc, options);
//
//    }
//
//
//    $( "#current" ).click(function() {
//        type = 'minute';
//        $(document).ready(function(){
//           updateprice();
//        });
//    });
//
//    $( "#week" ).click(function() {
//        //console.log('view hourly data');
//        type = 'hour';
//        $(document).ready(function(){
//              var request;
//              request = $.ajax({
//                type: 'POST',
//                url: "mocktrade/gethistoryprice_week",
//                data:
//                {
//                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//                    blockchain: 'all',
//                    currency: 'usd',
//                    rate: 'hour',
//                },
//                datatype: "json"
//              });
//
//              request.done(function(msg) {
//                //console.log("ok got old prices in the past week");
//                btcState = msg['BTC'];
//                ltcState = msg['LTC'];
//                ethState = msg['ETH'];
//                //console.log(btcState);
//                balanceState = msg['BAL'];
//                var update = 0;
//                displayBalanceHistChart(balance, btcState, ltcState, ethState);
//              });
//           });
//
//    });
//
//    $( "#month" ).click(function() {
//        type = 'month';
//        $(document).ready(function(){
//              var request;
//              request = $.ajax({
//                type: 'POST',
//                url: "mocktrade/gethistoryprice_week",
//                data:
//                {
//                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//                    blockchain: 'all',
//                    currency: 'usd',
//                    rate: 'day',
//                },
//                datatype: "json"
//              });
//
//              request.done(function(msg) {
//                //console.log("ok got old prices in the past month");
//                btcState = msg['BTC'];
//                ltcState = msg['LTC'];
//                ethState = msg['ETH'];
//                balanceState = msg['BAL'];
//                var update = 0;
//                displayBalanceHistChart(balance, btcState, ltcState, ethState);
//              });
//           });
//
//    });





//    function displayBalanceChart(balance, btc, eth, ltc, update) {
//
//    if (update == 1){
//      if (balanceState.length >= 10){
//          balanceState.shift();
//      }
//      balanceState.push(balance);
//      if (btcState.length >= 10){
//          btcState.shift();
//      }
//      btcState.push(btc);
//      if (ltcState.length >= 10){
//          ltcState.shift();
//      }
//      ltcState.push(ltc);
//      if (ethState.length >= 10){
//          ethState.shift();
//      }
//      ethState.push(eth);
//    }
//
//    if(type == 'minute'){
//    var data_balance = {
//        labels: [-270+'s', -240+'s', -210+'s', -180+'s', -150+'s', -120+'s', -90+'s', -60+'s', -30+'s', 00+'s'],
//        datasets: [
//            {
//                label: "Balance",
//                fillColor: "rgba(220,220,220,0.2)",
//                strokeColor: "rgba(220,220,220,1)",
//                pointColor: "rgba(220,220,220,1)",
//                pointStrokeColor: "#fff",
//                pointHighlightFill: "#fff",
//                pointHighlightStroke: "rgba(220,220,220,1)",
//                data: balanceState
//            }
//        ]
//    };
//
//    var data_btc = {
//        labels: [-270+'s', -240+'s', -210+'s', -180+'s', -150+'s', -120+'s', -90+'s', -60+'s', -30+'s', 00+'s'],
//        datasets: [
//            {
//                label: "Balance",
//                fillColor: "rgba(0, 115, 230,0.2)",
//                strokeColor: "rgba(0, 115, 230,1)",
//                pointColor: "rgba(0, 115, 230,1)",
//                pointStrokeColor: "#fff",
//                pointHighlightFill: "#fff",
//                pointHighlightStroke: "rgba(0, 115, 230,1)",
//                data: btcState
//            }
//        ]
//    };
//
//    var data_ltc = {
//        labels: [-270+'s', -240+'s', -210+'s', -180+'s', -150+'s', -120+'s', -90+'s', -60+'s', -30+'s', 00+'s'],
//        datasets: [
//            {
//                label: "Balance",
//                illColor: "rgba(0, 38, 77,0.2)",
//                strokeColor: "rgba(0, 38, 77,1)",
//                pointColor: "rgba(0, 38, 77,1)",
//                pointStrokeColor: "#fff",
//                pointHighlightFill: "#fff",
//                pointHighlightStroke: "rgba(0, 38, 77,1)",
//                data: ltcState
//            }
//        ]
//    };
//
//    var data_eth = {
//        labels:[-270+'s', -240+'s', -210+'s', -180+'s', -150+'s', -120+'s', -90+'s', -60+'s', -30+'s', 00+'s'],
//        datasets: [
//            {
//                label: "Balance",
//                fillColor: "rgba(0, 77, 153,0.2)",
//                strokeColor: "rgba(0, 77, 153,1)",
//                pointColor: "rgba(0, 77, 153,1)",
//                pointStrokeColor: "#fff",
//                pointHighlightFill: "#fff",
//                pointHighlightStroke: "rgba(0, 77, 153,1)",
//                data: ethState
//            }
//        ]
//    };
//
//    var ctx_balance = document.getElementById("balanceChart").getContext("2d");
//    var ctx_btc = document.getElementById("btcChart").getContext("2d");
//    var ctx_ltc = document.getElementById("ltcChart").getContext("2d");
//    var ctx_eth = document.getElementById("ethChart").getContext("2d");
//
//    var options = {
//      tooltips: {
//				enabled: true,
//				},
//      responsive: true,
//       };
//
//
//    if (balanceChart) {
//        balanceChart.destroy();
//      }
//      if (lineChart1) {
//        lineChart1.destroy();
//      }
//      if (lineChart2){
//        lineChart2.destroy();
//      }
//      if (lineChart3) {
//        lineChart3.destroy();
//      }
//
//
//    balanceChart = new Chart(ctx_balance).Line(data_balance, options);
//    lineChart1 = new Chart(ctx_ltc).Line(data_ltc, options);
//    lineChart2 = new Chart(ctx_btc).Line(data_btc, options);
//    lineChart3 = new Chart(ctx_eth).Line(data_eth, options);
//
//    }
//  }

//    updateprice();
//
//    setInterval(function(){
//        updateprice()
//    }, 30000);
