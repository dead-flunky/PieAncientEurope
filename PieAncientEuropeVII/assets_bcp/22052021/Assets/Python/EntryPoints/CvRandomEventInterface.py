# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvRandomEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
import CvUtil
from CvPythonExtensions import *
from EventSigns import placeLandmark # K-Mod
from operator import itemgetter # K-Mod (used to avoid OOS when sorting)
import CvEventInterface
import PAE_City

gc = CyGlobalContext()
localText = CyTranslator()


######## HOLY MOUNTAIN ###########

def getHelpHolyMountain1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    szHelp = ""

    map = gc.getMap()
    iMinPoints = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers() / 2

    iBuilding = -1
    iReligion = gc.getPlayer(kTriggeredData.ePlayer).getStateReligion()

    if iReligion != -1:
        for i in range(gc.getNumBuildingInfos()):
            if gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo, gc.getNumSpecialBuildingInfos(), "SPECIALBUILDING_TEMPLE"):
                if gc.getBuildingInfo(i).getReligionType() == iReligion:
                    iBuilding = i
                    break

        if iBuilding != -1:
            szHelp = localText.getText("TXT_KEY_EVENT_HOLY_MOUNTAIN_HELP", ( gc.getBuildingInfo(iBuilding).getTextKey(), gc.getBuildingInfo(iBuilding).getTextKey(), iMinPoints))

    return szHelp

def canTriggerHolyMountain(argsList):
    kTriggeredData = argsList[0]
    map = gc.getMap()

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if plot.getOwner() == -1:
        return true

    return false

def expireHolyMountain1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if plot is None:
        return true

    if plot.getOwner() != kTriggeredData.ePlayer and plot.getOwner() != -1:
        # for PAE and the black fog of war
        CvUtil.removeScriptData(plot,"H")
        return true

    return false

def canTriggerHolyMountainDone(argsList):

    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    if kOrigTriggeredData is None:
        return false

    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)
    if plot is None:
        return false

    if plot.getOwner() != kTriggeredData.ePlayer:
        return false

    # for PAE and the black fog of war
    CvUtil.removeScriptData(plot,"H")

    return true

def canTriggerHolyMountainRevealed(argsList):

    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    if kOrigTriggeredData is None:
        return false

    iNumPoints = 0

    for i in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(i).getReligionType() == kOrigTriggeredData.eReligion:
            #if (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),"SPECIALBUILDING_CHRISTIAN_MONASTERY")):
            #  iNumPoints += 2 * player.countNumBuildings(i)
            if gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),"SPECIALBUILDING_TEMPLE"):
                iNumPoints += player.countNumBuildings(i)

    if player.countNumBuildings(gc.getInfoTypeForString("BUILDING_ORACLE2")) > 0:
        iNumPoints = iNumPoints * 2
    if player.countNumBuildings(gc.getInfoTypeForString("BUILDING_ORACLE")) > 0:
        iNumPoints = iNumPoints * 2

    if iNumPoints < gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2:
        return false

    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)
    if plot is None:
        return false

    plot.setRevealed(player.getTeam(), true, true, -1)
    # for PAE and the black fog of war
    CvUtil.addScriptData(plot,"H","X")

    if kTriggeredData.ePlayer == gc.getGame().getActivePlayer():
        CyCamera().JustLookAtPlot(CyMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY))

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return true

def doHolyMountainRevealed(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    if kTriggeredData.ePlayer == gc.getGame().getActivePlayer():
        CyCamera().JustLookAtPlot( CyMap().plot( kTriggeredData.iPlotX, kTriggeredData.iPlotY ) )

    return 1

######## MARATHON ###########

def canTriggerMarathon(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    team = gc.getTeam(player.getTeam())

    if team.AI_getAtWarCounter(otherPlayer.getTeam()) == 1:
        (loopUnit, iter) = otherPlayer.firstUnit(false)
        while loopUnit:
            plot = loopUnit.plot()
            if not plot.isNone():
                if plot.getOwner() == kTriggeredData.ePlayer:
                    return true
            (loopUnit, iter) = otherPlayer.nextUnit(iter, false)

    return false

######## WEDDING FEUD ###########

def doWeddingFeud2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasReligion(kTriggeredData.eReligion):
            loopCity.changeHappinessTimer(30)
        (loopCity, iter) = player.nextCity(iter, false)

    return 1

def getHelpWeddingFeud2(argsList):
    iEvent = argsList[0]
    event = gc.getEventInfo(iEvent)
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_2_HELP", (gc.getDefineINT("TEMP_HAPPY"), 30, religion.getChar()))

    return szHelp

def canDoWeddingFeud3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getGold() - 10 * player.getNumCities() < 0:
        return false

    return true


def doWeddingFeud3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iLoopPlayer)
        if loopPlayer.isAlive() and loopPlayer.getStateReligion() == player.getStateReligion():
            loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
            player.AI_changeAttitudeExtra(iLoopPlayer, 1)

    if gc.getTeam(destPlayer.getTeam()).canDeclareWar(player.getTeam()):
        if destPlayer.isHuman():
            # this works only because it's a single-player only event
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
            popupInfo.setText(localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_OTHER_3", (gc.getReligionInfo(kTriggeredData.eReligion).getAdjectiveKey(), player.getCivilizationShortDescriptionKey())))
            popupInfo.setData1(kTriggeredData.eOtherPlayer)
            popupInfo.setData2(kTriggeredData.ePlayer)
            popupInfo.setPythonModule("CvRandomEventInterface")
            popupInfo.setOnClickedPythonCallback("weddingFeud3Callback")
            popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
            popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
            popupInfo.addPopup(kTriggeredData.eOtherPlayer)
        else:
            gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)

    return 1


def weddingFeud3Callback(argsList):
    iButton = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    if iButton == 0:
        destPlayer = gc.getPlayer(iData1)
        player = gc.getPlayer(iData2)
        gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)

    return 0

def getHelpWeddingFeud3(argsList):
    iEvent = argsList[0]
    event = gc.getEventInfo(iEvent)
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_HELP", (1, religion.getChar()))

    return szHelp

######## SPICY ###########

def canTriggerSpicy(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpice = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_SPICES')
    iHappyBonuses = 0
    bSpices = false
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0 :
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 4:
                    return false
            if i == iSpice:
                return false

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iSpice, false):
        return false

    return true

def doSpicy2(argsList):
#  need this because plantations are notmally not allowed unless there are already spices
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if not plot.isNone():
        plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_PLANTATION'))

    return 1

def getHelpSpicy2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iPlantation = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_PLANTATION')
    szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iPlantation).getTextKey(), ))

    return szHelp

######## BABY BOOM ###########

