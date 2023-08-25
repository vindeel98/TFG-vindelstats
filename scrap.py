from cgitb import text
import json
import requests as rq
from bs4 import BeautifulSoup
import re 
from datetime import datetime
import util
import psycopg2
import db
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException        
from urllib.error import HTTPError
    
def getTeam(url):
    page = rq.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    names = soup.find("span",class_="liga").get_text()
    print(names)
def getRoster(url):

    state = 0

    page = rq.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    'CHECK IF URL EXISTS'
    if not page:
        state = -2
        json_data = '{}'
        playersids = '{}'
        teamid =  None
        teamid = None
        teamname = None
        season = None
        league = None
        return state,json_data,playersids,teamid,teamname,season,league
    
    names = soup.find_all("td",class_="nombre jugador")
    positions = soup.find_all("td", class_="puesto")
    numbers = soup.find_all("td", class_="dorsal")
    ages = soup.find_all("td", class_="fecha nacimiento")
    nationalities = soup.find_all("td", class_="nacionalidad")
    heights = soup.find_all("td", class_="altura")
    wights = soup.find_all("td", class_="peso")

    json_data = util.prepareJSON('roster')
    
    playersids = '{'
    teamname = soup.find("span",class_="titulo").get_text()
    season = soup.find("span",class_="temporada").get_text()
    league = soup.find("span",class_="liga").get_text()

    'CHECK IF URL IS FILL OR NOT'
    try:
        teamid = re.search(r'(?<=i=).*(?=&)', str(names[0])).group(0)
    except IndexError:
        state = -1
        json_data = util.endJSON(json_data)
        playersids+= '}'
        teamid =  re.findall(r'\d+', url[-6:]) 
        teamid = (teamid[0])
        return state,json_data,playersids,teamid,teamname,season,league
        
    size = len(names)
    
    for i in range (size):

        id = re.search(r'(?<=c=).*(?=")', str(names[i])).group(0)
        if (playersids.find(id) != -1):
            continue

        playersids += id + ','       
        x = {
            "id": id,
            "name": names[i].get_text(),
            "position": positions[i].get_text(),
            "number": numbers[i].get_text() ,
            "age": re.search(r'\d{2}\W\d{2}\W\d{4}', ages[i].get_text()).group(0),
            "nationality": nationalities[i].get_text(),
            "height": heights[i].get_text(),
            "weight": wights[i].get_text()
        }
        json_data += json.dumps(x,ensure_ascii=False) + ','

    playersids = playersids[:-1]
    playersids += '}'
    json_data = json_data[:-1]
    json_data = util.endJSON(json_data)
    return state,json_data,playersids,teamid,teamname,season,league
def getTrayectoriaStats(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome('/home/aleix/Desktop/tfg/chromedriver',options=options)
    driver.get(url)
    
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[6]/div[2]/span/span[1]'))).click()    
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="_ctl0_MainContentPlaceHolderMaster_estadisticasCarreraButton"]'))).click()
    
    return driver.page_source

