var io = io();
$(document).ready(function (){
  io.on(poll_code, function(data){
    console.log(data);
    var votes_count = data.votes_count;
    $('#votes_count').text(votes_count);
  });
});
