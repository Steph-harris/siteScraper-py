$(document).ready(function(){
    preloader("#Standings");

    get_standings();
});

  function get_standings(){
    $.ajax({
      method: "GET",
      url: "/standings",
      dataType: "json",
    }).done(function(dt){
      dt = JSON.parse(dt)
      console.table(dt);

      buildStandings(dt)
    });
  }

  function buildStandings(dt){
    var stDt = dt.standings_date;
    var teamsLn = dt.standing.length;
    var teams = dt.standing;
    var newRws;
    var i =0;
    var stStr = "(Standings as of " + stDt.substr(5, 5) + ")";
    var newTb = `<table id='Standings_Tbl'><thead>
    <th>Team</th>
    <th>W</th>
    <th>L</th>
    <th>G.B.</th>
    <th>Last 10</th>
    <th>Streak</th>
    </thead></table>`;

    _.forEach(teams, function(val){
      switch(val.division){
        case "E":
          var division = "East"
          break;
        case "W":
          var division = "West"
          break;
        case "C":
          var division = "Central"
          break;
      }

      if(i%5 == 0){
        newRws += `<tr><td class="div_header" title="${val.conference} ${division} Division Standings"><b>${val.conference} ${division}</b></td>
        
        </tr>`;
      }
      newRws += `<tr title="${val.first_name} ${val.last_name } Standing"><
      <td>${val.first_name} ${val.last_name }</td>
      <td>${val.won}</td>
      <td>${val.lost}</td>
      <td>${val.games_back}</td>
      <td>${val.last_ten}</td>
      <td>${val.streak}</td>
      </tr>`;
      i++;
    });

    $("#Standings").attr("title", stStr);
    $("#Standings").append(newTb);
    $("#Standings_Tbl").append(newRws);
    removePreloader("#Standings");
}

//adjust length for standings
//add more detailed league