def canTriggerBabyBoom(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    if team.getAtWarCount(true) > 0:
        return false

    for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
        if iLoopTeam != player.getTeam():
            if team.AI_getAtPeaceCounter(iLoopTeam) == 1:
                return true

    return false

######## BARD TALE ###########

def applyBardTale3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    player.changeGold(-10 * player.getNumCities())

def canApplyBardTale3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getGold() - 10 * player.getNumCities() < 0:
        return false

    return true


def getHelpBardTale3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    szHelp = localText.getText("TXT_KEY_EVENT_GOLD_LOST", (10 * player.getNumCities(), ))

    return szHelp

######## BROTHERS IN NEED ###########

def canTriggerBrothersInNeed(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not player.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
        return false

    listResources = []
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IVORY'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_ZINN'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_BRONZE'))

    bFound = false
    for iResource in listResources:
        if player.getNumTradeableBonuses(iResource) > 1 and otherPlayer.getNumAvailableBonuses(iResource) <= 0:
            bFound = true
            break

    if not bFound:
        return false

    for iTeam in range(gc.getMAX_CIV_TEAMS()):
        if iTeam != player.getTeam() and iTeam != otherPlayer.getTeam() and gc.getTeam(iTeam).isAlive():
            if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(player.getTeam()):
                return true

    return false

def canDoBrothersInNeed1(argsList):
    kTriggeredData = argsList[1]
    newArgs = (kTriggeredData, )

    return canTriggerBrothersInNeed(newArgs)

######## HURRICANE ###########

def canTriggerHurricaneCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return false

    if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return false

    if city.plot().getLatitude() <= 0:
        return false

    if city.getPopulation() < 2:
        return false

    return true

def canApplyHurricane1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    listBuildings = []
    for iBuilding in range(gc.getNumBuildingInfos()):
        if city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
            listBuildings.append(iBuilding)

    return len(listBuildings) > 0

def canApplyHurricane2(argsList):
    return not canApplyHurricane1(argsList)


def applyHurricane1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    listCheapBuildings = []
    listExpensiveBuildings = []
    for iBuilding in range(gc.getNumBuildingInfos()):
        if city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
            listCheapBuildings.append(iBuilding)
        if city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
            listExpensiveBuildings.append(iBuilding)

    if listCheapBuildings:
        iBuilding = listCheapBuildings[gc.getGame().getSorenRandNum(len(listCheapBuildings), "Hurricane event cheap building destroyed")]
        szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
        CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), true, true)
        city.setNumRealBuilding(iBuilding, 0)

    if listExpensiveBuildings:
        iBuilding = listExpensiveBuildings[gc.getGame().getSorenRandNum(len(listExpensiveBuildings), "Hurricane event expensive building destroyed")]
        szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
        CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), true, true)
        city.setNumRealBuilding(iBuilding, 0)


######## CYCLONE ###########

def canTriggerCycloneCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return false

    if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return false

    if city.plot().getLatitude() >= 0:
        return false

    return true

######## MONSOON ###########

