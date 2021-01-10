games = [];
$.each($('#variations').children(), function(i, x) {
  x = $(x);
  games.push({
    "id": x.attr('id'),
    "pgn": x.data('pgn')
  });
});
console.log(JSON.stringify(games));






games = [];
$.each($('#variations').children(), function(i, x) {
  x = $(x);
  games.push({
    "id": x.attr('id'),
    "pgn": x.find(".variation-card__moves").text()
  });
});
console.log(JSON.stringify(games));


