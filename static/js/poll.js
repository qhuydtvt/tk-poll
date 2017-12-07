$(document).ready(function() {
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
});
