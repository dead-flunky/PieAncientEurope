# StartingPointsUtil
# MODDER READ THIS:
# You do not have to change anything in this file
# all changes have to be done in the CvEventManager.
# This file just has to be in the same folder like the CvEventManager.py.

from CvPythonExtensions import (CyGlobalContext, CyMap,
                                UnitAITypes, DirectionTypes,
                                CyEngine)


# import sys
# import CvUtil
gc = CyGlobalContext()
SpawnCivList = []
BarbCityList = []
UsedValidCivList = []

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range


def PlaceBarbarianCities(BarbCityList, Debugging):
    """
    place barbarian cities

    Parameters
    ----------
    BarbCityList : array-like
        DESCRIPTION.
    Debugging : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    pBarb = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    eWarrior = gc.getInfoTypeForString("UNIT_WARRIOR")
    for BarbCity in BarbCityList:
        iX = BarbCity.CityX
        iY = BarbCity.CityY
        pCity = pBarb.initCity(iX, iY)
        pCity.setName(BarbCity.CityName, 0)
        pCity.setPopulation(BarbCity.CityPopulation)
        for _ in xrange(BarbCity.CityNumDefenders):
            pBarb.initUnit(eWarrior, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def FlushVisibleArea():
    """
    makes the old starting positions invisible for the teams

    Returns
    -------
    None.

    """

    iMaxX = CyMap().getGridWidth()
    iMaxY = CyMap().getGridHeight()
    iMaxTeam = gc.getMAX_CIV_TEAMS()
    for iX in xrange(iMaxX):
        for iY in xrange(iMaxY):
            pPlot = CyMap().plot(iX, iY)
            for iTeams in xrange(iMaxTeam):
                if not pPlot.isVisible(iTeams, False):
                    pPlot.setRevealed(iTeams, False, False, iTeams)


def AddCoordinateSignsToMap():
    """
    adds signs with the coordinates to the map so that potential starting positions can easier be modified

    Returns
    -------
    None.

    """

    iHumanPlayer = -1
    for iCivs in xrange(gc.getMAX_CIV_PLAYERS()):
        pPlayer = gc.getPlayer(iCivs)
        if pPlayer.isHuman():
            iHumanPlayer = iCivs
            break
    for iX in xrange(CyMap().getGridWidth()):
        for iY in xrange(CyMap().getGridHeight()):
            pPlot = CyMap().plot(iX, iY)
            PrintString = "X = "+str(iX)+" Y = "+str(iY)
            CyEngine().addSign(pPlot, iHumanPlayer, PrintString)


def CutString(string):
    """
    generic string cutting function
    first < and > at the end are cut of, then the other
    > and < are searched, and what is between is used as value

    Parameters
    ----------
    string : string
        String starting with < and ending with >.

    Returns
    -------
    string
        Part of the input string between the first pair of '<' and '>'
        inside the outermost.

    """
    #

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