def canTriggerMonsoonCity(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return false

    if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
        return false

    iJungleType = CvUtil.findInfoTypeNum(gc.getFeatureInfo, gc.getNumFeatureInfos(),'FEATURE_JUNGLE')

    for iDX in range(-3, 4):
        for iDY in range(-3, 4):
            pLoopPlot = plotXY(city.getX(), city.getY(), iDX, iDY)
            if not pLoopPlot.isNone() and pLoopPlot.getFeatureType() == iJungleType:
                return true

    return false

######## CHAMPION ###########

def canTriggerChampion(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    if team.getAtWarCount(true) > 0:
        return false

    return true

def canTriggerChampionUnit(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iUnit = argsList[2]

    player = gc.getPlayer(ePlayer)
    unit = player.getUnit(iUnit)

    if unit.isNone():
        return false

    if unit.getDamage() > 0:
        return false

    if unit.getExperience() < 3:
        return false

    iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
    if unit.isHasPromotion(iLeadership):
        return false

    return true

def applyChampion(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')

    unit.setHasPromotion(iLeadership, true)

def getHelpChampion(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')

    szHelp = localText.getText("TXT_KEY_EVENT_CHAMPION_HELP", (unit.getNameKey(), gc.getPromotionInfo(iLeadership).getTextKey()))

    return szHelp

######## GOLD RUSH ###########

def canTriggerGoldRush(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    iIndustrial = CvUtil.findInfoTypeNum(gc.getEraInfo,gc.getNumEraInfos(),'ERA_MEDIEVAL')

    if player.getCurrentEra() != iIndustrial:
        return false

    return true

######## INFLUENZA ###########

def canTriggerInfluenza(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iKlassik = CvUtil.findInfoTypeNum(gc.getEraInfo,gc.getNumEraInfos(),'ERA_MEDIEVAL')

    if player.getCurrentEra() <= iKlassik:
        return false

#    iMedicine1 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE1')
#    iMedicine2 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE2')
#    iMedicine3 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE3')
    iMedicine4 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_HEILKUNDE')

    if team.isHasTech(iMedicine4):
        szBuffer = localText.getText("TXT_KEY_EVENT_INFLUENZA_TEAM_HEILKUNDE", ("", ))
        CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_GREEN"), 0, 0, false, false)
        return false

    return true

def applyInfluenza2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    eventCity = player.getCity(kTriggeredData.iCityId)

    iMaxCities = player.getNumCities()

    iNumCities = 2 + gc.getGame().getSorenRandNum(iMaxCities, "Influenza event number of cities")

    listCities = []
    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.getPopulation() > 2:
            iDistance = plotDistance(eventCity.getX(), eventCity.getY(), loopCity.getX(), loopCity.getY())
            if iDistance > 0:
                listCities.append((iDistance, loopCity))
        (loopCity, iter) = player.nextCity(iter, false)

    #listCities.sort()
    #k-mod
	listCities.sort(key=itemgetter(0)) # K-Mod. Sorting by pointers can cause OOS.

    if iNumCities > len(listCities):
        iNumCities = len(listCities)

    for i in range(iNumCities):
        (iDist, loopCity) = listCities[i]
        loopCity.changePopulation(-2)
        szBuffer = localText.getText("TXT_KEY_EVENT_INFLUENZA_HIT_CITY", (loopCity.getNameKey(), ))
        CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_RED"), loopCity.getX(), loopCity.getY(), true, true)


def getHelpInfluenza2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_INFLUENZA_HELP_2", (2, ))

    return szHelp

######## ANTELOPE ###########

def canTriggerAntelope(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER')
    iHappyBonuses = 0
    bDeer = false
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0 :
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 5:
                    return false
            if i == iDeer:
                return false

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iDeer, false):
        return false

    return true

def doAntelope2(argsList):
    # Need this because camps are not normally allowed unless there is already deer.
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if not plot.isNone():
        plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP'))

    return 1

def getHelpAntelope2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iCamp = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP')
    szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iCamp).getTextKey(), ))

    return szHelp

######## HIYOSILVER ###########

def canTriggerHiyoSilver(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSilver = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_SILVER')
    iHappyBonuses = 0
    bSilver = false
    for i in range(gc.getNumBonusInfos()):
        bonus = gc.getBonusInfo(i)
        iNum = player.getNumAvailableBonuses(i)
        if iNum > 0 :
            if bonus.getHappiness() > 0:
                iHappyBonuses += 1
                if iHappyBonuses > 5:
                    return false
            if i == iSilver:
                return false

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.canHaveBonus(iSilver, false):
        return false

    return true

######## WININGMONKS ###########

def canTriggerWiningMonks(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getNumAvailableBonuses(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_WINE')) > 0:
        return false

    return true


def doWiningMonks2(argsList):
#  Need this because wineries are not normally allowed unless there is already wine.
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    if not plot.isNone():
        plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_WINERY'))

    return 1

def getHelpWiningMonks2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iImp = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_WINERY')
    szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iImp).getTextKey(), ))

    return szHelp

######## ANCIENT OLYMPICS ###########

def doAncientOlympics2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    for j in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(j)
        if loopPlayer is not None and not loopPlayer.isNone():
            if j != kTriggeredData.ePlayer and loopPlayer.isAlive() and not loopPlayer.isMinorCiv():
                for i in range(map.numPlots()):
                    plot = map.plotByIndex(i)
                    if not plot.isWater() and plot.getOwner() == kTriggeredData.ePlayer and plot.isAdjacentPlayer(j, true):
                        loopPlayer.AI_changeMemoryCount(kTriggeredData.ePlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1)
                        break

    return 1

def getHelpAncientOlympics2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_ANCIENTOLYMPICS_HELP_2", ( 1, ))

    return szHelp

######## HEROIC_GESTURE ###########

def canTriggerHeroicGesture(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not gc.getTeam(destPlayer.getTeam()).canChangeWarPeace(player.getTeam()):
        return false

    if gc.getTeam(destPlayer.getTeam()).AI_getWarSuccess(player.getTeam()) <= 0:
        return false

    if gc.getTeam(player.getTeam()).AI_getWarSuccess(destPlayer.getTeam()) <= 0:
        return false

    # K-Mod. an ugly hack to prevent the AI from signing a peace deal when it really doesn't want to.
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_PEACE_TREATY

	if player.getTradeDenial(kTriggeredData.eOtherPlayer, tradeData) != DenialTypes.NO_DENIAL:
		return false

	if destPlayer.getTradeDenial(kTriggeredData.ePlayer, tradeData) != DenialTypes.NO_DENIAL:
		return false
	# K-Mod end

	return true

def doHeroicGesture2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if destPlayer.isHuman():
        # this works only because it's a single-player only event
        popupInfo = CyPopupInfo()
        popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popupInfo.setText(localText.getText("TXT_KEY_EVENT_HEROIC_GESTURE_OTHER_3", (player.getCivilizationAdjective(1), )))
        popupInfo.setData1(kTriggeredData.eOtherPlayer)
        popupInfo.setData2(kTriggeredData.ePlayer)
        popupInfo.setPythonModule("CvRandomEventInterface")
        popupInfo.setOnClickedPythonCallback("heroicGesture2Callback")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
        popupInfo.addPopup(kTriggeredData.eOtherPlayer)
    else:
        destPlayer.forcePeace(kTriggeredData.ePlayer)
        destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
        player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

    return

def heroicGesture2Callback(argsList):
    iButton = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    if iButton == 0:
        destPlayer = gc.getPlayer(iData1)
        player = gc.getPlayer(iData2)
        destPlayer.forcePeace(iData2)
        destPlayer.AI_changeAttitudeExtra(iData2, 1)
        player.AI_changeAttitudeExtra(iData1, 1)

    return 0

def getHelpHeroicGesture2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    # Get help text
    szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()))

    return szHelp

######## GREAT_MEDIATOR ###########

def canTriggerGreatMediator(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not gc.getTeam(player.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
        return false

    if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
        return false

    # K-Mod. an ugly hack to prevent the AI from signing a peace deal when it really doesn't want to.
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_PEACE_TREATY

	if player.getTradeDenial(kTriggeredData.eOtherPlayer, tradeData) != DenialTypes.NO_DENIAL:
		return false

	if destPlayer.getTradeDenial(kTriggeredData.ePlayer, tradeData) != DenialTypes.NO_DENIAL:
		return false
	# K-Mod end

	return true

def doGreatMediator2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if destPlayer.isHuman():
        # this works only because it's a single-player only event
        popupInfo = CyPopupInfo()
        popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
        popupInfo.setText(localText.getText("TXT_KEY_EVENT_GREAT_MEDIATOR_OTHER_3", (player.getCivilizationAdjective(1), )))
        popupInfo.setData1(kTriggeredData.eOtherPlayer)
        popupInfo.setData2(kTriggeredData.ePlayer)
        popupInfo.setPythonModule("CvRandomEventInterface")
        popupInfo.setOnClickedPythonCallback("greatMediator2Callback")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
        popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
        popupInfo.addPopup(kTriggeredData.eOtherPlayer)
    else:
        gc.getTeam(player.getTeam()).makePeace(destPlayer.getTeam())
        destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
        player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

    return

def greatMediator2Callback(argsList):
    iButton = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    if iButton == 0:
        destPlayer = gc.getPlayer(iData1)
        player = gc.getPlayer(iData2)
        gc.getTeam(destPlayer.getTeam()).makePeace(player.getTeam())
        destPlayer.AI_changeAttitudeExtra(iData2, 1)
        player.AI_changeAttitudeExtra(iData1, 1)

    return 0

def getHelpGreatMediator2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    # Get help text
    szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()))

    return szHelp

######## ANCIENT_TEXTS ###########

def doAncientTexts2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
            loopTeam = gc.getTeam(loopPlayer.getTeam())
            if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
                loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)

    return

def getHelpAncientTexts2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_TRIGGER_ANCIENT_TEXTS_1", (1, ))

    return szHelp

######## THE_HUNS ###########

def canTriggerTheHuns(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Horseback Riding.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_HORSEBACK_RIDING_3')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false


    # # Can we build the counter unit?
    # iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SPEARMAN')
    # iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
    # if iCounterUnit == -1:
        # return false

    # (loopCity, iter) = player.firstCity(false)
    # bFound = false
    # while loopCity:
        # if loopCity.canTrain(iCounterUnit, false, false):
            # bFound = true
            # break

        # (loopCity, iter) = player.nextCity(iter, false)

    # if not bFound:
        # return false


    #  Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false


def getHelpTheHuns1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_HUNS_HELP_1", ())

    return szHelp


def applyTheHuns1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Hun event location")])

    iNumUnits  = map.getWorldSize() + 5

    iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_HORSE_ARCHER_SCYTHS')
    iUnitType2 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_MONGOL_KESHIK')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType1, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
        barbPlayer.initUnit(iUnitType2, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)

######## THE_VANDALS ###########

def canTriggerTheVandals(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Buergersoldaten.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_BUERGERSOLDATEN')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_AXEMAN')
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
    if iCounterUnit == -1:
        return false

    (loopCity, iter) = player.firstCity(false)
    bFound = false
    while(loopCity):
        if (loopCity.canTrain(iCounterUnit, false, false)):
            bFound = true
            break

        (loopCity, iter) = player.nextCity(iter, false)

    if not bFound:
        return false

    #  Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false


def getHelpTheVandals1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_VANDALS_HELP_1", ())

    return szHelp


def applyTheVandals1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Vandal event location")])

    iNumUnits  = map.getWorldSize() + 5

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_CELTIC_GALLIC_WARRIOR')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)


######## THE_GOTHS ###########

def canTriggerTheGoths(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Mathematics.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_MATHEMATICS')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    #   At least one civ on the board must know Iron Working.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_KETTENPANZER')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    #  Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false


def getHelpTheGoths1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_GOTHS_HELP_1", ())

    return szHelp


def applyTheGoths1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Goth event location")])

    iNumUnits  = map.getWorldSize() + 5

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_STAMMESFUERST')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)


######## THE_PHILISTINES ###########

def canTriggerThePhilistines(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Monotheism.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_MONOTHEISM')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    #   At least one civ on the board must know Breitschwert und Schild.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_BEWAFFNUNG4')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_AXEMAN')
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
    if iCounterUnit == -1:
        return false

    (loopCity, iter) = player.firstCity(false)
    bFound = false
    while loopCity:
        if loopCity.canTrain(iCounterUnit, false, false):
            bFound = true
            break

        (loopCity, iter) = player.nextCity(iter, false)

    if not bFound:
        return false

    #  Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false


def getHelpThePhilistines1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_PHILISTINES_HELP_1", ())

    return szHelp


def applyThePhilistines1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Philistine event location")])

    iNumUnits  = map.getWorldSize() + 3

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PHILISTER')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)


######## THE_VEDIC_ARYANS ###########

def canTriggerTheVedicAryans(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Polytheism.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_VASALLENTUM')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    #   At least one civ on the board must know Archery.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_ARMOR')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    # Can we build the counter unit?
    iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_ARCHER')
    iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
    if iCounterUnit == -1:
        return false

    (loopCity, iter) = player.firstCity(false)
    bFound = false
    while loopCity:
        if loopCity.canTrain(iCounterUnit, false, false):
            bFound = true
            break

        (loopCity, iter) = player.nextCity(iter, false)

    if not bFound:
        return false

    #  Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false


def getHelpTheVedicAryans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THE_VEDIC_ARYANS_HELP_1", ())

    return szHelp


def applyTheVedicAryans1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if not listPlots:
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Vedic Aryan event location")])

    iNumUnits  = map.getWorldSize() + 4

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_RADSCHA')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)

######## SECURITY_TAX ###########

def canTriggerSecurityTax(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iWalls = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_WALLS')
    if player.getNumCities() > player.getBuildingClassCount(iWalls):
        return false

    return true


######## LITERACY ###########

def canTriggerLiteracy(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
    if player.getNumCities() > player.getBuildingClassCount(iLibrary):
        return false

    return true

######## HORSE WHISPERING ###########

def canTriggerHorseWhispering(argsList):
    kTriggeredData = argsList[0]

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    return true

def getHelpHorseWhispering1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    iNumStables = gc.getMap().getWorldSize() + 3
    szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_HELP", (iNumStables, ))

    return szHelp

def canTriggerHorseWhisperingDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iStable = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_STABLE')
    if gc.getMap().getWorldSize() + 3 > player.getBuildingClassCount(iStable):
        return false

    return true

def getHelpHorseWhisperingDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    iNumUnits = gc.getMap().getWorldSize() + 2
    szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_DONE_HELP_1", (iNumUnits, ))

    return szHelp

def applyHorseWhisperingDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    map = gc.getMap()
    plot = map.plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    iNumUnits = gc.getMap().getWorldSize() + 2
    iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_HORSE_ARCHER')
    iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)

    if iUnitType != -1:
        for i in range(iNumUnits):
            player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

######## CLASSIC LITERATURE ###########

def canTriggerClassicLiterature(argsList):
    kTriggeredData = argsList[0]

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    return true

def getHelpClassicLiterature1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iLibrariesRequired = gc.getMap().getWorldSize() + 2

    szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_HELP_1", (iLibrariesRequired, ))

    return szHelp


def canTriggerClassicLiteratureDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
    iBuildingsRequired = gc.getMap().getWorldSize() + 2
    if iBuildingsRequired > player.getBuildingClassCount(iLibrary):
        return false

    return true

def getHelpClassicLiteratureDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_DONE_HELP_2", ( ))

    return szHelp

def canApplyClassicLiteratureDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), 'ERA_MEDIEVAL')

    for iTech in range(gc.getNumTechInfos()):
        if gc.getTechInfo(iTech).getEra() == iEraAncient and player.canResearch(iTech, false):
            return true

    return false

def applyClassicLiteratureDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), 'ERA_MEDIEVAL')

    listTechs = []
    for iTech in range(gc.getNumTechInfos()):
        if gc.getTechInfo(iTech).getEra() == iEraAncient and player.canResearch(iTech, false):
            listTechs.append(iTech)

    if listTechs:
        iTech = listTechs[gc.getGame().getSorenRandNum(len(listTechs), "Classic Literature Event Tech selection")]
        gc.getTeam(player.getTeam()).setHasTech(iTech, true, kTriggeredData.ePlayer, true, true)

def getHelpClassicLiteratureDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpecialist = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), 'SPECIALIST_SCIENTIST', )
    iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

    szCityName = u""
    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasBuilding(iGreatLibrary):
            szCityName = loopCity.getNameKey()
            break

        (loopCity, iter) = player.nextCity(iter, false)

    szHelp = localText.getText("TXT_KEY_EVENT_FREE_SPECIALIST", (1, gc.getSpecialistInfo(iSpecialist).getTextKey(), szCityName))

    return szHelp

def canApplyClassicLiteratureDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

    (loopCity, iter) = player.firstCity(false)
    while(loopCity):
        if (loopCity.isHasBuilding(iGreatLibrary)):
            return true

        (loopCity, iter) = player.nextCity(iter, false)

    return false

def applyClassicLiteratureDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpecialist = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), 'SPECIALIST_SCIENTIST', )
    iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasBuilding(iGreatLibrary):
            loopCity.changeFreeSpecialistCount(iSpecialist, 1)
            return

        (loopCity, iter) = player.nextCity(iter, false)

######## MASTER BLACKSMITH ###########

def canTriggerMasterBlacksmith(argsList):
    kTriggeredData = argsList[0]

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    return true

def getHelpMasterBlacksmith1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iRequired = gc.getMap().getWorldSize() + 4

    szHelp = localText.getText("TXT_KEY_EVENT_MASTER_BLACKSMITH_HELP_1", (iRequired, player.getCity(kTriggeredData.iCityId).getNameKey()))

    return szHelp

def expireMasterBlacksmith1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)
    if city is None or city.getOwner() != kTriggeredData.ePlayer:
        return true

    return false

def canTriggerMasterBlacksmithDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iForge = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_FORGE')
    iBuildingsRequired = gc.getMap().getWorldSize() + 4
    if iBuildingsRequired > player.getBuildingClassCount(iForge):
        return false

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    city = player.getCity(kOrigTriggeredData.iCityId)
    if city is None or city.getOwner() != kTriggeredData.ePlayer:
        return false

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId

    return true

def canApplyMasterBlacksmithDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
    city = player.getCity(kTriggeredData.iCityId)

    if city is None:
        return false

    map = gc.getMap()
    iBestValue = map.getGridWidth() + map.getGridHeight()
    bestPlot = None
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == kTriggeredData.ePlayer and plot.canHaveBonus(iBonus, false):
            iValue = plotDistance(city.getX(), city.getY(), plot.getX(), plot.getY())
            if iValue < iBestValue:
                iBestValue = iValue
                bestPlot = plot

    if bestPlot is None:
        return false

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = bestPlot.getX()
    kActualTriggeredDataObject.iPlotY = bestPlot.getY()

    return true

def applyMasterBlacksmithDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    city = player.getCity(kTriggeredData.iCityId)

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
    plot.setBonusType(iBonus)

    szBuffer = localText.getText("TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", (gc.getBonusInfo(iBonus).getTextKey(), city.getNameKey()))
    CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), gc.getInfoTypeForString("COLOR_WHITE"), plot.getX(), plot.getY(), true, true)

def canApplyMasterBlacksmithDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getStateReligion() == -1:
        return false

    return true

######## NATIONAL SPORTS LEAGUE ###########

def canTriggerSportsLeague(argsList):
    kTriggeredData = argsList[0]

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    return true
def getHelpSportsLeague1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iRequired = gc.getMap().getWorldSize() + 4
    iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STATUE_OF_ZEUS')

    szHelp = localText.getText("TXT_KEY_EVENT_SPORTS_LEAGUE_HELP_1", (iRequired, gc.getBuildingInfo(iBuilding).getTextKey()))

    return szHelp

def canTriggerSportsLeagueDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_STADION')
    iBuildingsRequired = gc.getMap().getWorldSize() + 4
    if iBuildingsRequired > player.getBuildingClassCount(iBuilding):
        return false

    return true

def canApplySportsLeagueDone3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iZeus = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STATUE_OF_ZEUS')

    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasBuilding(iZeus):
            return true

        (loopCity, iter) = player.nextCity(iter, false)

    return false

######## SECRET_KNOWLEDGE ###########

def getHelpSecretKnowledge2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    szHelp = localText.getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+4[ICON_CULTURE]"))

    return szHelp

def applySecretKnowledge2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    city.setBuildingCommerceChange(gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_CULTURE, 4)

######## EXPERIENCED_CAPTAIN ###########

