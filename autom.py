from ast import LShift
from inspect import _void
from pickle import FALSE
from selenium import webdriver
import scrap as sc
import util


url_match = 'https://baloncestoenvivo.feb.es/partido/'

def importMatchesLeague(driver,league):
    matches = sc.getMatches(driver,1)
    
    for match in matches:
        matchid = match[2]
        jornada = match[1]
        grupo = match [0]
        seasonid = util.translateSeason('2022/2023')

        generic,local,visitor, local_player_stats, visitors_players_stats = sc.getMatchInfo(url_match + str(matchid))
        sc.importMatchStats(matchid,seasonid,league,jornada,grupo,generic,local,visitor)
        sc.importMatchPlayerStats(matchid,seasonid,league,generic,local_player_stats,visitors_players_stats)



def main():
    driver = sc.prepareMainDriver()

    
    importMatchesLeague(driver,'LEB ORO') #LEB ORO
    importMatchesLeague(driver,'LEB PLATA') #LEB PLATA
    importMatchesLeague(driver,'EBA') #EBA
    importMatchesLeague(driver,'LF1') #LF1
    importMatchesLeague(driver,'LF2') #LF2
    importMatchesLeague(driver,'LFCHALLANGE') #LF CHALLANGE

if __name__== "__main__" :
    main()
