var muted = true;
if (!muted) {
    setTimeout(function() {
      var sound = new Audio('/static/sounds/victory.mp3');
      sound.play();
    }, 0);
}

$(".draggable" ).draggable({
  revert: 'invalid',
  cursor: "pointer"
});

$(".droppable").droppable({
  drop: function(event, ui) {
    var span = ui.draggable;
    var connectedId = span[0].id;
    var votePointClass = connectedId.replace('voter-name', 'vote-point');
    var name = span.html();

    var newSpan = $(`
      <div class="team-member" connected_id="${connectedId}">
        <span>${name}</span>
        <i class="fa fa-times" aria-hidden="true"></i>
      </div>
      `).appendTo($(this).find('.team-container'));

    $(`.${votePointClass}`).removeClass('fade-in').addClass('fade-out')
    ui.draggable.css("position", "").css("left", "").css("top", "");
    ui.draggable.hide();

    newSpan.find("i").click(function() {
      ui.draggable.show();
      newSpan.remove();
      $(`.${votePointClass}`).removeClass('fade-out').css("opacity", 1);
    });
  }
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
  $('#btn_select_team').hide();
}
