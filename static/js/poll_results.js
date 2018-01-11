var muted = true;
if (!muted) {
    setTimeout(function() {
      var sound = new Audio('/static/sounds/victory.mp3');
      sound.play();
    }, 0);
}

$(".draggable" ).draggable({
  revert: true,
  cursor: "pointer"
});

$(document).ready(function() {
  $('#btn_select_team').click(function(event) {
    hideAllResultBar();
  });

  $('.choice-result-value').click(function(event){
    var view = event.target;
    $(view).closest('.choice-result').addClass('height-shrink');
  });
});

function hideAllResultBar() {
  $('.choice-result-tray').addClass('shrink');

  $('.voter-name').addClass('fade-in');
  $('.vote-point').addClass('fade-in');
  $('.team-list').addClass('show');
}
