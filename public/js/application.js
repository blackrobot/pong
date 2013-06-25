;(function($) {
  var $range, $games_won, $games_lost;

  function rangeUpdate() {
    var val = $range.val();

    $games_won.val(val);
    $games_lost.val(3 - val);
  }

  function setupRange() {
    $range = $('.match-range');

    if ($range.length <= 0) { return; }

    $games_won = $('#id_games_won');
    $games_lost = $('#id_games_lost');

    $range.noUiSlider({
      range: [0, 3],
      start: 0,
      handles: 1,
      step: 1,
      orientation: 'vertical',
      slide: rangeUpdate
    });
  }

  function init() {
    setupRange();
  }

  $(init);
}(jQuery));
