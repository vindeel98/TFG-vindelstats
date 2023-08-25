import psycopg2
import json
import time
import util

def connectDB():
    try:
        conn = psycopg2.connect(
            database="vindelstats",
            host="localhost",
            user="postgres",
            password="1190400237986")
        return conn

    except:
        print("I am unable to connect to the database")
        return 0


def insertTeam(conn,teamid,teamname,playersids,season,league,clubid,available):
    cursor = conn.cursor()

    print(teamid,teamname,playersids,util.translateSeason(season),util.translateLeague(league.strip()))
    query = "INSERT INTO teams (teamid,clubid,teamname,playersid,seasonid,league,available) values(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(teamid,clubid,teamname,playersids,util.translateSeason(season),util.translateLeague(league.strip()),available))
    conn.commit()

def checkPlayerExist(conn,playerid):
    cursor = conn.cursor()
    cursor.execute("SELECT * from players where playerid= %s", [playerid])
    conn.commit()
    
    data = cursor.fetchone()
    if data == None:
        return False
    else:
        return True

def checkTeamExist(conn,teamid):
    cursor = conn.cursor()
    cursor.execute("SELECT * from teams where teamid= %s", [teamid])
    conn.commit()
    
    data = cursor.fetchone()
    if data == None:
        return False
    else:
        return True
def insertPlayersTeam(conn,roster,teamid,teamname,playersids,league):

    cursor = conn.cursor()
    roster_dict = json.loads(roster)

    for items in roster_dict.items():
        for player in items[1]:
            playerid = player.get('id')
            playerid = playerid.replace(',',"")

            if(not checkPlayerExist(conn,playerid)):
                name = player.get('name')

                height = util.translateInt(player.get('height'))
                weight = util.translateInt(player.get('weight'))
                nationality = player.get('nationality')
                age = util.translateAge(player.get('age'))
                position = util.translatePosition(player.get('position'))
                gender = util.translateGender(league)
            
                
                print(playerid,name,age,nationality,height,gender,position)
                query = "INSERT INTO players (playerid,name,age,nationality,height,gender,position) values (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,(playerid,name,age,nationality,height,gender,position))
                conn.commit()

def checkOrInsertTeam(conn,teamid,teamname,playersids,season,league,clubid):
    cursor = conn.cursor()
    exist = checkTeamExist(conn,teamid)
    if (not exist):
        available = False

        season = season.strip()
        f = open("teamsNOTfound.txt","a")
        f.write("New team added: " + teamid + " " + teamname + " " + season + " " + util.translateLeague(league) +'\n')
        f.close()

        insertTeam(conn,teamid,teamname,playersids,season,league,clubid,available)

def updateSeasonName(conn):
    cursor = conn.cursor()
    query = 'update teams set seasonname = seasons.seasonname from seasons where seasons.seasonid = teams.seasonid'
    cursor.execute(query)
    conn.commit()

def getTeams(conn):
    cursor = conn.cursor()
    query = 'select teamid from teams'
    cursor.execute(query)
    
    data = cursor.fetchall()
    list = []
    
    for row in data:
        list.append(row[0])
        
    return list

def searchTeam(conn,seasonid,teamname):
    cursor = conn.cursor()
    query = 'select teamid,league from teams where seasonid = %s and teamname = %s'
    cursor.execute(query,(seasonid,teamname))
    conn.commit()
    data = cursor.fetchone()
    return (data[0],data[1])

