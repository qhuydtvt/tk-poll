var currentChoiceIndex = 0;

$(document).ready(function(){
  $('#btn_add_choice').click(function(event) {
    var input = $(event.target).siblings('input');
    addNewChoice(input.val());
    input.val('');
  });

  $('#input_new_choice').on('keyup', function(event){
    if (event.keyCode == 13) {
      var input = $(event.target);
      addNewChoice(input.val());
      input.val('');
    }
  });
});

function addNewChoice(choice) {
  $("#choice_list").append(`
    <li class="item-choice">
      <input class="input-choice" type="text" name="choice_${currentChoiceIndex++}" value="${choice}">
      <span class="text-red choice-action">
        <i class="fa fa-minus pointer" aria-hidden="true"></i>
      </span>
    </li>
  `);
}
