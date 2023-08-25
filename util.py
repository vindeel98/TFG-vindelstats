from ast import LShift
from inspect import _void
from pickle import FALSE
from selenium import webdriver

def prepareJSON(word):
    return '{'+'"'+word+'":['

def endJSON(data):
    return data + ']}' 

def translateAge(age):

    if (age == ''):
        return None
    format = '%Y-%m-%d'
    age = age.split("/")


    year = age[2]
    month = age[1]
    day = age[0]
    
    age = year +'-'+month +'-'+day
    '''age = time.strptime(age,format)'''
    return age

def translateInt(variable):
    if (variable == '-' or variable == ' '):
         return None
    else:
        return variable

def translatePosition(variable):
    if (variable == '-' or variable == ' '):
         return None
    if (variable == 'Alero'):
        return 'FORWARD'
    
def translateGender(league):

    league = translateLeague(league.strip())
    if (league == "LEB ORO" or  league == "ADECCO ORO"  or  league == "ADECCO PLATA" or league == "LEB PLATA" or league == "ADECCO BRONCE" or league == "EBA" or league == "LEB" or league == "LEB 2" or league == "1A DIVISION"):
         return "Male"
    else: 
        return "Famale"

def translateLeague(league):
    if (league == "LIGA LEB ORO" or league == "LEB ORO" or league == "1"):
        return "LEB ORO"

    if (league == "ADECCO ORO" or league == "ADECCO LEB ORO" or league == "ORO"):
        return "ADECCO ORO"

    if (league == "LIGA LEB PLATA" or league == "LEB PLATA" or league == "2"):
        return "LEB PLATA" 

    if (league == "ADECCO PLATA" or league == "ADECCO LEB PLATA" or league == "PLATA"):
        return "ADECCO PLATA" 

    if (league == "ADECCO BRONCE" or league == "ADECCO LEB BRONCE" or league == "BRONCE"):
        return "ADECCO BRONCE" 

    if (league == "LIGA EBA" or league == "EBA" or league == "3"):
        return "EBA"    
    
    if (league == "LEB"):
        return "LEB" 

    if (league == "LEB 2"):
        return "LEB 2"

    if (league == "Liga Femenina 1" or league == "Liga Femenina de Baloncesto" or league == "LIGA DIA" or league == "LF ENDESA" or league == "4"):
        return "LF1"

    if (league == "Liga Femenina 2" or league == "Liga Femenina de Baloncesto 2" or league == "L.F.-2" or league == "9"):
        return "LF2"

    if (league == "LF CHALLENGE" or league == "67"):
        return "LF CHALLENGE"

    if (league == "1ª División M."):
        return "1A DIVISION"

def translateSeason(season):
    if (season == '2022/2023' or season == '22/23'):
        return 1
    if (season == '2021/2022' or season == '21/22'):
        return 2
    if (season == '2020/2021' or season == '20/21'):
        return 3
    if (season == '2019/2020' or season == '19/20'):
        return 4
    if (season == '2018/2019' or season == '18/19'):
        return 5
    if (season == '2017/2018'or season == '17/18'):
        return 6
    if (season == '2016/2017' or season == '16/17'):
        return 7
    if (season == '2015/2016' or season == '15/16'):
        return 8
    if (season == '2014/2015' or season == '14/15'):
        return 9
    if (season == '2013/2014' or season == '13/14'):
        return 10
    if (season == '2012/2013' or season == '12/13'):
        return 11
    if (season == '2011/2012' or season == '11/12'):
        return 12
    if (season == '2010/2011' or season == '10/11'):
        return 13
    if (season == '2009/2010' or season == '09/10'):
        return 14
    if (season == '2008/2009' or season == '08/09'):
        return 15
    if (season == '2007/2008' or season == '07/08'):
        return 16
    if (season == '2006/2007' or season == '06/07'):
        return 17
    if (season == '2005/2006' or season == '05/06'):
        return 18
    if (season == '2004/2005' or season == '04/05'):
        return 19
    if (season == '2003/2004' or season == '03/04'):
        return 20
    if (season == '2002/2003' or season == '02/03'):
        return 21
    if (season == '2001/2002' or season == '01/02'):
        return 22
    if (season == '2000/2001' or season == '00/01'):
        return 23
    if (season == '1999/2000' or season == '99/00'):
        return 24
    if (season == '1998/1999' or season == '98/99'):
        return 25
    if (season == '1997/1998' or season == '97/98'):
        return 26
    if (season == '1996/1997' or season == '96/97'):
        return 27
    if (season == '1995/1996' or season == '95/96'):
        return 28
    if (season == '1994/1995' or season == '94/95'):
        return 29
    if (season == '1993/1994' or season == '93/94'):
        return 30
    if (season == '1992/1993' or season == '92/93'):
        return 31
    if (season == '1991/1992' or season == '91/92'):
        return 32
    if (season == '1990/1991' or season == '90/91'):
        return 33

def prepareMainDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('/home/aleix/Desktop/tfg/chromedriver',options=options)
    return driver

def translateReferees(referees):
    
    referee_list = []
    for referee in referees:
        nombre = referee.split(',')[1].strip()
        apellido = referee.split(',')[0].strip()
        referee_list.append(nombre + " "  +apellido)
   
    return referee_list

def translateMinutes(time):
    if (time == ''):
        return 0
        
    time = time.split(':')
    minutes = int(time[0])
    seconds = int(time[1])
    return(minutes*60 + seconds)

def translateName(name):
    first_name = name.split(',')[1]
    second_name = name.split(',')[0]

    name_complete = (first_name + " "+ second_name) 
    return name_complete.strip()

def translateStarter(symbol):
    if (symbol == '*'):
        return True
    else:
        return False