const express = require('express');
const { HLTV } = require('hltv');
const app = express();

app.get('/matches', function(req, res) {
  HLTV.getMatches().then((matches) => {
    res.send(matches);
  });
});

app.get('/matches/:matchId', function(req, res) {
  HLTV.getMatch({ id: req.params.matchId }).then((match) => {
    res.send(match);
  });
});

app.get('/stats/matches', function(req, res) {
  HLTV.getMatchesStats({ startDate: 2019-01-01, endDate: new Date().toISOString().slice(0,10) }).then((matches_stats) => {
    res.send(matches_stats);
  });
});

app.get('/stats/matches/:matchId', function(req, res) {
  HLTV.getMatchMapStats({ id: req.params.matchId }).then((match_stats) => {
    res.send(match_stats);
  });
});

app.get('/results', function(req, res) {
  HLTV.getResults({ pages: 1 }).then((results) => {
    res.send(results);
  });
});

app.get('/results/detailed', function (req, res) {
  
  HLTV.getMatchesStats({ startDate: 2019-01-01, endDate: new Date().toISOString().slice(0,10) }).then(async (matches_stats) => {
    const promises = [];
    matches_stats.forEach((current_match) => {
      promises.push(HLTV.getMatchMapStats({ id: current_match.id }));
    });
    const resolvedPromises = await Promise.all(promises);
    res.send(resolvedPromises);
  });
  
});

app.listen(3000, function() {
  console.log('Listening on port 3000...');
});