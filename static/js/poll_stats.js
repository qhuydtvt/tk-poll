var io = io();
$(document).ready(function (){
  io.on(poll_code, function(data){
    var votes_count = data.votes_count;
    $('#votes_count').text(votes_count);
    showHideResultButton(votes_count > 0);
  });
});

function showHideResultButton(show) {
  if (show) {
    $("#btn_results").show();
  } else {
    $("#btn_results").hide();
  }
}
