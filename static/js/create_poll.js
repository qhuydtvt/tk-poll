var currentChoiceCount = 1;

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

  $('#sel_final_pick_count').change(function(event) {
    var selectedIndex = event.target.selectedIndex;
    var options = event.target.options;
    var selectedOption = options[selectedIndex];
    updatePickCountInput(selectedOption.text);
  });

  $('#btn_create_poll').click(function(event){
    if($('#sel_final_pick_count')[0].selectedIndex == 0) {
      console.log("ABC");
      event.preventDefault();
      alert("You forgot to select final pick");
      return false;
    }
  });

  updateCreateWrapper();
  updateFinalPick();
});

function addNewChoice(choice) {
  if (!choice) {
    return;
  }
  var newChoice = $(`
    <div class="choice-wrapper">
      <input class="input-choice input-empty-clear" type="text" name="choice_${currentChoiceCount++}" value="${choice}">
      <i class="fa fa-times text-red choice-action pointer btn-remmove-choice" aria-hidden="true"></i>
    </div>
  `);

  newChoice.insertBefore('.choice-wrapper:last');

  $('.btn-remmove-choice').click(function(event){
    $(event.target).parent().remove();
    updateCreateWrapper();
    updateFinalPick();
  });

  $('.input-empty-clear').focusout(function(event){
    var input = $(event.target);
    if (input.val() == "") {
      input.parent().remove();
      updateCreateWrapper();
      updateFinalPick();
    }
  });

  $('.input-choice:last').focus();

  updateCreateWrapper();
  updateFinalPick();
}

function updateCreateWrapper() {
  if ($('.choice-wrapper').length > 2) {
    $('#poll-create-wrapper').show();
  } else {
    $('#poll-create-wrapper').hide();
  }
}

function updateFinalPick() {
  $('#sel_final_pick_count').empty();
  $('#sel_final_pick_count').append($("<option>-- Final pick --</option>"));
  for(var selection = 1; selection < currentChoiceCount - 1; selection++) {
    $('#sel_final_pick_count').append(`<option>${selection}</option>`);
  }
}

function updatePickCountInput(selectedValue) {
  if (/^\d+$/.test(selectedValue)) {
    $('#input_final_pick_count').attr('value', selectedValue);
  }
}