def getStats(teamid):
    url = url_team_stats + '/' + str(teamid)
    state,roster,playersids,teamid,teamname,season,league = getRoster(url_team + '/' + str(teamid))

    page = rq.get(url)
    status = page.status_code
        
    if (str(status).startswith('5')):
        f = open("teamsNOTfound.txt","a")
        f.write("Error at stats with: " + teamid + '\n')
        f.close()
        return 
    
    soup = BeautifulSoup(page.content, "html.parser")

    names = soup.find_all("td",class_="nombre jugador")
    season = util.translateSeason(season)
    league = util.translateLeague(league.strip())
    names = soup.find_all("td",class_="nombre jugador")
    fases   = soup.find_all("td",class_="fase")
    parS = soup.find_all("td",class_="partidos")
    mntS  = soup.find_all("td",class_="minutos")
    ptS = soup.find_all("td",class_="puntos")
    t2S = soup.find_all("td",class_="tiros dos")
    t3S = soup.find_all("td",class_="tiros tres")
    tcS = soup.find_all("td",class_="tiros campo")
    tlS = soup.find_all("td",class_="tiros libres")
    roS = soup.find_all("td",class_="rebotes ofensivos")
    rdS = soup.find_all("td",class_="rebotes defensivos")
    rtS = soup.find_all("td",class_="rebotes total")
    astS = soup.find_all("td",class_="asistencias")
    recS = soup.find_all("td",class_="recuperaciones")
    perS = soup.find_all("td",class_="perdidas")
    tpfS = soup.find_all("td",class_="tapones favor")
    tpcS = soup.find_all("td",class_="tapones contra")
    matS = soup.find_all("td",class_="mates")
    fcS = soup.find_all("td",class_="faltas cometidas")
    frS = soup.find_all("td",class_="faltas recibidas")
    valS = soup.find_all("td",class_="valoracion")

    ids = []
    idnegative = 0

    for name in names:
        href = name.find("a")
        if (href != None):
            href = href['href']
            
            if (href.find("&c=") != -1):
                id = href.split("&c=")[1]
                ids.append(id)
            else:
                #CHECK QUE EXISTA UNA URL DEL JUGADOR, SI NO EXISTE, LO AÑADIREMOS A LA BD CON UN ID NEGATIVO
                if (idnegative == 0):
                    conn = db.connectDB()
                    id = db.getLastPlayer(conn) - 1
                    idnegative = id
                    ids.append(str(id))
                else:
                    id = idnegative - 1
                    idnegative = idnegative - 1
                    ids.append(str(id))
        else:
            ids.append(None)
    size = names.__len__() - 1
    for i in range(size): 
        temporal_name = names[i].get_text().strip()
        temporal_playerid = ids[i]
        
        if (temporal_name != ""):
            name = util.translateName(names[i].get_text().strip())
            playerid = temporal_playerid

        #CHECKEA QUE FORMI PART DE L'EQUIP O NO
        try:
            playersids.index(str(id))
            isfromteam = True
        except ValueError:
            isfromteam = False


        phase = fases[i].get_text().strip()
        games = parS[i].get_text().strip()
        mnt = util.translateMinutes(mntS[i].get_text().strip())
        pt = ptS[i].get_text().strip()
        t2t = t2S[i].get_text().strip().split(' ')[0].split('/')[0]
        t2s = t2S[i].get_text().strip().split(' ')[0].split('/')[1]
        t3t = t3S[i].get_text().strip().split(' ')[0].split('/')[0]
        t3s = t3S[i].get_text().strip().split(' ')[0].split('/')[1]
        tlt = tlS[i].get_text().strip().split(' ')[0].split('/')[0]
        tls = tlS[i].get_text().strip().split(' ')[0].split('/')[1]
        tct = tcS[i].get_text().strip().split(' ')[0].split('/')[0]
        tcs = tcS[i].get_text().strip().split(' ')[0].split('/')[1]
        ro = roS[i].get_text().strip()
        rd = rdS[i].get_text().strip()
        rt = rtS[i].get_text().strip()
        asst = astS[i].get_text().strip()
        br = recS[i].get_text().strip()
        bp = perS[i].get_text().strip()    
        tf = tpfS[i].get_text().strip()
        tc = tpcS[i].get_text().strip()
        mt = matS[i].get_text().strip()
        fc = fcS[i].get_text().strip()
        fr = frS[i].get_text().strip()
        va = valS[i].get_text().strip()
        
        conn = db.connectDB()
        if (conn != 0):
            exist = db.checkPlayerExist(conn,playerid)
            #SI NO EXISTE EL JUGADOR, LO METEMOS EN LA BASE DE DATOS CON EL CAMPO FEBLICENSE = FALSE
            if (not exist):
                nationality = None
                height = None
                position = None
                age = None
                gender = league
                feblicense = False
                db.insertPlayer(conn,playerid,nationality,height,age,position,name,gender,feblicense)
                
            db.insertPlayersStats(conn,name,phase,playerid,teamid,season,league,isfromteam,teamname,games,mnt,pt,t2t,t2s,t3t,t3s,tlt,tls,tct,tcs,ro,rd,rt,asst,bp,br,tf,tc,mt,fc,fr,va)
            
    #IMPORTA LAS STATS DEL EQUIPO ENTERO
    
    size = ptS.__len__() - 1

    pt = ptS[size].get_text().strip()
    t2t = t2S[size].get_text().strip().split(' ')[0].split('/')[0]
    t2s = t2S[size].get_text().strip().split(' ')[0].split('/')[1]
    t3t = t3S[size].get_text().strip().split(' ')[0].split('/')[0]
    t3s = t3S[size].get_text().strip().split(' ')[0].split('/')[1]
    tlt = tlS[size].get_text().strip().split(' ')[0].split('/')[0]
    tls = tlS[size].get_text().strip().split(' ')[0].split('/')[1]
    tct = tcS[size].get_text().strip().split(' ')[0].split('/')[0]
    tcs = tcS[size].get_text().strip().split(' ')[0].split('/')[1]
    ro = roS[size].get_text().strip()
    rd = rdS[size].get_text().strip()
    rt = rtS[size].get_text().strip()
    asst = astS[size].get_text().strip()
    br = recS[size].get_text().strip()
    bp = perS[size].get_text().strip()    
    tf = tpfS[size].get_text().strip()
    tc = tpcS[size].get_text().strip()
    mt = matS[size].get_text().strip()
    fc = fcS[size].get_text().strip()
    fr = frS[size].get_text().strip()
    va = valS[size].get_text().strip()

    conn = db.connectDB()     
    if (conn != 0):
        db.insertTeamStats(conn,teamid,season,league,teamname,pt,t2t,t2s,t3t,t3s,tlt,tls,tct,tcs,ro,rd,rt,asst,bp,br,tf,tc,mt,fc,fr,va)