def canTriggerExperiencedCaptain(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    if unit.isNone():
        return false

    if unit.getExperience() < 7:
        return false

    return true

######## GREED ###########

def canTriggerGreed(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not gc.getTeam(player.getTeam()).canChangeWarPeace(otherPlayer.getTeam()):
        return false

    listBonuses = []
    iIron = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON')
    if 0 == player.getNumAvailableBonuses(iIron):
        listBonuses.append(iIron)
    iHorse = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE')
    if 0 == player.getNumAvailableBonuses(iHorse):
        listBonuses.append(iHorse)
    iCopper = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
    if 0 == player.getNumAvailableBonuses(iCopper):
        listBonuses.append(iCopper)
    iZinn = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_ZINN')
    if 0 == player.getNumAvailableBonuses(iZinn):
        listBonuses.append(iZinn)

    map = gc.getMap()
    bFound = false
    listPlots = []
    for iBonus in listBonuses:
        for i in range(map.numPlots()):
            loopPlot = map.plotByIndex(i)
            if loopPlot.getOwner() == kTriggeredData.eOtherPlayer and loopPlot.getBonusType(player.getTeam()) == iBonus and loopPlot.isRevealed(player.getTeam(), false) and not loopPlot.isWater():
                listPlots.append(loopPlot)
                bFound = true
        if bFound:
            break

    if not bFound:
        return false

    plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Greed event plot selection")]

    if -1 == getGreedUnit(player, plot):
        return false

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = plot.getX()
    kActualTriggeredDataObject.iPlotY = plot.getY()

    return true

def getHelpGreed1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    iBonus = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY).getBonusType(player.getTeam())

    iTurns = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()

    szHelp = localText.getText("TXT_KEY_EVENT_GREED_HELP_1", (otherPlayer.getCivilizationShortDescriptionKey(), gc.getBonusInfo(iBonus).getTextKey(), iTurns))

    return szHelp

def expireGreed1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if plot.getOwner() == kTriggeredData.ePlayer or plot.getOwner() == -1:
        return false

    if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent():
        return true

    if plot.getOwner() != kTriggeredData.eOtherPlayer:
        return true

    return false

def canTriggerGreedDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)

    if plot.getOwner() != kOrigTriggeredData.ePlayer:
        return false

    if -1 == getGreedUnit(player, plot):
        return false

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
    kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer

    return true

def getGreedUnit(player, plot):
    iBonus = plot.getBonusType(player.getTeam())
    iBestValue = 0
    iBestUnit = -1
    for iUnitClass in range(gc.getNumUnitClassInfos()):
        iUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClass)
        if iUnit != -1 and player.canTrain(iUnit, false, false) and (gc.getUnitInfo(iUnit).getDomainType() == DomainTypes.DOMAIN_LAND):
            iValue = 0
            if gc.getUnitInfo(iUnit).getPrereqAndBonus() == iBonus:
                iValue = player.AI_unitValue(iUnit, UnitAITypes.UNITAI_ATTACK, plot.area())
            else:
                for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
                    if gc.getUnitInfo(iUnit).getPrereqOrBonuses(j) == iBonus:
                        iValue = player.AI_unitValue(iUnit, UnitAITypes.UNITAI_ATTACK, plot.area())
                        break
            if iValue > iBestValue:
                iBestValue = iValue
                iBestUnit = iUnit

    return iBestUnit


def getHelpGreedDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iNumUnits = gc.getMap().getWorldSize() + 4
    iUnitType = getGreedUnit(player, plot)

    if iUnitType != -1:
        szHelp = localText.getText("TXT_KEY_EVENT_GREED_DONE_HELP_1", (iNumUnits, gc.getUnitInfo(iUnitType).getTextKey()))

    return szHelp

def applyGreedDone1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iUnitType = getGreedUnit(player, plot)
    iNumUnits = gc.getMap().getWorldSize() + 4

    if iUnitType != -1:
        for i in range(iNumUnits):
            player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)


######## WAR CHARIOTS ###########

def canTriggerWarChariots(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eReligion = ReligionTypes(player.getStateReligion())

    return true

def getHelpWarChariots1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getMap().getWorldSize() + 8
    szHelp = localText.getText("TXT_KEY_EVENT_WAR_CHARIOTS_HELP_1", (iNumUnits, ))

    return szHelp

def canTriggerWarChariotsDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getMap().getWorldSize() + 8
    iUnitClassType1 = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CHARIOT')
    iUnitClassType2 = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CHARIOT_ARCHER')
    iUnitClassType3 = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_WAR_CHARIOT')
    if player.getUnitClassCount(iUnitClassType1) + player.getUnitClassCount(iUnitClassType2) + player.getUnitClassCount(iUnitClassType3) < iNumUnits:
        return false

    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion

    return true

def getHelpWarChariotsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpecialist = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), 'SPECIALIST_GREAT_GENERAL', )
    iStall = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STABLE')
    iProvinzpalast = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_PROVINZPALAST')

    szCityName = u""
    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasBuilding(iStall) and loopCity.isHasBuilding(iProvinzpalast):
            szCityName = loopCity.getNameKey()
            break

        (loopCity, iter) = player.nextCity(iter, false)

    szHelp = localText.getText("TXT_KEY_EVENT_FREE_SPECIALIST", (1, gc.getSpecialistInfo(iSpecialist).getTextKey(), szCityName))

    return szHelp

def canApplyWarChariotsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iStall = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STABLE')
    iProvinzpalast = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_PROVINZPALAST')

    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasBuilding(iStall) and loopCity.isHasBuilding(iProvinzpalast):
            return true

        (loopCity, iter) = player.nextCity(iter, false)

    return false

def applyWarChariotsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iSpecialist = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), 'SPECIALIST_GREAT_GENERAL', )
    iStall = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STABLE')
    iProvinzpalast = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_PROVINZPALAST')

    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasBuilding(iStall) and loopCity.isHasBuilding(iProvinzpalast):
            loopCity.changeFreeSpecialistCount(iSpecialist, 1)
            #return # soll jede Stadt mit Provinzpalast und Stall bekommen

        (loopCity, iter) = player.nextCity(iter, false)

######## ELITE SWORDSMEN ###########

def getHelpEliteSwords1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getMap().getWorldSize() + 8
    szHelp = localText.getText("TXT_KEY_EVENT_ELITE_SWORDS_HELP_1", (iNumUnits, ))

    return szHelp

def canTriggerEliteSwordsDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getMap().getWorldSize() + 8
    iUnitClassType1 = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_KURZSCHWERT')
    iUnitClassType2 = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SCHILDTRAEGER')
    iUnitClassType3 = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SWORDSMAN')
    iUnits = player.getUnitClassCount(iUnitClassType1) + player.getUnitClassCount(iUnitClassType2) + player.getUnitClassCount(iUnitClassType3)
    if iUnits < iNumUnits:
        return false

    return true


def canApplyEliteSwordsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_ROYAL')

    if player.isCivic(iCivic):
        return true

    return false

######## WARSHIPS ###########

def canTriggerWarships(argsList):
    kTriggeredData = argsList[0]

    map = gc.getMap()
    iNumWater = 0

    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)

        if plot.isWater():
            iNumWater += 1

        if 100 * iNumWater >= 20 * map.numPlots():
            return true

    return false

def getHelpWarships1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getMap().getWorldSize() + 8

    iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIGHTHOUSE')
    szHelp = localText.getText("TXT_KEY_EVENT_WARSHIPS_HELP_1", (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey()))

    return szHelp

def canTriggerWarshipsDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getMap().getWorldSize() + 8
    iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_TRIREME')

    if player.getUnitClassCount(iUnitClassType) < iNumUnits:
        return false

    return true


def canApplyWarshipsDone2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIGHTHOUSE')
    if player.getBuildingClassCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
        return false

    return true

######## Great Beast ########

def doGreatBeast3(argsList):
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    (loopCity, iter) = player.firstCity(false)
    while loopCity:
        if loopCity.isHasReligion(kTriggeredData.eReligion):
            loopCity.changeHappinessTimer(40)
        (loopCity, iter) = player.nextCity(iter, false)

def getHelpGreatBeast3(argsList):
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_GREAT_BEAST_3_HELP", (gc.getDefineINT("TEMP_HAPPY"), 40, religion.getChar()))

    return szHelp

####### Immigrants ########

def canTriggerImmigrantCity(argsList):
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return false

    if (city.happyLevel() - city.unhappyLevel(0) < 1) or (city.goodHealth() - city.badHealth(true) < 1):
        return false

    if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE) < 5500:
        return false

####### Controversial Philosopher ######