def insertPlayersStats(conn,name,phase,id,teamid,season,league,isfromteam,teamname,games,mnt,pt,t2t,t2s,t3t,t3s,tlt,tls,tct,tcs,ro,rd,rt,asst,bp,br,tf,tc,mt,fc,fr,va):
    cursor = conn.cursor()

    exists = checkPlayerStatsExist(conn,id,season,phase,teamid)
    if (not exists):
        query = "INSERT INTO stats_season_player (seasonid,playerid,phase,name,league,teamname,teamid,games,mnt,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va,tlt,isfromteam) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print(name,phase,id,teamid,season,league,isfromteam,teamname,games,mnt,pt,t2t,t2s,t3t,t3s,tlt,tls,tct,tcs,ro,rd,rt,asst,bp,br,tf,tc,mt,fc,fr,va)
        cursor.execute(query,(season,id,phase,name,league,teamname,teamid,games,mnt,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va,tlt,isfromteam))
        conn.commit()
    else:
        query = "SELECT games,mnt,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va,tlt from stats_season_player where seasonid = %s and phase = %s and playerid = %s and teamid = %s"
        cursor.execute(query,(season,phase,id,teamid))
        conn.commit()

        data = cursor.fetchone()
        
        games_new = str(int(games) + data[0])
        mnt_new = str(int(mnt) +  data[1]) 
        pt_new = str(int(pt) + data[2])
        t2s_new = str(int(t2s) + data[3])
        t3s_new = str(int(t3s) + data[4])
        tcs_new =str(int(tcs) + data[5])
        tls_new = str(int(tls) + data[6])
        t2t_new = str(int(t2t) + data[7])
        t3t_new = str(int(t3t) + data[8])
        tct_new = str(int(tct) + data[9]) 
        ro_new = str(int(ro) + data[10])
        rd_new =str(int(rd) + data[11])
        rt_new = str(int(rt) + data[12])
        asst_new = str(int(asst) + data[13])
        br_new = str(int(br) + data[14])
        bp_new= str(int(bp) + data[15])
        tf_new = str(int(tf) + data[16])
        tc_new = str(int(tc) + data[17])
        mt_new = str(int(mt) + data[18])
        fc_new = str(int(fc) + data[19])
        fr_new = str(int(fr) + data[20])
        va_new = str(int(va) + data[21])
        tlt_new = str(int(tlt) + data[22])
        
        query = "UPDATE stats_season_player set games = %s,mnt = %s,pt = %s,t2s = %s,t3s = %s,tcs = %s,tls = %s,t2t = %s,t3t = %s,tct = %s,ro = %s,rd = %s,rt = %s,asst = %s,br = %s,bp = %s,tf = %s,tc = %s,mt = %s,fc = %s,fr = %s,va = %s,tlt = %s where seasonid = %s and phase = %s and playerid = %s and teamid = %s"
        cursor.execute(query,(games_new,mnt_new,pt_new,t2s_new,t3s_new,tcs_new,tls_new,t2t_new,t3t_new,tct_new,ro_new,rd_new,rt_new,asst_new,br_new,bp_new,tf_new,tc_new,mt_new,fc_new,fr_new,va_new,tlt_new,season,phase,id,teamid))
        
        f = open("updateStats.txt","a")
        print(id,teamid,teamname,season,league)
        f.write("Player sum: " + str(id) +  " " + str(teamid) + " " + str(teamname) + " " + str(season) + " " + league +'\n')
        f.close()
        conn.commit()

def insertTeamStats(conn,teamid,seasonid,league,teamname,pt,t2t,t2s,t3t,t3s,tlt,tls,tct,tcs,ro,rd,rt,asst,bp,br,tf,tc,mt,fc,fr,va):
    cursor = conn.cursor()
    query = "INSERT INTO stats_season_team (seasonid,teamid,league,teamname,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,tlt,ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print (seasonid,teamid,league,teamname,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,tlt,ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va)
    cursor.execute(query,(seasonid,teamid,league,teamname,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,tlt,ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va))
    conn.commit()


def checkPlayerStatsExist(conn,playerid,seasonid,phase,teamid):
    cursor = conn.cursor()
    cursor.execute("SELECT * from stats_season_player where playerid= %s and seasonid= %s and phase= %s and teamid= %s", [playerid,seasonid,phase,teamid])
    conn.commit()
    
    data = cursor.fetchone()
    if data == None:
        return False
    else:
        return True


def insertPlayer(conn,playerid,nationality,height,age,position,name,gender,feblicense):
    cursor = conn.cursor()
    query = "INSERT INTO players (playerid,nationality,height,age,position,name,gender,feblicense) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    
    f = open("notFEBPlayers.txt","a")
    gender = util.translateGender(gender)
    f.write("New player added: " + playerid + " " + name + " " + gender + " " +'\n')
    f.close()

    #print(playerid,nationality,height,age,position,name,gender,feblicense)
    cursor.execute(query,(playerid,nationality,height,age,position,name,gender,feblicense))
    conn.commit()