def importPlayersStats():
    conn = db.connectDB()
    if (conn != 0):
        try:
            clubid = 1
            teams = db.getTeams(conn)

        except Exception as e:
            print("I am unable to getTeams to the database " + e)
    
    for teamid in teams:
        getStats(teamid)

def importTeam(url):
    state,roster,playersids,teamid,teamname,season,league = getRoster(url)
    conn = db.connectDB()
    
    if (conn != 0 and state != -2):
        try:
            clubid = None
            available = True
            status = db.insertTeam(conn,teamid,teamname,playersids,season,league,clubid,available)
        except Exception as e:
            print("I am unable to insertTeam to the database " + e)
    if (state == -1):
        print(teamname + "Dataweb not fill with stats yet")
    
    if (state == -2):
        print("This page not exists")
    
def importPlayersTeam(url):
    state,roster,playersids,teamid,teamname,season,league = getRoster(url)
    conn = db.connectDB()
    if (conn != 0 and state != -2):
        try:
            clubid = None
            playersids = list(dict.fromkeys(playersids))  
            status = db.insertPlayersTeam(conn,roster,teamid,teamname,playersids,league)

        except Exception as e:
            print("I am unable to insertPlayersTeam to the database " + e)
    if (state == -1):
        print("Dataweb not fill with stats yet")

    if (state == -2):
        print("This page not exists")

def getTeamsFromURLs(driver,grupos_size):

    teams = []
    for grupo in range(0, grupos_size):
        select = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_gruposDropDownList"))
        grupos = select.options
        select.select_by_index(grupo)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        ases = soup.findAll("a",href=True)

        for a in ases:
            link = str(a['href'])
            if (link.find('https://baloncestoenvivo.feb.es/Equipo.aspx?i') != -1):
                num = re.findall(r'\d+', link[-6:]) 
                teams.append(num[0])
    return teams

def importInfoLeague(driver,liga):
    
    for temporada in range(1996,2022):
        url_completa = url_feb + "/" + str(liga) + "/" + str(temporada)
        driver.get(url_completa)

        try:
            select = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_gruposDropDownList"))
            grupos = select.options
            grupos_size = len(grupos)
        
        except NoSuchElementException:
            continue

        teams = getTeamsFromURLs(driver,grupos_size)
        teams = list(dict.fromkeys(teams))  

        f = open("importlog.txt","a")
        f.write("LIGA: " + str(liga) + " TEMPORADA: " + str(temporada) + " NUM TEAMS: " + str(len(teams)) + '\n')
        f.close()

        for team in teams:
            importTeam(url_team + team) 
            importPlayersTeam(url_team + team) 

