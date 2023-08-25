const express = require('express');
const app = express();
const Pool = require('pg').Pool;
  
const pool = new Pool({

    user: 'postgres',
    host: 'localhost',
    database: 'vindelstats',
    password: '1190400237986',
    dialect: 'postgres',
    port: 5432
});
  
const bodyParser = require('body-parser');
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }));
  
app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});
  
pool.connect((err, client, release) => {
    if (err) {
        return console.error(
            'Error acquiring client', err.stack)
    }
    client.query('SELECT NOW()', (err, result) => {
        release()
        if (err) {
            return console.error(
                'Error executing query', err.stack)
        }
        console.log("Connected to Database !")
    })
})
  
app.get('/player/:player', (req, res, next) => {
    player = req.params.player
    pool.query('select * from players inner join stats_season_player s on players.playerid = s.playerid where players.playerid = $1',[player])
          .then(Data1 => {
            res.send(Data1.rows);
    })
})

app.get('/:league/stats', (req, res, next) => {
    league = req.params.league
    league = translateLeague(league)

    console.log('entraaqui' + league)
    seasonid = 2
    pool.query('select * from stats_season_player where league = $1 and seasonid = $2 order by name',[league,seasonid])
          .then(Data1 => {
            res.send(Data1.rows);
    })
})

app.get('/lastplayed', (req, res, next) => {
    pool.query('select teamname_loc,teamname_vis,pt_loc,pt_vis from matches order by matchdate desc limit 10')
          .then(Data1 => {
            res.send(Data1.rows);
    })
})

app.get('/lastplayed/:league', (req, res, next) => {
    league = req.params.league
    pool.query('select teamname_loc,teamname_vis,pt_loc,pt_vis from matches order by matchdate desc limit 10 where league = $1 ' ,[league])
          .then(Data1 => {
            res.send(Data1.rows);
    })
})



app.get('/players', (req, res, next) => {
    pool.query('Select * from players')
        .then(testData => {
            console.log(testData);
            res.send(testData.rows);
        })
})


app.get('/players', (req, res, next) => {
    pool.query('Select * from players')
        .then(testData => {
            console.log(testData);
            res.send(testData.rows);
        })
})


function translateLeague(league){
    if (league === 'oro') return 'LEB ORO'
    if (league === 'plata') return 'LEB PLATA'
    if (league === 'eba') return 'EBA'
    if (league === 'lf1') return 'LF1'
    if (league === 'lf2') return 'LF2'
    if (league === 'lfchall') return 'LF CHALLENGE'

}

app.get('/:league/rank/:type', (req, res, next) => {
    league = req.params.league

    league = translateLeague(league)
    type = req.params.type
    seasonid = 2

    console.log("entra aqui" + type + seasonid + league)

    if (type == "pt" || type == "t2s"|| type == "t3s"|| type == "rt" || type == "asst" || type == "br" || type == "tf"|| type == "mt" ){
        query = 'select * from stats_season_player where seasonid = 2 and league= $1 order by ' + type +' desc limit 10'
        pool.query(query,[league] )
        .then(testData => {
            res.send(testData.rows);
        })

    }
        
})


// Require the Routes API  
// Create a Server and run it on the port 3001
const server = app.listen(3001, function () {
    let host = server.address().address
    let port = server.address().port
    // Starting the Server at the port 3001
})