var final_pick = 0;
function poll_init(final_pick_) {
  final_pick = final_pick_;
}

$(document).ready(function(){
  $('.choice .up').click(function(event) {
    var choice = $(event.target).closest('.choice');
    var choice_before = $(choice).prev();
    choice_before.insertAfter(choice);
  });

  $('.choice .down').click(function(event){
    var choice = $(event.target).closest('.choice');
    var choice_after = $(choice).next();
    choice_after.insertBefore(choice);
  });

  $('#poll_form').submit(function(event){
    event.preventDefault();
    $('#poll_form .choice-id').remove();
    var selectedChoiceArr = [];
    var choiceEls = $('.choice span');
    for(var i = 0; i < final_pick; i++) {
      var selectedChoice = $(choiceEls[i]).attr('id');
      var inputVote = $(`
        <input class="d-none" name="${selectedChoice}" value="${final_pick - i}"></input>
        `);
      $("#poll_form").append(inputVote);
    }
    this.submit();
  });
});