def updateDB(variable):
    if variable == 'seasonname':
        conn = db.connectDB()
        if (conn != 0):
            try:
                status = db.updateSeasonName(conn)
            except Exception as e:
                print("I am unable to updateSeasonName to the database " + e)

def getMatchesFromURLs(driver,grupos_size):
    matches = []

    for grupo in range(0, grupos_size):
        
        
        select_grupos = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_gruposDropDownList"))
        select_grupos.select_by_index(grupo)
        select_grupos = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_gruposDropDownList"))
        grupo_text = select_grupos.first_selected_option.text
       

        select_jornada = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_jornadasDropDownList"))
        jornadas_size = len(select_jornada.options)
        
 
        for jornada in range(0,jornadas_size):
            select_jornada = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_jornadasDropDownList"))
            select_jornada.select_by_index(jornada)
            select_jornada = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_jornadasDropDownList"))
            jornada_text = select_jornada.first_selected_option.text

            soup = BeautifulSoup(driver.page_source, "html.parser")
            ases = soup.findAll("a",href=True)

            for a in ases:
                link = str(a['href'])
                if (link.find('https://baloncestoenvivo.feb.es/Partido.aspx?p') != -1):
                    num = re.findall(r'\d+', link[-7:]) 
                    x = (grupo_text,jornada_text,num[0])
                    matches.append(x)
    
    return matches

def getMatches(driver,liga):
    temporada = 2021
    url_completa = url_feb + "/" + str(liga) + "/" + str(temporada)
    
    driver.get(url_completa)

    try:
        select = Select(driver.find_element_by_id("_ctl0_MainContentPlaceHolderMaster_gruposDropDownList"))
        grupos = select.options
        grupos_size = len(grupos)

    except NoSuchElementException:
        return
    

    json_data = getMatchesFromURLs(driver,grupos_size)
    print(json_data)
    return json_data