def getLastPlayer(conn):
    cursor = conn.cursor()
    query = "SELECT min(playerid) from players "
    cursor.execute(query)
    conn.commit()
    data = cursor.fetchone()
    return data[0]

def importMatch(conn,matchid,seasonid,league,jornada,grupo,generic,local,visitor):
    cursor = conn.cursor()
    query = "INSERT INTO matches (matchid,matchdate,matchlocation,seasonid,matchcourt,referees,teamid_loc,teamid_vis,teamname_loc,teamname_vis,teamname_winner,teamid_winner,pt_loc,pt_vis,league,jornada,grupo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    matchdate =  util.translateAge(generic.get("matchdate"))
    matchlocation = generic.get("matchlocation")
    matchcourt = generic.get("matchcourt")
    referees = generic.get("referees")
    teamid_loc = generic.get("teamid_loc")
    teamid_vis = generic.get("teamid_vis")
    teamname_loc = generic.get("teamname_loc")
    teamname_vis = generic.get("teamname_vis")
    teamid_winner = generic.get("teamid_winner")
    teamname_winner = generic.get("teamname_winner")
    pt_loc = generic.get("pt_loc")
    pt_vis = generic.get("pt_vis")

    league = util.translateLeague(league)
    

    #print(matchid,matchdate,matchlocation,seasonid,matchcourt,referees,teamid_loc,teamid_vis,teamname_loc,teamname_vis,teamname_winner,teamid_winner,pt_loc,pt_vis,league,jornada,grupo)
    cursor.execute(query,(matchid,matchdate,matchlocation,seasonid,matchcourt,referees,teamid_loc,teamid_vis,teamname_loc,teamname_vis,teamname_winner,teamid_winner,pt_loc,pt_vis,league,jornada,grupo))
    conn.commit()


def insertMatchStats(conn,matchid,seasonid,league,generic,local,visitor):
    print("2")
def importMatchPlayerStats(conn,matchid,seasonid,league,stats,generic):

    print(stats)
    cursor = conn.cursor()
    query = "INSERT INTO stats_match_player \
        (matchid,seasonid,league,teamid_own,teamid_loc,teamid_vis,teamname_loc,teamname_vis, \
        starter,mnt,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,tlt, \
        ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va,masmenos,playerid,playername,dorsal \
        ) values \
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
         %s,%s,%s,%s,%s)"

    league = util.translateLeague(league)
    teamid_loc = generic.get('teamid_loc')
    teamid_vis = generic.get('teamid_vis')
    teamname_loc = generic.get("teamname_loc")
    teamname_vis = generic.get("teamname_vis")

    playerid = stats.get('playerid')
    teamid_own = stats.get('teamid_own')
    starter = stats.get('starter')
    mnt = stats.get('mnt')
    pt = stats.get('pt')
    t2s = stats.get('t2t')
    t3s = stats.get('t3t')
    tcs = stats.get('tcs')
    tls = stats.get('tls')
    t2t = stats.get('t2t')
    t3t = stats.get('t3t')
    tct = stats.get('tct')
    tlt = stats.get('tlt')

    ro = stats.get('ro')
    rd= stats.get('rd')
    rt= stats.get('rt')
    asst = stats.get('asst')
    br= stats.get('br')
    bp= stats.get('bp')
    tf= stats.get('tf')
    tc= stats.get('tc')
    mt= stats.get('mt')
    fc= stats.get('fc')
    fr= stats.get('fr')
    va= stats.get('va')
    masmenos = stats.get("masmenos")
    playername = util.translateName(stats.get("playername"))
    dorsal =  stats.get("dorsal")

    if (not checkPlayerExist(conn,playerid)):
        insertPlayer(conn,playerid,None,None,None,None,playername,util.translateGender(league),False)


    cursor.execute(query,
    (matchid,seasonid,league,teamid_own,teamid_loc,teamid_vis,teamname_loc,teamname_vis, \
        starter,mnt,pt,t2s,t3s,tcs,tls,t2t,t3t,tct,tlt, \
        ro,rd,rt,asst,br,bp,tf,tc,mt,fc,fr,va,masmenos,playerid,playername,dorsal))
    
    conn.commit()