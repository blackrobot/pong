;(function($) {
  var selector = '.sparkline';
  var data_key = 'record';
  var config = {
    'type': 'tristate',
    'disableInteraction': true,
    'disableTooltips': true,
    'disableHighlight': true,
    'barWidth': 6,
    'barSpacing': 2,
    'posBarColor': 'rgba(70, 136, 71, 0.75)',
    'negBarColor': 'rgba(185, 74, 72, 0.75)'
  };

  function init() {
    var $el;
    var $sparklines = $(selector);

    $sparklines.each(function(i, e) {
      $el = $(this);
      $el.sparkline($el.data(data_key), config);
    });
  }

  $(init);
}(jQuery));