def getMatchInfo(url):
    page = rq.get(url)
    soup = BeautifulSoup(page.content, "html.parser") 
    names = soup.findAll("span",class_="nombre")

    #INFORMACION GENERICA DEL PARTIDO
    teamname_loc = names[0].get_text().strip()
    teamname_vis = names[1].get_text().strip()

    teamid_loc = names[0].find("a")['href'].split("?i=")[1]
    teamid_vis = names[1].find("a")['href'].split("?i=")[1]

    matchdate = soup.find("span",class_="txt").get_text().strip().split('-')[0].strip()
    matchlocation = soup.find("span",class_="txt direccion").get_text().strip()
    matchcourt= soup.find("span",class_="txt pabellon").get_text().strip()

    referees= soup.findAll("span",class_="txt referee")
    referee_list = []
    for referee in referees:
        referee_list.append(referee.get_text().strip())
    
    score = soup.findAll("span",class_="resultado")
    pt_loc = score[0].get_text().strip()
    pt_vis = score[1].get_text().strip()

    if (pt_loc > pt_vis):
        teamid_winner = teamid_loc
        teamname_winner = teamname_loc
    
    else:
        teamid_winner = teamid_vis
        teamname_winner =  teamname_vis

    generic = {
        "matchdate": matchdate,
        "matchlocation": matchlocation,
        "matchcourt": matchcourt,
        "referees" : util.translateReferees(referee_list),
        "teamid_loc" : teamid_loc,
        "teamid_vis" : teamid_vis,
        "teamname_loc" : teamname_loc,
        "teamname_vis" : teamname_vis,
        "teamid_winner" : teamid_winner,
        "teamname_winner" : teamname_winner,
        "pt_loc" : pt_loc,
        "pt_vis" : pt_vis
    }

    #INFORMACION DE ESTADISTICAS
    quarters_score = soup.findAll("span",class_="marcador")
    firstqt_loc = quarters_score[0].get_text().strip().split('/')[0]
    firstqt_vis = quarters_score[0].get_text().strip().split('/')[1]
    secondqt_loc = quarters_score[1].get_text().strip().split('/')[0]
    secondqt_vis = quarters_score[1].get_text().strip().split('/')[1]
    thirdqt_loc = quarters_score[2].get_text().strip().split('/')[0]
    thirdqt_vis = quarters_score[2].get_text().strip().split('/')[1]
    fourth_loc = quarters_score[3].get_text().strip().split('/')[0]
    fourth_vis = quarters_score[3].get_text().strip().split('/')[1]

    #FALTA COMPROVAR QUE NO HI HAN PRORROGUES
    prorr_loc = None
    prror_vis = None


    local = {
        "teamid_loc": teamid_loc,
        "teamname_loc": teamname_loc,
        "pt_loc" : pt_loc,
        "firstqt_loc" : firstqt_loc,
        "secondqt_loc" : secondqt_loc,
        "thirdqt_loc" : thirdqt_loc,
        "fourthqt_loc" : fourth_loc,
        "prorr_loc" : prorr_loc
    }
    visitor = {
        "teamid_vis": teamid_vis,
        "teamname_vis": teamname_vis,
        "pt_vis" : pt_vis,
        "firstqt_vis" : firstqt_vis,
        "secondqt_vis" : secondqt_vis,
        "thirdqt_vis" : thirdqt_vis,
        "fourthqt_vis" : fourth_vis,
        "prorr_vis" : prror_vis

    }

    soup = BeautifulSoup(page.content, "html.parser")

    incialS = soup.find_all("td",class_="inicial")
    dorsalS = soup.find_all("td",class_="dorsal")
    names = soup.find_all("td",class_="nombre jugador")
    mntS  = soup.find_all("td",class_="minutos")
    ptS = soup.find_all("td",class_="puntos")
    t2S = soup.find_all("td",class_="tiros dos")
    t3S = soup.find_all("td",class_="tiros tres")
    tcS = soup.find_all("td",class_="tiros campo")
    tlS = soup.find_all("td",class_="tiros libres")
    roS = soup.find_all("td",class_="rebotes ofensivos")
    rdS = soup.find_all("td",class_="rebotes defensivos")
    rtS = soup.find_all("td",class_="rebotes total")
    astS = soup.find_all("td",class_="asistencias")
    recS = soup.find_all("td",class_="recuperaciones")
    perS = soup.find_all("td",class_="perdidas")
    tpfS = soup.find_all("td",class_="tapones favor")
    tpcS = soup.find_all("td",class_="tapones contra")
    matS = soup.find_all("td",class_="mates")
    fcS = soup.find_all("td",class_="faltas cometidas")
    frS = soup.find_all("td",class_="faltas recibidas")
    valS = soup.find_all("td",class_="valoracion")
    balS = soup.find_all("td",class_="balance")

    local_players_stats = []
    vis_players_stats = []
    trobat = False
    
    for i in range(names.__len__()):
        name =  names[i].get_text().strip()
                
        if (name != "" and not trobat):
            name =  names[i]
            href = name.find("a")['href']
            if (href.find("&c=") != -1):
                id = href.split("&c=")[1]

            x = {
                "id" : id,
                "teamid_own": teamid_loc,
                "starter" :  incialS[i].get_text().strip(),
                "dorsal" : dorsalS[i].get_text().strip(),
                "name" :  names[i].get_text().strip(),
                "mnt" :  util.translateMinutes(mntS[i].get_text().strip()),
                "pt" :  ptS[i].get_text().strip(),
                "t2t" :  t2S[i].get_text().strip().split(' ')[0].split('/')[0],
                "t2s" :  t2S[i].get_text().strip().split(' ')[0].split('/')[1],
                "t3t" :  t3S[i].get_text().strip().split(' ')[0].split('/')[0],
                "t3s" :  t3S[i].get_text().strip().split(' ')[0].split('/')[1],
                "tlt" :  tlS[i].get_text().strip().split(' ')[0].split('/')[0],
                "tls" :  tlS[i].get_text().strip().split(' ')[0].split('/')[1],
                "tct" :  tcS[i].get_text().strip().split(' ')[0].split('/')[0],
                "tcs" :  tcS[i].get_text().strip().split(' ')[0].split('/')[1],
                "ro":  roS[i].get_text().strip(),
                "rd" :  rdS[i].get_text().strip(),
                "rt" :  rtS[i].get_text().strip(),
                "asst":  astS[i].get_text().strip(),
                "br" :   recS[i].get_text().strip(),
                "bp" :   perS[i].get_text().strip(),    
                "tf" :   tpfS[i].get_text().strip(),
                "tc" :   tpcS[i].get_text().strip(),
                "mt" :   matS[i].get_text().strip(),
                "fc" :   fcS[i].get_text().strip(),
                "fr" :   frS[i].get_text().strip(),
                "va" :   valS[i].get_text().strip(),
                "bal" :  balS[i].get_text().strip()
            } 
            local_players_stats.append(x)
        elif (name != "" and trobat):
            name =  names[i]
            href = name.find("a")['href']
            if (href.find("&c=") != -1):
                id = href.split("&c=")[1]

            x = {
                "id" : id,
                "teamid_own": teamid_vis,
                "starter" :  incialS[i].get_text().strip(),
                "dorsal" : dorsalS[i].get_text().strip(),
                "name" :  names[i].get_text().strip(),
                "mnt" :  util.translateMinutes(mntS[i].get_text().strip()),
                "pt" :  ptS[i].get_text().strip(),
                "t2t" :  t2S[i].get_text().strip().split(' ')[0].split('/')[0],
                "t2s" :  t2S[i].get_text().strip().split(' ')[0].split('/')[1],
                "t3t" :  t3S[i].get_text().strip().split(' ')[0].split('/')[0],
                "t3s" :  t3S[i].get_text().strip().split(' ')[0].split('/')[1],
                "tlt" :  tlS[i].get_text().strip().split(' ')[0].split('/')[0],
                "tls" :  tlS[i].get_text().strip().split(' ')[0].split('/')[1],
                "tct" :  tcS[i].get_text().strip().split(' ')[0].split('/')[0],
                "tcs" :  tcS[i].get_text().strip().split(' ')[0].split('/')[1],
                "ro":  roS[i].get_text().strip(),
                "rd" :  rdS[i].get_text().strip(),
                "rt" :  rtS[i].get_text().strip(),
                "asst":  astS[i].get_text().strip(),
                "br" :   recS[i].get_text().strip(),
                "bp" :   perS[i].get_text().strip(),    
                "tf" :   tpfS[i].get_text().strip(),
                "tc" :   tpcS[i].get_text().strip(),
                "mt" :   matS[i].get_text().strip(),
                "fc" :   fcS[i].get_text().strip(),
                "fr" :   frS[i].get_text().strip(),
                "va" :   valS[i].get_text().strip(),
                "bal" : balS[i].get_text().strip()
            } 
            vis_players_stats.append(x)
        elif (name == "" and not trobat):
            trobat = True
            local.update({"mnt" :  util.translateMinutes(mntS[i].get_text().strip())})
            local.update({"pt" :  ptS[i].get_text().strip()})
            local.update({"t2t" :  t2S[i].get_text().strip().split(' ')[0].split('/')[0]})
            local.update({"t2s" :  t2S[i].get_text().strip().split(' ')[0].split('/')[1]})
            local.update({"t3t" :  t3S[i].get_text().strip().split(' ')[0].split('/')[0]})
            local.update({"t3s" :  t3S[i].get_text().strip().split(' ')[0].split('/')[1]})
            local.update({"tlt" :  tlS[i].get_text().strip().split(' ')[0].split('/')[0]})
            local.update({"tls" :  tlS[i].get_text().strip().split(' ')[0].split('/')[1]})
            local.update({"tct" :  tcS[i].get_text().strip().split(' ')[0].split('/')[0]})
            local.update({"tcs" :  tcS[i].get_text().strip().split(' ')[0].split('/')[1]})
            local.update({"ro":  roS[i].get_text().strip()})
            local.update({"rd" :  rdS[i].get_text().strip()})
            local.update({"rt" :  rtS[i].get_text().strip()})
            local.update({"asst":  astS[i].get_text().strip()})
            local.update({"br" :   recS[i].get_text().strip()})
            local.update({"bp" :   perS[i].get_text().strip()})   
            local.update({"tf" :   tpfS[i].get_text().strip()})
            local.update({"tc" :   tpcS[i].get_text().strip()})
            local.update({"mt" :   matS[i].get_text().strip()})
            local.update({"fc" :   fcS[i].get_text().strip()})
            local.update({"fr" :   frS[i].get_text().strip()})
            local.update({"va" :   valS[i].get_text().strip()})
            local.update({"bal" :  balS[i].get_text().strip()})
        else:
            visitor.update({"mnt" :  util.translateMinutes(mntS[i].get_text().strip())})
            visitor.update({"pt" :  ptS[i].get_text().strip()})
            visitor.update({"t2t" :  t2S[i].get_text().strip().split(' ')[0].split('/')[0]})
            visitor.update({"t2s" :  t2S[i].get_text().strip().split(' ')[0].split('/')[1]})
            visitor.update({"t3t" :  t3S[i].get_text().strip().split(' ')[0].split('/')[0]})
            visitor.update({"t3s" :  t3S[i].get_text().strip().split(' ')[0].split('/')[1]})
            visitor.update({"tlt" :  tlS[i].get_text().strip().split(' ')[0].split('/')[0]})
            visitor.update({"tls" :  tlS[i].get_text().strip().split(' ')[0].split('/')[1]})
            visitor.update({"tct" :  tcS[i].get_text().strip().split(' ')[0].split('/')[0]})
            visitor.update({"tcs" :  tcS[i].get_text().strip().split(' ')[0].split('/')[1]})
            visitor.update({"ro":  roS[i].get_text().strip()})
            visitor.update({"rd" :  rdS[i].get_text().strip()})
            visitor.update({"rt" :  rtS[i].get_text().strip()})
            visitor.update({"asst":  astS[i].get_text().strip()})
            visitor.update({"br" :   recS[i].get_text().strip()})
            visitor.update({"bp" :   perS[i].get_text().strip()})   
            visitor.update({"tf" :   tpfS[i].get_text().strip()})
            visitor.update({"tc" :   tpcS[i].get_text().strip()})
            visitor.update({"mt" :   matS[i].get_text().strip()})
            visitor.update({"fc" :   fcS[i].get_text().strip()})
            visitor.update({"fr" :   frS[i].get_text().strip()})
            visitor.update({"va" :   valS[i].get_text().strip()})
            visitor.update({"bal" :  balS[i].get_text().strip()})

    return generic, local, visitor, local_players_stats, vis_players_stats


