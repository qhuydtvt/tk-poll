var currentChoiceIndex = 0;

$(document).ready(function(){
  $('#btn_add_choice').click(function(event) {
    var input = $(event.target).siblings('input');
    addNewChoice(input.val());
    input.val('');
  });

  $('#input_new_choice').on('keydown', function(event){
    if (event.keyCode == 13) {
      event.preventDefault();
      var input = $(event.target);
      addNewChoice(input.val());
      input.val('');
      return false;
    }
  });

  updateCreateButton();
});

function addNewChoice(choice) {
  var newChoice = $(`
    <div class="choice-wrapper">
      <input class="input-choice" type="text" name="choice_${currentChoiceIndex++}" value="${choice}">
      <i class="fa fa-minus text-red choice-action pointer btn-remmove-choice" aria-hidden="true"></i>
    </div>
  `);

  newChoice.insertBefore('.choice-wrapper:last');

  $('.btn-remmove-choice').click(function(event){
    $(event.target).parent().remove();
    updateCreateButton();
  });

  $('.input-choice:last').focus();

  updateCreateButton();
}

function updateCreateButton() {
  if ($('.choice-wrapper').length > 2) {
    $('#btn-create-poll').show();
  } else {
    $('#btn-create-poll').hide();
  }
}