def canTriggerControversialPhilosopherCity(argsList):
    ePlayer = argsList[1]
    iCity = argsList[2]

    player = gc.getPlayer(ePlayer)
    city = player.getCity(iCity)

    if city.isNone():
        return false
    if not city.isCapital():
        return false
    if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) < 3500:
        return false

    return true

######## Preaching Researcher #######

def canTriggerPreachingResearcherCity(argsList):
    iCity = argsList[2]

    player = gc.getPlayer(argsList[1])
    city = player.getCity(iCity)

    if city.isHasBuilding(gc.getInfoTypeForString("BUILDING_GYMNASION")) or city.isHasBuilding(gc.getInfoTypeForString("BUILDING_SCHULE")):
        return true
    return false

######## Dissident Priest (Egyptian event) #######

def canTriggerDissidentPriestCity(argsList):
    iCity = argsList[2]

    player = gc.getPlayer(argsList[1])
    city = player.getCity(iCity)

    if city.isGovernmentCenter():
        return false
    if city.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE) < 3000:
        return false
    if player.getStateReligion() != -1:
        return false

    return true

######## ABRAHAM ###########

def canTriggerAbraham(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ISRAEL"):
        return true
    return false

######## GROSSESAQUEDUCT ###########

def canTriggerGrossesAqueduct(argsList):
    kTriggeredData = argsList[0]

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    return true

def getHelpGrossesAqueduct1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    map = gc.getMap()

    iNumGrossesAqueduct = gc.getMap().getWorldSize() + 4
    szHelp = localText.getText("TXT_KEY_EVENT_GROSSES_AQUEDUCT_HELP", (iNumGrossesAqueduct, ))

    return szHelp

def canTriggerGrossesAqueductDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iGrossesAqueduct = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_AQUEDUCT')
    if gc.getMap().getWorldSize() + 4 > player.getBuildingClassCount(iGrossesAqueduct):
        return false

    return true

######## HUNTER ###########

def canTriggerHunterUnit(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iUnit = argsList[2]

    player = gc.getPlayer(ePlayer)
    unit = player.getUnit(iUnit)

    if unit.isNone():
        return false

    iSentry = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SENTRY')
    if unit.isHasPromotion(iSentry):
        return false

    iWildlife = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_WILDLIFE')
    if unit.isHasPromotion(iWildlife):
        return true

    return false

def applyHunter(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iSentry = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SENTRY')

    unit.setHasPromotion(iSentry, true)

def getHelpHunter(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iSentry = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SENTRY')

    szHelp = localText.getText("TXT_KEY_EVENT_HUNTER_HELP", (unit.getNameKey(), gc.getPromotionInfo(iSentry).getTextKey()))

    return szHelp

######## KILIKIEN ###########

def canTriggerKilikien(argsList):

    kTriggeredData = argsList[0]
    pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
    map = gc.getMap()

#   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

#   At least one civ on the board must know Sailing.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_WARSHIPS2')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

#        Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false

def getHelpKilikien1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_KILIKIEN_HELP_1", ())

    return szHelp

def applyKilikien1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Kilikien event location")])

    iNumUnit1 = map.getWorldSize() + 2

    iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_KILIKIEN')
    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnit1):
        barbPlayer.initUnit(iUnitType1, plot.getX(), plot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH)

######## MOOR ###########

def canTriggerMoor(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    if unit.isNone():
        return false

    iSumpf = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SUMPF1')
    if unit.isHasPromotion(iSumpf):
        return false

    return true

######## MOORPROMO ###########

def canTriggerMoorPromo(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    if unit.isNone():
        return false

    if unit.getExperience() < 5:
        return false

    iSumpf = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SUMPF1')
    if unit.isHasPromotion(iSumpf):
        return false

    return true

def canTriggerMoorPromoUnit(argsList):
    eTrigger = argsList[0]
    ePlayer = argsList[1]
    iUnit = argsList[2]

    player = gc.getPlayer(ePlayer)
    unit = player.getUnit(iUnit)

    if unit.isNone():
        return false

    if unit.getExperience() < 7:
        return false

    iSumpf = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SUMPF1')
    if unit.isHasPromotion(iSumpf):
        return false

    return true

def applyMoorPromo(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iSumpf = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SUMPF1')

    unit.setHasPromotion(iSumpf, true)

def getHelpMoorPromo(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    iSumpf = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_SUMPF1')

    szHelp = localText.getText("TXT_KEY_EVENT_MOORPROMO_HELP", (unit.getNameKey(), gc.getPromotionInfo(iSumpf).getTextKey()))

    return szHelp

######## Leprakolo ###########

def canTriggerLeprakolo(argsList):
    kTriggeredData = argsList[0]

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    return true

def getHelpLeprakolo1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumLeprakolo = gc.getMap().getWorldSize() + 2
    szHelp = localText.getText("TXT_KEY_EVENT_LEPRAKOLO_HELP", (iNumLeprakolo, ))

    return szHelp

def canTriggerLeprakoloDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iLeprakolo = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LEPRAKOLONIE')
    if gc.getMap().getWorldSize() + 2 > player.getBuildingClassCount(iLeprakolo):
        return false

    return true

######## PIRATEN ###########

def canTriggerPiraten(argsList):

    kTriggeredData = argsList[0]
    pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

#   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

#   At least one civ on the board must know Piracy.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_PIRACY')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

#   Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false

def getHelpPiraten1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_PIRATEN_HELP_1", ())

    return szHelp

def applyPiraten1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if 0 == len(listPlots):
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Piraten event location")])

    iNumUnit1 = map.getWorldSize() + 4

    iTech1 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_RUDERER2')
    iTech2 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_RUDERER3')
    iTech3 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_WARSHIPS2')
    if gc.getTeam(pPlayer.getTeam()).isHasTech(iTech3):
        iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PIRAT_LIBURNE')
    elif gc.getTeam(pPlayer.getTeam()).isHasTech(iTech2):
        iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PIRAT_TRIREME')
    elif gc.getTeam(pPlayer.getTeam()).isHasTech(iTech1):
        iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PIRAT_BIREME')
    else:
        iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PIRAT_KONTERE')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnit1):
        barbPlayer.initUnit(iUnitType1, plot.getX(), plot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH)

######## Spartacus ###########

def canTriggerSpartacus(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Mathematics.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_GLADIATOR2')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    #  Find an eligible plot
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == kTriggeredData.ePlayer and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false

def getHelpSpartacus1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_SPARTACUS_HELP_1", ())

    return szHelp

def applySpartacus1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == kTriggeredData.ePlayer and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if not listPlots:
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Spartacus event location")])

    iNumUnits = map.getWorldSize() + 3

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_GLADIATOR')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)

######## TROJA ###########

def doTroja2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iLoopPlayer)
        if loopPlayer.isAlive() and loopPlayer.getStateReligion() == player.getStateReligion():
            loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
            player.AI_changeAttitudeExtra(iLoopPlayer, 2)

    return 1

def getHelpTroja2(argsList):
    iEvent = argsList[0]
    event = gc.getEventInfo(iEvent)
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_TROJA_HELP_2", (1, religion.getChar()))

    return szHelp

def doTroja3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iLoopPlayer)
        if loopPlayer.isAlive() and loopPlayer.getStateReligion() == player.getStateReligion():
            loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 3)
            player.AI_changeAttitudeExtra(iLoopPlayer, 3)

    return 1

def getHelpTroja3(argsList):
    iEvent = argsList[0]
    event = gc.getEventInfo(iEvent)
    kTriggeredData = argsList[1]
    religion = gc.getReligionInfo(kTriggeredData.eReligion)

    szHelp = localText.getText("TXT_KEY_EVENT_TROJA_HELP_3", (1, religion.getChar()))

    return szHelp

######## ZAUBERTRANK ###########

def canTriggerZaubertrank(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_CELT"):
        return true
    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
        return true
    return false

######## OREICHALKOS ###########

def canTriggerOreichalkos(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iOreichalkos = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OREICHALKOS')
    if player.getNumAvailableBonuses(iOreichalkos) > 0:
        return false

    return true

def doOreichalkos2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    city = player.getCity(kTriggeredData.iCityId)

    iOreichalkos = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OREICHALKOS')
    plot.setBonusType(iOreichalkos)

    szBuffer = localText.getText("TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", (gc.getBonusInfo(iOreichalkos).getTextKey(), city.getNameKey()))
    CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iOreichalkos).getButton(), gc.getInfoTypeForString("COLOR_WHITE"), plot.getX(), plot.getY(), true, true)

def getHelpOreichalkos2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OREICHALKOS')
    szHelp = localText.getText("TXT_KEY_EVENT_GET_BONUS_HELP", (gc.getBonusInfo(iBonus).getTextKey(),""))

    return szHelp

######## MAGNETIT ###########

def canTriggerMagnetit(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iMagnetit = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_MAGNETIT')
    if player.getNumAvailableBonuses(iMagnetit) > 0:
        return false

    return true

def doMagnetit2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    city = player.getCity(kTriggeredData.iCityId)

    iMagnetit = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_MAGNETIT')
    plot.setBonusType(iMagnetit)

    szBuffer = localText.getText("TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", (gc.getBonusInfo(iMagnetit).getTextKey(), city.getNameKey()))
    CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iMagnetit).getButton(), gc.getInfoTypeForString("COLOR_WHITE"), plot.getX(), plot.getY(), true, true)

def getHelpMagnetit2(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_MAGNETIT')
    szHelp = localText.getText("TXT_KEY_EVENT_GET_BONUS_HELP", (gc.getBonusInfo(iBonus).getTextKey(),""))

    return szHelp

######## FRAUENHAAR ###########

def canTriggerFrauenhaar(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_CELT"):
        return true
    if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
        return true
    return false

######## ARCHER ###########

def getHelpArcher1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 5
    szHelp = localText.getText("TXT_KEY_EVENT_ARCHER_HELP_1", (iNumUnits, ))

    return szHelp

def canTriggerArcherDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 5
    iUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_REFLEX_ARCHER')
    iUnits = player.getUnitClassCount(iUnitClass)
    if iUnits < iNumUnits:
        return false

    return true

######## ELEFANTEN ###########

def getHelpElefanten1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumUnits = gc.getMap().getWorldSize() + 5
    szHelp = localText.getText("TXT_KEY_EVENT_ELEFANTEN_HELP_1", (iNumUnits, ))

    return szHelp

def canTriggerElefantenDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iNumUnits = gc.getMap().getWorldSize() + 5
    iUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_WAR_ELEPHANT')
    iUnits = player.getUnitClassCount(iUnitClass)
    if iUnits < iNumUnits:
        return false

    return true

#### PROVINZHS ####

def canTriggerProvinzHS(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    if player.getNumCities() < 10:
        return false

    return true

def getHelpProvinzHS1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumProvinzHS = gc.getMap().getWorldSize() + 1
    szHelp = localText.getText("TXT_KEY_EVENT_PROVINZHS_HELP", (iNumProvinzHS, ))

    return szHelp

def canTriggerProvinzHSDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iProvinzHS = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_PROVINZPALAST')
    iProvinzHSRequired = gc.getMap().getWorldSize() + 1
    if iProvinzHSRequired > player.getBuildingClassCount(iProvinzHS):
        return false

    return true

#### KASTELL ####

def canTriggerKastell(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and player.isHuman(): return false

    if player.getNumCities() > 5:
        if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ROME"): return true
        if player.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"): return true

    return false

def getHelpKastell1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iKastellRequired = gc.getMap().getWorldSize() + 1
    szHelp = localText.getText("TXT_KEY_EVENT_KASTELL_HELP", (iKastellRequired, ))

    return szHelp

def canTriggerKastellDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    iKastell = gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
    iKastellRequired = gc.getMap().getWorldSize() + 1
    if iKastellRequired > player.getImprovementCount(iKastell):
        return false

    return true

def applyKastellDone1(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iKastell = gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
    team.changeImprovementYieldChange(iKastell, 1, 2)

def applyKastellDone2(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iKastell = gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
    team.changeImprovementYieldChange(iKastell, 2, 2)
    
######## Isis ###########

def canTriggerIsis(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    #city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
    #if None == city or city.isNone():
    #        return false

    # Hack to remember the number of cities you already have with the Corporation
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iOtherPlayerCityId = gc.getGame().countCorporationLevels(kTriggeredData.eCorporation)
    kActualTriggeredDataObject.iCityId = city.getID()
    kActualTriggeredDataObject.iPlotX = city.getX()
    kActualTriggeredDataObject.iPlotY = city.getY()

    bFound = false
    for iBuilding in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
            kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
            bFound = true
            break

    if not bFound:
        return false

    return true

def expireIsis1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if city is None or city.isNone():
        return true

    return false

def getHelpIsis1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    #iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 5
    iNumCities = gc.getMap().getWorldSize() + 4

    szHelp = localText.getText("TXT_KEY_EVENT_ISIS_HELP_1", (gc.getCorporationInfo(kTriggeredData.eCorporation).getTextKey(), iNumCities))

    return szHelp

def canTriggerIsisDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    iNumCitiesRequired = gc.getMap().getWorldSize() + 4 # + kOrigTriggeredData.iOtherPlayerCityId

    if iNumCitiesRequired > gc.getGame().countCorporationLevels(kOrigTriggeredData.eCorporation):
        return false

    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
    kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return true

######## Mithras ###########

def canTriggerMithras(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    #city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
    #if None == city or city.isNone():
    #        return false

    # Hack to remember the number of cities you already have with the Corporation
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iOtherPlayerCityId = gc.getGame().countCorporationLevels(kTriggeredData.eCorporation)
    kActualTriggeredDataObject.iCityId = city.getID()
    kActualTriggeredDataObject.iPlotX = city.getX()
    kActualTriggeredDataObject.iPlotY = city.getY()

    bFound = false
    for iBuilding in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
            kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
            bFound = true
            break

    if not bFound:
        return false

    return true

def expireMithras1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if city is None or city.isNone():
        return true

    return false

def getHelpMithras1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumCities = gc.getMap().getWorldSize() + 4

    szHelp = localText.getText("TXT_KEY_EVENT_MITHRAS_HELP_1", (gc.getCorporationInfo(kTriggeredData.eCorporation).getTextKey(), iNumCities))

    return szHelp

def canTriggerMithrasDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    iNumCitiesRequired = gc.getMap().getWorldSize() + 4 #+ kOrigTriggeredData.iOtherPlayerCityId

    if iNumCitiesRequired > gc.getGame().countCorporationLevels(kOrigTriggeredData.eCorporation):
        return false


    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
    kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return true

######## Helle ###########

def canTriggerHelle(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    city = player.getCity(kTriggeredData.iCityId)

    #city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
    #if None == city or city.isNone():
    #        return false

    # Hack to remember the number of cities you already have with the Corporation
    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.iOtherPlayerCityId = gc.getGame().countCorporationLevels(kTriggeredData.eCorporation)
    kActualTriggeredDataObject.iCityId = city.getID()
    kActualTriggeredDataObject.iPlotX = city.getX()
    kActualTriggeredDataObject.iPlotY = city.getY()

    bFound = false
    for iBuilding in range(gc.getNumBuildingInfos()):
        if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
            kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
            bFound = true
            break

    if not bFound:
        return false

    return true

def expireHelle1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    city = player.getCity(kTriggeredData.iCityId)
    if city is None or city.isNone():
        return true

    return false

def getHelpHelle1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    iNumCities = gc.getMap().getWorldSize() + 4

    szHelp = localText.getText("TXT_KEY_EVENT_HELLE_HELP_1", (gc.getCorporationInfo(kTriggeredData.eCorporation).getTextKey(), iNumCities))

    return szHelp

def canTriggerHelleDone(argsList):
    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

    iNumCitiesRequired = gc.getMap().getWorldSize() + 4 # + kOrigTriggeredData.iOtherPlayerCityId

    if iNumCitiesRequired > gc.getGame().countCorporationLevels(kOrigTriggeredData.eCorporation):
        return false


    kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
    kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
    kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
    kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
    kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
    kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY

    return true

######## MEUTEREI ###########

def canTriggerMeuterei(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    unit = player.getUnit(kTriggeredData.iUnitId)

    if unit is None or unit.isNone():
        return false

    iLoyal = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LOYALITAT')
    if unit.isHasPromotion(iLoyal):
        return false

    return true

def applyMeuterei(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_KONTERE')
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH)

######## KARAWANE ###########

def applyKarawane(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_MERCHANT')
    player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_MERCHANT, DirectionTypes.DIRECTION_SOUTH)

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_CARAVAN')
    player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_MERCHANT, DirectionTypes.DIRECTION_SOUTH)
    player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_MERCHANT, DirectionTypes.DIRECTION_SOUTH)

######## BALEAREN und KRETA ###########

def canTriggerBalearen(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
        return false

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if plot.getOwner() > -1 and plot.getOwner() != gc.getBARBARIAN_PLAYER():
        return false

    return true

def doBalearenRevealed(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    player = gc.getPlayer(kTriggeredData.ePlayer)

    plot.setRevealed(player.getTeam(), true, true, -1)
    # for PAE and the black fog of war
    CvUtil.addScriptData(plot,"H","X")
    if kTriggeredData.ePlayer == gc.getGame().getActivePlayer():
        CyCamera().JustLookAtPlot(CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY))

    return 1

def getHelpBalearen1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    iTurns = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 2

    szHelp = localText.getText("TXT_KEY_EVENT_BALEAREN_HELP_1", (iTurns, ))

    return szHelp

def expireBalearen1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 2:
        return true

    if plot.getOwner() != kTriggeredData.ePlayer and plot.getOwner() != gc.getBARBARIAN_PLAYER() and plot.getOwner() != -1:
        # for PAE and the black fog of war
        CvUtil.removeScriptData(plot,"H")
        return true

    return false

def canTriggerBalearenDone(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
    plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)

    if plot.getOwner() != kTriggeredData.ePlayer:
        return false

    # for PAE and the black fog of war
    CvUtil.removeScriptData(plot,"H")

    return true

def applyKretaDone(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iNumUnits  = gc.getMap().getWorldSize() + 1

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_ARCHER_KRETA')

    for i in range(iNumUnits):
        player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

def applyBalearenDone(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iNumUnits  = gc.getMap().getWorldSize() + 1

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_BALEAREN')

    for i in range(iNumUnits):
        player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

######## Soeldner ###########

def canTriggerSoeldner(argsList):
    kTriggeredData = argsList[0]
    trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
    player = gc.getPlayer(kTriggeredData.ePlayer)
    otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

    if not player.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
        return false

    listResources = []
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_CELTIC'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_ROMAN'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_NUMID'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_NUBIA'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_GREEK'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_PERSIA'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_GERMAN'))
    listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_INDIA'))

    bFound = false
    for iResource in listResources:
        if player.getNumTradeableBonuses(iResource) > 1 and otherPlayer.getNumAvailableBonuses(iResource) <= 0:
            bFound = true
            break

    if not bFound:
        return false

    for iTeam in range(gc.getMAX_CIV_TEAMS()):
        if iTeam != player.getTeam() and iTeam != otherPlayer.getTeam() and gc.getTeam(iTeam).isAlive():
            if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(player.getTeam()):
                return true

    return false

def canDoSoeldner1(argsList):
    kTriggeredData = argsList[1]
    newArgs = (kTriggeredData, )

    return canTriggerSoeldner(newArgs)

######## THORGAL ###########

def applyThorgal(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_VIKING_2')
    NewUnit = player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

    NewUnit.setName("Thorgal")

def getHelpRome_Religion_3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_THORGAL", ())

    return szHelp

######## BEDUINEN ###########

def canTriggerBeduinen(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    #   If Barbarians are disabled in this game, this event will not occur.
    if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
        return false

    #   At least one civ on the board must know Sattel.
    bFoundValid = false
    iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_HORSEBACK_RIDING_2')
    for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
        loopPlayer = gc.getPlayer(iPlayer)
        if loopPlayer.isAlive():
            if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
                bFoundValid = true
                break

    if not bFoundValid:
        return false

    #  Find an eligible plot
    map = gc.getMap()
    terr_desert = gc.getInfoTypeForString('TERRAIN_DESERT')
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.getTerrainType() == terr_desert and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            return true

    return false


def getHelpBeduinen1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_BEDUINEN_HELP_1", ())

    return szHelp


def applyBeduinen1(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    listPlots = []
    map = gc.getMap()
    terr_desert = gc.getInfoTypeForString('TERRAIN_DESERT')
    for i in range(map.numPlots()):
        plot = map.plotByIndex(i)
        if plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.getTerrainType() == terr_desert and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true):
            listPlots.append(i)

    if not listPlots:
        return

    plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Beduinen event location")])

    iNumUnits  = map.getWorldSize() + 2

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_BEDUINE')

    barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
    for i in range(iNumUnits):
        barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)

        
# Check City colony or province after events
# Nicht wieder entfernen!!! Das braucht man in den Events!
def doCheckCityStatus(argsList):
  iEvent = argsList[0]
  kTriggeredData = argsList[1]

  player = gc.getPlayer(kTriggeredData.ePlayer)
  pCity = player.getCity(kTriggeredData.iCityId)

  PAE_City.doCheckCityState( pCity )        
        
######## BIER ###########

def canTriggerBier(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iGaerung = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_GAERUNG')

    if team.isHasTech(iGaerung):
        return false

    return true

def applyBier(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    iTeam = player.getTeam()
    pTeam = gc.getTeam(iTeam)

    iGaerung = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_GAERUNG')

    pTeam.setHasTech(iGaerung, 1, kTriggeredData.ePlayer, 0, 1)

#######  Waldbrand ########

def applyForest_Fire (argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
    iVerbrannterWald = gc.getInfoTypeForString("FEATURE_FOREST_BURNT")

    plot.setFeatureType(iVerbrannterWald,1)

###### Reflexbogen #######

def canTriggerReflex(argsList):
    kTriggeredData = argsList[0]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    team = gc.getTeam(player.getTeam())

    iReflex = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_REFLEXBOGEN')

    if team.isHasTech(iReflex):
        return false

    return true

def applyReflex(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    iTeam = player.getTeam()
    pTeam = gc.getTeam(iTeam)

    iReflex = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_REFLEXBOGEN')

    pTeam.setHasTech(iReflex, 1, kTriggeredData.ePlayer, 0, 1)

######## Rome_Religion_3 ###########

def applyRome_Religion_3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PROPHET')
    NewUnit = player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

    NewUnit.setName("Pontifex Maximus")

def getHelpEvent_Prophet(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    szHelp = localText.getText("TXT_KEY_EVENT_PROPHET", ())

    return szHelp

######## Zoro_3 ###########

def applyZoro_3(argsList):
    iEvent = argsList[0]
    kTriggeredData = argsList[1]

    player = gc.getPlayer(kTriggeredData.ePlayer)
    plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

    iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PROPHET')
    NewUnit = player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

    NewUnit.setName("Zarathustra")

######## KEIN_WEIN ###########

def canTriggerKeinWein(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getNumAvailableBonuses(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_WINE')) > 0:
        return false

    return true

######## KEINE_OLIVEN ###########

def canTriggerKeineOliven(argsList):

    kTriggeredData = argsList[0]
    player = gc.getPlayer(kTriggeredData.ePlayer)

    if player.getNumAvailableBonuses(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OLIVES')) > 0:
        return false

    return true
