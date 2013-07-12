;(function($) {
  var $messages;

  function submitForm(event) {
    var $button = $(this);
    var $form = $button.parent();

    $form.find('button').attr('disabled', true);
    $form.find('input[name="confirmed"]').val($button.data('confirm'));

    $.post($form.attr('action'), $form.serialize(), function(data, t, j) {
      $messages.append(data);
      $form.parents('tr').addClass('muted');
    }, 'html');
  }

  function init() {
    var $forms = $('.confirmation-form');
    $messages = $('#messages');
    $forms.find('button').click(submitForm);
  }

  $(init);
}(jQuery));
