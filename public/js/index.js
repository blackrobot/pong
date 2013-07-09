;(function($) {
  var config = {
    'type': 'tristate',
    'disableInteraction': true,
    'disableTooltips': true,
    'disableHighlight': true,
    'barWidth': 6,
    'barSpacing': 2,
    'posBarColor': 'rgba(70, 136, 71, 0.8)',
    'negBarColor': 'rgba(185, 74, 72, 0.8)'
  };

  function init() {
    $('.sparkline').each(function(i, e) {
      var $el = $(this);
      $el.sparkline($el.data('record'), config);
    });
  }

  $(init);
}(jQuery));
