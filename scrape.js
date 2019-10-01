games = [];
$.each($('#sortList').children(), function(i, x) {
  x = $(x);
  games.push({
    "id": x.attr('id'),
    "pgn": x.data('pgn')
  });
});
console.log(JSON.stringify(games));