def importMatchStats(matchid,seasonid,league,jornada,grupo,generic,local,visitor):
    conn = db.connectDB()
    if (conn != 0):
        try:
            status = db.importMatch(conn,matchid,seasonid,league,jornada,grupo,generic,local,visitor)
            status = db.insertMatchStats(conn,matchid,seasonid,league,generic,local,visitor)

        except Exception as e:
            print("I am unable to importMatchStats to the database " + e)

def importMatchPlayerStats(matchid,seasonid,league,generic,local,visitor):
    for player in local:
        stats = {
           "playername" : player["name"],
           "playerid" : player["id"],
           "dorsal" : player["dorsal"],
            "teamid_own": player["teamid_own"],
            "starter": util.translateStarter(player["starter"]),
            "mnt": player["mnt"],
            "pt": player["pt"],
            "t2s": player["t2t"],
            "t3s": player["t3s"],
            "tcs": player["tcs"],
            "tls": player["tls"],
            "t2t": player["t2t"],
            "t3t": player["t3t"],
            "tct": player["tct"],
            "tlt": player["tlt"],

            "ro":player["ro"],
            "rd":player["rd"],
            "rt":player["rt"],
            "asst":player["asst"],
            "br":player["br"],
            "bp": player["bp"],
            "tf": player["tf"],
            "tc": player["tc"],
            "mt": player["mt"],
            "fc": player["fc"],
            "fr": player["fr"],
            "va": player["va"],
            "masmenos": player["bal"]

        }
    
        conn = db.connectDB()
        if (conn != 0):
            try:
                print(stats)
                status = db.importMatchPlayerStats(conn,matchid,seasonid,league,stats,generic)

            except Exception as e:
                print("I am unable to importMatchPlayerStats to the database " + e)
    for player in visitor:
        stats = {
            "playerid" : player["id"],
            "playername" : player["name"],
            "dorsal" : player["dorsal"],
            "teamid_own": player["teamid_own"],
            "starter": util.translateStarter(player["starter"]),
            "mnt": player["mnt"],
            "pt": player["pt"],
            "t2s": player["t2t"],
            "t3s": player["t3s"],
            "tcs": player["tcs"],
            "tls": player["tls"],
            "t2t": player["t2t"],
            "t3t": player["t3t"],
            "tct": player["tct"],
            "tlt": player["tlt"],

            "ro":player["ro"],
            "rd":player["rd"],
            "rt":player["rt"],
            "asst":player["asst"],
            "br":player["br"],
            "bp": player["bp"],
            "tf": player["tf"],
            "tc": player["tc"],
            "mt": player["mt"],
            "fc": player["fc"],
            "fr": player["fr"],
            "va": player["va"],
            "masmenos": player["bal"]
        }
    
        conn = db.connectDB()
        if (conn != 0):
            try:
                status = db.importMatchPlayerStats(conn,matchid,seasonid,league,stats,generic)

            except Exception as e:
                print("I am unable to importMatchPlayerStats to the database " + e)



