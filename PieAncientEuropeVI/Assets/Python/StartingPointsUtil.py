# StartingPointsUtil
# MODDER READ THIS:
# You do not have to change anything in this file
# all changes have to be done in the CvEventManager.
# This file just has to be in the same folder like the CvEventManager.py.

from CvPythonExtensions import *
import sys
import CvUtil
gc = CyGlobalContext()
SpawnCivList = []
BarbCityList = []
UsedValidCivList = []

# place barbarian cities
def PlaceBarbarianCities(BarbCityList, Debugging):
    pBarb = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for BarbCity in BarbCityList:
        iX = BarbCity.CityX
        iY = BarbCity.CityY
        pCity = pBarb.initCity(iX, iY)
        pCity.setName(BarbCity.CityName, 0)
        pCity.setPopulation(BarbCity.CityPopulation)
        eWarrior = gc.getInfoTypeForString("UNIT_WARRIOR")
        for i in range(BarbCity.CityNumDefenders):
            pBarb.initUnit(eWarrior, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# makes the old starting positions invisible for the teams
def FlushVisibleArea():
    iMaxX = CyMap().getGridWidth()
    iMaxY = CyMap().getGridHeight()
    iMaxTeam = gc.getMAX_CIV_TEAMS()
    for iX in xrange(iMaxX):
        for iY in xrange(iMaxY):
            pPlot = CyMap().plot(iX, iY)
            for iTeams in xrange(iMaxTeam):
                if not pPlot.isVisible(iTeams, False):
                    pPlot.setRevealed(iTeams, False, False, iTeams)

# adds signs with the coordinates to the map
# so that potential starting positions can easier be modified
def AddCoordinateSignsToMap():
    iMaxX = CyMap().getGridWidth()
    iMaxY = CyMap().getGridHeight()
    iMaxPlayer = gc.getMAX_CIV_PLAYERS()
    iHumanPlayer = -1
    for iCivs in xrange(iMaxPlayer):
        pPlayer = gc.getPlayer(iCivs)
        if pPlayer.isHuman():
            iHumanPlayer = iCivs
            break
    for iX in xrange(iMaxX):
        for iY in xrange(iMaxY):
            pPlot = CyMap().plot(iX, iY)
            PrintString = "X = "+str(iX)+" Y = "+str(iY)
            CyEngine().addSign(pPlot, iHumanPlayer, PrintString)

# generic string cutting function
# first < and > at the end are cut of, then the other
# > and < are searched, and what is between is used as value
def CutString(string):
    string = str(string)
    string = string.strip()
    string = string[2:-1]
    BeginPos = -1
    EndPos = -1
    for i in xrange(len(string)):
        if string[i] == ">":
            BeginPos = i
        elif string[i] == "<":
            EndPos = i
            break
    else:
        return "-1"
    NewString = string[BeginPos+1:EndPos]
    return str(NewString)

class SpawningCiv:
    def __init__(self):
        self.CivString = 0
        self.SpawnX = []
        self.SpawnY = []
        self.timesUsed = 0

class BarbarianCity:
    def __init__(self):
        self.CityName = 0
        self.CityX = 0
        self.CityY = 0
        self.CityPopulation = 1
        self.CityNumDefenders = 0
