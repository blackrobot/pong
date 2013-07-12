;(function($) {
  function submitForm(event) {
    var $button = $(this);
    var $form = $button.parent();

    $form.find('button').attr('disabled', true);
    $form.find('input[name="confirmed"]').val($button.data('confirm'));
    $form.submit();
  }

  function init() {
    var $forms = $('.confirmation-form');
    $forms.find('button').click(submitForm);
  }

  $(init);
}(jQuery));