def importMatchesLeague(driver,league):
    matches = getMatches(driver,1)
    print(matches)
    
    for match in matches:
        matchid = match[2]
        jornada = match[1]
        grupo = match [0]
        seasonid = util.translateSeason('2021/2022')

        generic,local,visitor, local_player_stats, visitors_players_stats = getMatchInfo(url_match + str(matchid))
        importMatchStats(matchid,seasonid,league,jornada,grupo,generic,local,visitor)
        importMatchPlayerStats(matchid,seasonid,league,generic,local_player_stats,visitors_players_stats)

#VARIABLES GLOBALES
url_team = "https://baloncestoenvivo.feb.es/equipo/"
url_feb = "https://baloncestoenvivo.feb.es/resultados"
url_player = 'https://baloncestoenvivo.feb.es/jugador' 
url_stats = 'https://baloncestoenvivo.feb.es/estadisticas'
url_team_stats = 'https://baloncestoenvivo.feb.es/estadisticasacumuladas'
url_match = 'https://baloncestoenvivo.feb.es/partido/'


def main():
    driver = util.prepareMainDriver()

    #IMPORTA TOTA LA INFORMACIO DE LES DIFERENTS LLIGUES
    #importInfoLeague(driver,1)  #LEB ORO
    #importInfoLeague(driver,2)  #LEB PLATA
    #importInfoLeague(driver,3)  #EBA
    #importInfoLeague(driver,4)  #LF1
    #importInfoLeague(driver,9)  #LF2
    #importInfoLeague(driver,67) #LF CHALLANGE
    #updateDB('seasonname')
    
    #IMPORTA TOTA LES ESTADÍSTIQUES DE JUGADORS I EQUIPS
    #importPlayersStats()
    
    importMatchesLeague(driver,'LEB ORO') #LEB ORO
    #importMatchesLeague(driver,'LEB PLATA') #LEB PLATA
    #importMatchesLeague(driver,'EBA') #EBA
    #importMatchesLeague(driver,'LF1') #LF1
    #importMatchesLeague(driver,'LF2') #LF2
    #importMatchesLeague(driver,'LFCHALLANGE') #LF CHALLANGE

if __name__== "__main__" :
    main()



