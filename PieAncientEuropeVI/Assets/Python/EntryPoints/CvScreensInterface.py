## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
import CvMainInterface
#import CvDomesticAdvisor
import CvTechChooser
#import CvForeignAdvisor
import CvExoticForeignAdvisor
#import CvMilitaryAdvisor
#import CvFinanceAdvisor
import CvReligionScreen
import CvCorporationScreen
import CvCivicsScreen
import CvVictoryScreen
import CvEspionageAdvisor
import CvTradeRouteAdvisor
import CvTradeRouteAdvisor2

import CvOptionsScreen
import CvReplayScreen
import CvHallOfFameScreen
import CvDanQuayle
import CvUnVictoryScreen

import CvDawnOfMan
# import CvTechSplashScreen
import CvTopCivs
import CvInfoScreen

import CvIntroMovieScreen
import CvVictoryMovieScreen
import CvWonderMovieScreen
import CvEraMovieScreen
import CvSpaceShipScreen

# import CvPediaMain
# import CvPediaHistory

# BUG - Sevopedia - start
import SevoScreenEnums
# BUG - Sevopedia - end

#import CvWorldBuilderScreen
#import CvWorldBuilderDiplomacyScreen

# import CvDebugTools
import CvDebugInfoScreen
#import CvDiplomacy

import CvUtil
# import CvEventInterface
# import CvPopupInterface
import CvScreenUtilsInterface
import ScreenInput as PyScreenInput
from CvScreenEnums import *
from CvPythonExtensions import *

# BUG - Options - end
import BugCore
AdvisorOpt = BugCore.game.Advisors
CustDomAdvOpt = BugCore.game.CustDomAdv
TechWindowOpt = BugCore.game.TechWindow

# K-Mod
import BugOptionsScreen
def showBugOptionsScreen(argsList=None):
    BugOptionsScreen.showOptionsScreen()
# K-Mod end
# BUG - Options - end

import PAE_Trade
import PAE_Cultivation
import PAE_Unit
import PAE_City

gc = CyGlobalContext()

g_bIsScreenActive = -1

## World Builder ##
import CvPlatyBuilderScreen
import WBPlotScreen
import WBRiverScreen
import WBEventScreen
import WBBuildingScreen
import WBCityDataScreen
import WBCityEditScreen
import WBTechScreen
import WBProjectScreen
import WBTeamScreen
import WBPlayerScreen
import WBUnitScreen
import WBPromotionScreen
import WBDiplomacyScreen
import WBGameDataScreen
import WBPlayerUnits
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import WBTradeScreen

def toggleSetNoScreens():
    global g_bIsScreenActive
    print "SCREEN OFF"
    g_bIsScreenActive = -1

def toggleSetScreenOn(argsList):
    global g_bIsScreenActive
    print "%s SCREEN TURNED ON" %(argsList[0],)
    g_bIsScreenActive = argsList[0]

#diplomacyScreen = CvDiplomacy.CvDiplomacy()

mainInterface = CvMainInterface.CvMainInterface()
def showMainInterface():
    mainInterface.interfaceScreen()

def reinitMainInterface():
    mainInterface.initState()

def numPlotListButtons():
    return mainInterface.numPlotListButtons()

techChooser = CvTechChooser.CvTechChooser()
def showTechChooser():
    if CyGame().getActivePlayer() != -1:
        techChooser.interfaceScreen()

hallOfFameScreen = CvHallOfFameScreen.CvHallOfFameScreen(HALL_OF_FAME)
def showHallOfFame(argsList):
    hallOfFameScreen.interfaceScreen(argsList[0])

civicScreen = CvCivicsScreen.CvCivicsScreen()
def showCivicsScreen():
    if CyGame().getActivePlayer() != -1:
        civicScreen.interfaceScreen()

religionScreen = CvReligionScreen.CvReligionScreen()
def showReligionScreen():
    if CyGame().getActivePlayer() != -1:
        religionScreen.interfaceScreen()

corporationScreen = CvCorporationScreen.CvCorporationScreen()
def showCorporationScreen():
    if CyGame().getActivePlayer() != -1:
        corporationScreen.interfaceScreen()

optionsScreen = CvOptionsScreen.CvOptionsScreen()
def showOptionsScreen():
    optionsScreen.interfaceScreen()

#foreignAdvisor = CvForeignAdvisor.CvForeignAdvisor()
foreignAdvisor = CvExoticForeignAdvisor.CvExoticForeignAdvisor()
def showForeignAdvisorScreen(argsList):
    if CyGame().getActivePlayer() != -1:
        foreignAdvisor.interfaceScreen(argsList[0])

# BUG - Finance Advisor - start
##
# K-Mod, 18/dec/10, karadoc
# I've disabled this option. We always use the 'economics advisor' now.
# (but the way I've done it is a kludge)
##
# PAE was
# financeAdvisor = CvFinanceAdvisor.CvFinanceAdvisor()
financeAdvisor = None
def createFinanceAdvisor():
    """Creates the correct Finance Advisor based on an option."""
    global financeAdvisor
    if financeAdvisor is None:
        import EconomicsAdvisor
        financeAdvisor = EconomicsAdvisor.EconomicsAdvisor()
#       if (AdvisorOpt.isBugFinanceAdvisor()):
#           import BugFinanceAdvisor
#           financeAdvisor = BugFinanceAdvisor.BugFinanceAdvisor()
#       else:
#           import CvFinanceAdvisor
#           financeAdvisor = CvFinanceAdvisor.CvFinanceAdvisor()
        HandleInputMap[FINANCE_ADVISOR] = financeAdvisor
# BUG - Finance Advisor - end

def showFinanceAdvisor():
    if CyGame().getActivePlayer() != -1:
        financeAdvisor.interfaceScreen()

# BUG - CustDomAdv - start
# PAE
# domesticAdvisor = CvDomesticAdvisor.CvDomesticAdvisor()
domesticAdvisor = None

def createDomesticAdvisor():
    """Creates the correct Domestic Advisor based on an option."""
    global domesticAdvisor
    if domesticAdvisor is None:
        if CustDomAdvOpt.isEnabled():
            import CvCustomizableDomesticAdvisor
            domesticAdvisor = CvCustomizableDomesticAdvisor.CvCustomizableDomesticAdvisor()
        else:
            import CvDomesticAdvisor
            domesticAdvisor = CvDomesticAdvisor.CvDomesticAdvisor()
        HandleInputMap[DOMESTIC_ADVISOR] = domesticAdvisor
# BUG - CustDomAdv - end

def showDomesticAdvisor(argsList):
    if CyGame().getActivePlayer() != -1:
        domesticAdvisor.interfaceScreen()

traderouteAdvisor = CvTradeRouteAdvisor.CvTradeRouteAdvisor()
def showTradeRouteAdvisor(argsList):
        if CyGame().getActivePlayer() > -1:
                traderouteAdvisor.interfaceScreen()

traderouteAdvisor2 = CvTradeRouteAdvisor2.CvTradeRouteAdvisor2()
def showTradeRouteAdvisor2(argsList):
        if CyGame().getActivePlayer() > -1:
                traderouteAdvisor2.interfaceScreen()
# BUG - Military Advisor - start
# PAE
# militaryAdvisor = CvMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
militaryAdvisor = None
def createMilitaryAdvisor():
    """Creates the correct Military Advisor based on an option."""
    global militaryAdvisor
    if militaryAdvisor is None:
        if (AdvisorOpt.isBUG_MA()):
            import CvBUGMilitaryAdvisor
            militaryAdvisor = CvBUGMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
        else:
            import CvMilitaryAdvisor
            militaryAdvisor = CvMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
        HandleInputMap[MILITARY_ADVISOR] = militaryAdvisor

def showMilitaryAdvisor():
    if CyGame().getActivePlayer() != -1:
        # if (AdvisorOpt.isBUG_MA()):
            # TODO: move to CvBUGMilitaryAdvisor.interfaceScreen()
            # militaryAdvisor.IconGridActive = False
        militaryAdvisor.interfaceScreen()
# BUG - Military Advisor - end

espionageAdvisor = CvEspionageAdvisor.CvEspionageAdvisor()
def showEspionageAdvisor():
    if CyGame().getActivePlayer() != -1:
        espionageAdvisor.interfaceScreen()

dawnOfMan = CvDawnOfMan.CvDawnOfMan(DAWN_OF_MAN)
def showDawnOfMan(argsList):
    dawnOfMan.interfaceScreen()

introMovie = CvIntroMovieScreen.CvIntroMovieScreen()
def showIntroMovie(argsList):
    introMovie.interfaceScreen()

victoryMovie = CvVictoryMovieScreen.CvVictoryMovieScreen()
def showVictoryMovie(argsList):
    victoryMovie.interfaceScreen(argsList[0])

wonderMovie = CvWonderMovieScreen.CvWonderMovieScreen()
def showWonderMovie(argsList):
    wonderMovie.interfaceScreen(argsList[0], argsList[1], argsList[2])

eraMovie = CvEraMovieScreen.CvEraMovieScreen()
def showEraMovie(argsList):
    eraMovie.interfaceScreen(argsList[0])

spaceShip = CvSpaceShipScreen.CvSpaceShipScreen()
def showSpaceShip(argsList):
    if CyGame().getActivePlayer() != -1:
        spaceShip.interfaceScreen(argsList[0])

replayScreen = CvReplayScreen.CvReplayScreen(REPLAY_SCREEN)
def showReplay(argsList):
    if argsList[0] > -1:
        CyGame().saveReplay(argsList[0])
    replayScreen.showScreen(argsList[4])

danQuayleScreen = CvDanQuayle.CvDanQuayle()
def showDanQuayleScreen(argsList):
    danQuayleScreen.interfaceScreen()

unVictoryScreen = CvUnVictoryScreen.CvUnVictoryScreen()
def showUnVictoryScreen(argsList):
    unVictoryScreen.interfaceScreen()

topCivs = CvTopCivs.CvTopCivs()
def showTopCivs():
    topCivs.showScreen()

infoScreen = CvInfoScreen.CvInfoScreen(INFO_SCREEN)
def showInfoScreen(argsList):
    if CyGame().getActivePlayer() != -1:
        iTabID = argsList[0]
        iEndGame = argsList[1]
        infoScreen.showScreen(-1, iTabID, iEndGame)

debugInfoScreen = CvDebugInfoScreen.CvDebugInfoScreen()
def showDebugInfoScreen():
    debugInfoScreen.interfaceScreen()

# BUG - Tech Splash Screen - start
techSplashScreen = None
def createTechSplash():
    """Creates the correct Tech Splash Screen based on an option."""
    global techSplashScreen
    if techSplashScreen is None:
        if (TechWindowOpt.isDetailedView()):
            import TechWindow
            techSplashScreen = TechWindow.CvTechSplashScreen(TECH_SPLASH)
        elif (TechWindowOpt.isWideView()):
            import TechWindowWide
            techSplashScreen = TechWindowWide.CvTechSplashScreen(TECH_SPLASH)
        else:
            import CvTechSplashScreen
            techSplashScreen = CvTechSplashScreen.CvTechSplashScreen(TECH_SPLASH)
    HandleInputMap[TECH_SPLASH] = techSplashScreen

def deleteTechSplash(option=None, value=None):
    global techSplashScreen
    techSplashScreen = None
    if TECH_SPLASH in HandleInputMap:
        del HandleInputMap[TECH_SPLASH]

def showTechSplash(argsList):
    if techSplashScreen is None:
        createTechSplash()
    techSplashScreen.interfaceScreen(argsList[0])
# BUG - Tech Splash Screen - end

victoryScreen = CvVictoryScreen.CvVictoryScreen(VICTORY_SCREEN)
def showVictoryScreen():
    if CyGame().getActivePlayer() != -1:
        victoryScreen.interfaceScreen()

#################################################
## Civilopedia
#################################################

# BUG - Sevopedia - start

pediaMainScreen = None
bUsingSevopedia = False
def createCivilopedia():
    """Creates the correct Civilopedia based on an option."""
    global pediaMainScreen
    global bUsingSevopedia
    if pediaMainScreen is None:
        import SevoPediaUtil
        if (AdvisorOpt.Sevopedia()):
            import SevoPediaMain
            import SevoPediaHistory
            bUsingSevopedia = True
            pediaMainScreen = SevoPediaMain.SevoPediaMain()
        else:
            import CvPediaMain
            import CvPediaHistory
            bUsingSevopedia = False
            pediaMainScreen = CvPediaMain.CvPediaMain()
        HandleInputMap.update(
                            {
                                PEDIA_MAIN : pediaMainScreen,
                                PEDIA_TECH : pediaMainScreen,
                                PEDIA_UNIT : pediaMainScreen,
                                PEDIA_BUILDING : pediaMainScreen,
                                PEDIA_PROMOTION : pediaMainScreen,
                                PEDIA_PROJECT : pediaMainScreen,
                                PEDIA_UNIT_CHART : pediaMainScreen,
                                PEDIA_BONUS : pediaMainScreen,
                                PEDIA_IMPROVEMENT : pediaMainScreen,
                                PEDIA_TERRAIN : pediaMainScreen,
                                PEDIA_FEATURE : pediaMainScreen,
                                PEDIA_CIVIC : pediaMainScreen,
                                PEDIA_CIVILIZATION : pediaMainScreen,
                                PEDIA_LEADER : pediaMainScreen,
                                PEDIA_RELIGION : pediaMainScreen,
                                PEDIA_CORPORATION : pediaMainScreen,
                                PEDIA_HISTORY : pediaMainScreen,

                                SevoScreenEnums.PEDIA_MAIN      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_TECHS     : pediaMainScreen,
                                SevoScreenEnums.PEDIA_UNITS     : pediaMainScreen,
                                SevoScreenEnums.PEDIA_UNIT_UPGRADES : pediaMainScreen,
                                SevoScreenEnums.PEDIA_UNIT_CATEGORIES   : pediaMainScreen,
                                SevoScreenEnums.PEDIA_PROMOTIONS    : pediaMainScreen,
                                SevoScreenEnums.PEDIA_PROMOTION_TREE    : pediaMainScreen,
                                SevoScreenEnums.PEDIA_BUILDINGS     : pediaMainScreen,
                                SevoScreenEnums.PEDIA_NATIONAL_WONDERS  : pediaMainScreen,
                                SevoScreenEnums.PEDIA_GREAT_WONDERS : pediaMainScreen,
                                SevoScreenEnums.PEDIA_PROJECTS      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_SPECIALISTS   : pediaMainScreen,
                                SevoScreenEnums.PEDIA_TERRAINS      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_FEATURES      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_BONUSES       : pediaMainScreen,
                                SevoScreenEnums.PEDIA_IMPROVEMENTS  : pediaMainScreen,
                                SevoScreenEnums.PEDIA_CIVS      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_LEADERS       : pediaMainScreen,
                                # SevoScreenEnums.PEDIA_TRAITS      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_CIVICS        : pediaMainScreen,
                                SevoScreenEnums.PEDIA_RELIGIONS     : pediaMainScreen,
                                SevoScreenEnums.PEDIA_CORPORATIONS  : pediaMainScreen,
                                SevoScreenEnums.PEDIA_CONCEPTS      : pediaMainScreen,
                                SevoScreenEnums.PEDIA_BTS_CONCEPTS  : pediaMainScreen,
                                SevoScreenEnums.PEDIA_HINTS     : pediaMainScreen,
                                SevoScreenEnums.PEDIA_SHORTCUTS     : pediaMainScreen,
                            })
        global HandleNavigationMap
        HandleNavigationMap = {
                            MAIN_INTERFACE : mainInterface,
                            PEDIA_MAIN : pediaMainScreen,
                            PEDIA_TECH : pediaMainScreen,
                            PEDIA_UNIT : pediaMainScreen,
                            PEDIA_BUILDING : pediaMainScreen,
                            PEDIA_PROMOTION : pediaMainScreen,
                            PEDIA_PROJECT : pediaMainScreen,
                            PEDIA_UNIT_CHART : pediaMainScreen,
                            PEDIA_BONUS : pediaMainScreen,
                            PEDIA_IMPROVEMENT : pediaMainScreen,
                            PEDIA_TERRAIN : pediaMainScreen,
                            PEDIA_FEATURE : pediaMainScreen,
                            PEDIA_CIVIC : pediaMainScreen,
                            PEDIA_CIVILIZATION : pediaMainScreen,
                            PEDIA_LEADER : pediaMainScreen,
                            PEDIA_HISTORY : pediaMainScreen,
                            PEDIA_RELIGION : pediaMainScreen,
                            PEDIA_CORPORATION : pediaMainScreen,

                            SevoScreenEnums.PEDIA_MAIN      : pediaMainScreen,
                            SevoScreenEnums.PEDIA_TECHS     : pediaMainScreen,
                            SevoScreenEnums.PEDIA_UNITS     : pediaMainScreen,
                            SevoScreenEnums.PEDIA_UNIT_UPGRADES : pediaMainScreen,
                            SevoScreenEnums.PEDIA_UNIT_CATEGORIES   : pediaMainScreen,
                            SevoScreenEnums.PEDIA_PROMOTIONS    : pediaMainScreen,
                            SevoScreenEnums.PEDIA_PROMOTION_TREE    : pediaMainScreen,
                            SevoScreenEnums.PEDIA_BUILDINGS     : pediaMainScreen,
                            SevoScreenEnums.PEDIA_NATIONAL_WONDERS  : pediaMainScreen,
                            SevoScreenEnums.PEDIA_GREAT_WONDERS : pediaMainScreen,
                            SevoScreenEnums.PEDIA_PROJECTS      : pediaMainScreen,
                            SevoScreenEnums.PEDIA_SPECIALISTS   : pediaMainScreen,
                            SevoScreenEnums.PEDIA_TERRAINS      : pediaMainScreen,
                            SevoScreenEnums.PEDIA_FEATURES      : pediaMainScreen,
                            SevoScreenEnums.PEDIA_BONUSES       : pediaMainScreen,
                            SevoScreenEnums.PEDIA_IMPROVEMENTS  : pediaMainScreen,
                            SevoScreenEnums.PEDIA_CIVS          : pediaMainScreen,
                            SevoScreenEnums.PEDIA_LEADERS       : pediaMainScreen,
                            # SevoScreenEnums.PEDIA_TRAITS      : pediaMainScreen,
                            SevoScreenEnums.PEDIA_CIVICS        : pediaMainScreen,
                            SevoScreenEnums.PEDIA_RELIGIONS     : pediaMainScreen,
                            SevoScreenEnums.PEDIA_CORPORATIONS  : pediaMainScreen,
                            SevoScreenEnums.PEDIA_CONCEPTS      : pediaMainScreen,
                            SevoScreenEnums.PEDIA_BTS_CONCEPTS  : pediaMainScreen,
                            SevoScreenEnums.PEDIA_HINTS         : pediaMainScreen,
                            SevoScreenEnums.PEDIA_SHORTCUTS     : pediaMainScreen,
                        }

def linkToPedia(argsList):
    pediaMainScreen.link(argsList[0])

def pediaShow():
    createCivilopedia()
    return pediaMainScreen.pediaShow()

def pediaBack():
    return pediaMainScreen.back()

def pediaForward():
    return pediaMainScreen.forward()

def pediaMain(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_MAIN, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_MAIN, argsList[0], True)

def pediaJumpToTech(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_TECHS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_TECH, argsList[0], True)

def pediaJumpToUnit(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_UNITS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_UNIT, argsList[0], True)

def pediaJumpToBuilding(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_BUILDINGS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_BUILDING, argsList[0], True)

def pediaJumpToProject(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_PROJECTS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_PROJECT, argsList[0], True)

def pediaJumpToReligion(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_RELIGIONS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_RELIGION, argsList[0], True)

def pediaJumpToCorporation(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CORPORATIONS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_CORPORATION, argsList[0], True)

def pediaJumpToPromotion(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_PROMOTIONS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_PROMOTION, argsList[0], True)

def pediaJumpToUnitChart(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_UNIT_CATEGORIES, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_UNIT_CHART, argsList[0], True)

def pediaJumpToBonus(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_BONUSES, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_BONUS, argsList[0], True)

def pediaJumpToTerrain(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_TERRAINS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_TERRAIN, argsList[0], True)

def pediaJumpToFeature(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_FEATURES, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_FEATURE, argsList[0], True)

def pediaJumpToImprovement(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_IMPROVEMENTS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_IMPROVEMENT, argsList[0], True)

def pediaJumpToCivic(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CIVICS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_CIVIC, argsList[0], True)

def pediaJumpToCiv(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CIVS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_CIVILIZATION, argsList[0], True)

def pediaJumpToLeader(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_LEADERS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_LEADER, argsList[0], True)

def pediaJumpToSpecialist(argsList):
    if bUsingSevopedia:
        pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_SPECIALISTS, argsList[0], True, False)
    else:
        pediaMainScreen.pediaJump(PEDIA_SPECIALIST, argsList[0], True)

def pediaShowHistorical(argsList):
    if bUsingSevopedia:
        if argsList[0] == CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW:
            pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_BTS_CONCEPTS, argsList[1], True, False)
        else:
            pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CONCEPTS, argsList[1], True, False)
    else:
        iEntryId = pediaMainScreen.pediaHistorical.getIdFromEntryInfo(argsList[0], argsList[1])
        pediaMainScreen.pediaJump(PEDIA_HISTORY, iEntryId, True)

# BUG - Sevopedia - end

#################################################
## Worldbuilder
#################################################
# Platy's
worldBuilderScreen = CvPlatyBuilderScreen.CvWorldBuilderScreen()
def getWorldBuilderScreen():
  return worldBuilderScreen

def showWorldBuilderScreen():
  worldBuilderScreen.interfaceScreen()

def hideWorldBuilderScreen():
  worldBuilderScreen.killScreen()

def WorldBuilderToggleUnitEditCB():
  worldBuilderScreen.toggleUnitEditCB()

def WorldBuilderEraseCB():
  worldBuilderScreen.eraseCB()

def WorldBuilderLandmarkCB():
  worldBuilderScreen.landmarkModeCB()

def WorldBuilderExitCB():
  worldBuilderScreen.Exit()

def WorldBuilderToggleCityEditCB():
  worldBuilderScreen.toggleCityEditCB()

def WorldBuilderNormalPlayerTabModeCB():
  worldBuilderScreen.normalPlayerTabModeCB()

def WorldBuilderNormalMapTabModeCB():
  worldBuilderScreen.normalMapTabModeCB()

def WorldBuilderRevealTabModeCB():
  worldBuilderScreen.revealTabModeCB()

def WorldBuilderDiplomacyModeCB():
  WBDiplomacyScreen.WBDiplomacyScreen().interfaceScreen(CyGame().getActivePlayer(), False)

def WorldBuilderRevealAllCB():
  worldBuilderScreen.revealAll(True)

def WorldBuilderUnRevealAllCB():
  worldBuilderScreen.revealAll(False)

def WorldBuilderGetHighlightPlot(argsList):
  return worldBuilderScreen.getHighlightPlot(argsList)

def WorldBuilderOnAdvancedStartBrushSelected(argsList):
  iList,iIndex,iTab = argsList;
  print("WB Advanced Start brush selected, iList=%d, iIndex=%d, type=%d" %(iList,iIndex,iTab))
  if (iTab == worldBuilderScreen.m_iASTechTabID):
    showTechChooser()
  elif (iTab == worldBuilderScreen.m_iASCityTabID and iList == worldBuilderScreen.m_iASAutomateListID):
    CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_AUTOMATE, worldBuilderScreen.m_iCurrentPlayer, -1, -1, -1, True)

  if (worldBuilderScreen.setCurrentAdvancedStartIndex(iIndex)):
    if (worldBuilderScreen.setCurrentAdvancedStartList(iList)):
      return 1
  return 0

def WorldBuilderGetASUnitTabID():
  return worldBuilderScreen.getASUnitTabID()

def WorldBuilderGetASCityTabID():
  return worldBuilderScreen.getASCityTabID()

def WorldBuilderGetASCityListID():
  return worldBuilderScreen.getASCityListID()

def WorldBuilderGetASBuildingsListID():
  return worldBuilderScreen.getASBuildingsListID()

def WorldBuilderGetASAutomateListID():
  return worldBuilderScreen.getASAutomateListID()

def WorldBuilderGetASImprovementsTabID():
  return worldBuilderScreen.getASImprovementsTabID()

def WorldBuilderGetASRoutesListID():
  return worldBuilderScreen.getASRoutesListID()

def WorldBuilderGetASImprovementsListID():
  return worldBuilderScreen.getASImprovementsListID()

def WorldBuilderGetASVisibilityTabID():
  return worldBuilderScreen.getASVisibilityTabID()

def WorldBuilderGetASTechTabID():
  return worldBuilderScreen.getASTechTabID()

#################################################
## Utility Functions (can be overridden by CvScreenUtilsInterface
#################################################

def movieDone(argsList):
    # allows overides for mods
    if hasattr(CvScreenUtilsInterface.getScreenUtils(), "movieDone"):
        if CvScreenUtilsInterface.getScreenUtils().movieDone(argsList):
            return

    if (argsList[0] == INTRO_MOVIE_SCREEN):
        introMovie.hideScreen()

    if (argsList[0] == VICTORY_MOVIE_SCREEN):
        victoryMovie.hideScreen()

def leftMouseDown (argsList):
    # allows overides for mods
    if (CvScreenUtilsInterface.getScreenUtils().leftMouseDown(argsList)):
        return

    if ( argsList[0] == WORLDBUILDER_SCREEN ):
        worldBuilderScreen.leftMouseDown(argsList[1:])
        return 1
    return 0

def rightMouseDown (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().rightMouseDown(argsList):
        return

    if argsList[0] == WORLDBUILDER_SCREEN:
        worldBuilderScreen.rightMouseDown(argsList)
        return 1
    return 0

def mouseOverPlot (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().mouseOverPlot(argsList):
        return

    if WORLDBUILDER_SCREEN == argsList[0]:
        worldBuilderScreen.mouseOverPlot(argsList)

def handleInput (argsList):
    'handle input is called when a screen is up'
    inputClass = PyScreenInput.ScreenInput(argsList)

    # allows overides for mods
    ret = CvScreenUtilsInterface.getScreenUtils().handleInput((inputClass.getPythonFile(),inputClass))

    # get the screen that is active from the HandleInputMap Dictionary
    screen = HandleInputMap.get(inputClass.getPythonFile())

    # call handle input on that screen
    if screen and not ret:
        return screen.handleInput(inputClass)
    return 0

def update (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().update(argsList):
        return

    if argsList[0] in HandleInputMap:
        screen = HandleInputMap.get(argsList[0])
        screen.update(argsList[1])

def onClose (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().onClose(argsList):
        return

    if argsList[0] in HandleCloseMap:
        screen = HandleCloseMap.get(argsList[0])
        screen.onClose()

# Forced screen update
def forceScreenUpdate (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().forceScreenUpdate(argsList):
        return

    # Tech chooser update (forced from net message)
    if argsList[0] == TECH_CHOOSER:
        techChooser.updateTechRecords(False)
    # Main interface Screen
    elif argsList[0] == MAIN_INTERFACE:
        mainInterface.updateScreen()
    # world builder Screen
    elif argsList[0] == WORLDBUILDER_SCREEN:
        worldBuilderScreen.updateScreen()

    # BTS Original
    # world builder diplomacy Screen
    # elif argsList[0] == WORLDBUILDER_DIPLOMACY_SCREEN:
    #    worldBuilderDiplomacyScreen.updateScreen()

# Forced redraw
def forceScreenRedraw (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().forceScreenRedraw(argsList):
        return

    # Main Interface Screen
    if argsList[0] == MAIN_INTERFACE:
        mainInterface.redraw()
    # BTS Original
    #elif argsList[0] == WORLDBUILDER_SCREEN:
    #    worldBuilderScreen.redraw()
    #elif argsList[0] == WORLDBUILDER_DIPLOMACY_SCREEN:
    #    worldBuilderDiplomacyScreen.redraw()
    elif argsList[0] == TECH_CHOOSER:
        techChooser.updateTechRecords(True)


def minimapClicked (argsList):
    # allows overides for mods
    if CvScreenUtilsInterface.getScreenUtils().minimapClicked(argsList):
        return

    if MILITARY_ADVISOR == argsList[0]:
        militaryAdvisor.minimapClicked()

############################################################################
## Misc Functions
############################################################################

def handleBack(screens):
    for iScreen in screens:
        if iScreen in HandleNavigationMap:
            screen = HandleNavigationMap.get(iScreen)
            screen.back()
    print "Mouse BACK"
    return 0

def handleForward(screens):
    for iScreen in screens:
        if iScreen in HandleNavigationMap:
            screen = HandleNavigationMap.get(iScreen)
            screen.forward()
    print "Mouse FWD"
    return 0

def refreshMilitaryAdvisor (argsList):
    if argsList[0] == 1:
        militaryAdvisor.refreshSelectedGroup(argsList[1])
    elif argsList[0] == 2:
        militaryAdvisor.refreshSelectedLeader(argsList[1])
    elif argsList[0] == 3:
        militaryAdvisor.drawCombatExperience()
    elif argsList[0] <= 0:
        militaryAdvisor.refreshSelectedUnit(-argsList[0], argsList[1])

def updateMusicPath (argsList):
    szPathName = argsList[0]
    optionsScreen.updateMusicPath(szPathName)

def refreshOptionsScreen():
    optionsScreen.refreshScreen()

def cityWarningOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
    if city and not city.isNone():
        if iButtonId == 0:
            if city.isProductionProcess():
                CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, False, False)
            else:
                CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, True, False)
        elif iButtonId == 2:
            CyInterface().selectCity(city, False)

def cityWarningOnFocusCallback(argsList):
    CyInterface().playGeneralSound("AS2D_ADVISOR_SUGGEST")
    CyInterface().lookAtCityOffset(argsList[0])
    return 0

def liberateOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
    if (not city.isNone()):
        if (iButtonId == 0):
            CyMessageControl().sendDoTask(iData1, TaskTypes.TASK_LIBERATE, 0, -1, False, False, False, False)
        elif (iButtonId == 2):
            CyInterface().selectCity(city, False)

def colonyOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
    if city and not city.isNone():
        if iButtonId == 0:
            CyMessageControl().sendEmpireSplit(CyGlobalContext().getGame().getActivePlayer(), city.area().getID())
        elif iButtonId == 2:
            CyInterface().selectCity(city, False)

def featAccomplishedOnClickedCallback(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    if iButtonId == 1:
        if iData1 == FeatTypes.FEAT_TRADE_ROUTE:
            showDomesticAdvisor(())
        elif (iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_UNIT_SPY):
            showMilitaryAdvisor()
        elif (iData1 >= FeatTypes.FEAT_COPPER_CONNECTED) and (iData1 <= FeatTypes.FEAT_FOOD_CONNECTED):
            showForeignAdvisorScreen([0])
        elif (iData1 == FeatTypes.FEAT_NATIONAL_WONDER):
            # 2 is for the wonder tab...
            showInfoScreen([2, 0])
        elif (iData1 >= FeatTypes.FEAT_POPULATION_HALF_MILLION) and (iData1 <= FeatTypes.FEAT_POPULATION_2_BILLION):
            # 1 is for the demographics tab...
            showInfoScreen([1, 0])
        elif iData1 == FeatTypes.FEAT_CORPORATION_ENABLED:
            showCorporationScreen()

def featAccomplishedOnFocusCallback(argsList):
    iData1 = argsList[0]
    iData2 = argsList[1]
    iData3 = argsList[2]
    iData4 = argsList[3]
    szText = argsList[4]
    bOption1 = argsList[5]
    bOption2 = argsList[6]

    CyInterface().playGeneralSound("AS2D_FEAT_ACCOMPLISHED")
    if iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER and iData1 <= FeatTypes.FEAT_FOOD_CONNECTED:
        CyInterface().lookAtCityOffset(iData2)

    return 0

def popupHunsPayment(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    if iButtonId == 1: # = YES - NetID , iPlayer , unitID
      CyMessageControl().sendModNetMessage( 674, iData1, iData2, 0, 0 )

def popupRevoltPayment(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    #  NetID , iPlayer , City ID , RevoltTurns , 0 | 1 | 2
    CyMessageControl().sendModNetMessage( 675, iData1, iData2, iData3, iButtonId )

def popupProvinzPayment(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # NetID , iPlayer, CityID , ButtonID
    CyMessageControl().sendModNetMessage( 678, iData1, iData2, iButtonId, iData3 )

# Sell unit (Mercenary post)
# iOwner, iUnitID
def popupSellUnit(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # NetID , confirm = 1, nix , iPlayer, iUnitID
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 695, 1, 0, iData1, iData2 )

# Vasallen - Feature +++++++++++++++++++++++++
def popupVassal01(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser, iGold
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 671, iData1, iData2, iData3, 0 )
    # Kill Botschafter 0 to Loser / 1 to Winner
    elif iButtonId == 2:
        CyMessageControl().sendModNetMessage( 671, iData1, iData2, -1, iData4 )

def popupVassal03(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser, iGold1, iGold2
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 682, iData1, iData2, iData3, 0 )
    elif iButtonId == 1:
        CyMessageControl().sendModNetMessage( 682, iData1, iData2, iData4, 0 )
    else:
        CyMessageControl().sendModNetMessage( 682, iData1, iData2, -1, 0 )

def popupVassal04(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser, iGold1, iGold2
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 683, iData1, iData2, iData3, 0 )
    elif iButtonId == 1:
        CyMessageControl().sendModNetMessage( 683, iData1, iData2, iData4, 0 )

def popupVassal05(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser, iGold1
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 684, iData1, iData2, iData3, 0 ) # YES
    if iButtonId == 1:
        CyMessageControl().sendModNetMessage( 684, iData1, iData2, 0, 0 ) # NO
    else:
        CyMessageControl().sendModNetMessage( 684, iData1, iData2, -1, 0 ) # KILL

def popupVassal06(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser, iGold1
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 685, iData1, iData2, iData3, 0 ) # YES
    if iButtonId == 1:
        CyMessageControl().sendModNetMessage( 685, iData1, iData2, 0, 0 ) # NO
    else:
        CyMessageControl().sendModNetMessage( 685, iData1, iData2, -1, 0 ) # KILL

def popupVassal07(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3] # 0/1
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser, 0 , 0/1 (Loser/Winnerauswahl)
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 686, iData1, iData2, iData3, iData4 ) # YES

def popupVassal08(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # = YES - NetID , iWinner , iLoser (Hegemon), iVassal , iGold
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 687, iData1, iData2, iData3, iData4 ) # YES

def popupVassal09(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # iWinner , iLoser (Hegemon), iVassal , 0=Yes,1=No
    CyMessageControl().sendModNetMessage( 688, iData1, iData2, iData3, iButtonId ) # Yes or No

def popupVassal10(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # iWinner , iLoser (Hegemon), iVassal , iGold
    # NO: Kein Interesse: Gold=0
    if iButtonId == 1:
        iData4 = 0
    CyMessageControl().sendModNetMessage( 689, iData1, iData2, iData3, iData4 ) # Yes or No

def popupVassal11(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # iWinner , iLoser (Hegemon), iVassal , iGold
    # iButton:
    # Yes:  0
    # NO:   1 Kein Interesse, keine Auswirkungen. Ende.
    # KILL: 2
    if iButtonId != 1:
        if iButtonId == 2:
            iData4 = -1 # KILL
        CyMessageControl().sendModNetMessage( 690, iData1, iData2, iData3, iData4 ) # Yes or Kill

def popupVassal12(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 691, iData1, iData2, iData3, iData4 ) # Yes

def popupVassalTech(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # iHegemon (HI) , iVassal, iTech , iTechCost
    # iButton:
    # Yes   0: Tech, Beziehung +1
    # Half money 1: Tech mit halbem Geld, keine weiteren Auswirkungen
    # Money 2: Tech mit Geld, Beziehung -1
    # NO:   3: Keine Tech, Beziehung -2
    if iButtonId == 0:
        iData4 = -1
    elif iButtonId == 1:
        iData4 = int(iData4 / 2)
    elif iButtonId == 3:
        iData3 = -1
    CyMessageControl().sendModNetMessage( 702, iData1, iData2, iData3, iData4 )

def popupVassalTech2(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]

    # iHegemon (HI) , iVassal, iTech , iTechCost
    # iButton:
    # Yes 0: Tech kaufen
    # NO  1: Tech nicht kaufen
    if iButtonId == 1:
        iData4 = -1
    CyMessageControl().sendModNetMessage( 703, iData1, iData2, iData3, iData4 )

def popupReliaustreibung(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]
    szText = argsList[5]
    bOption1 = argsList[6]
    bOption2 = argsList[7]
    # iPlayer, iCity, iUnit , iCancelButton
    if iButtonId != iData4:
         CyMessageControl().sendModNetMessage( 704, iData1, iData2, iButtonId, iData3 )

def popupRenegadeCity(argsList):
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iWinner , pCity.getID , iLoser
    # iButtonId: Keep | Enslave | Raze
    CyMessageControl().sendModNetMessage( 706, iData1, iData2, iData3, iButtonId )

# Mercenaries -----------
def popupMercenariesMain(argsList):
    # iData1 (cityID), iData2 (iPlayer)
    iButtonId = argsList[0]
    iCity = argsList[1]
    iPlayer = argsList[2]
    #~ iData3 = argsList[3]
    iButtonCancel = argsList[4]

    # Hire (0) or Assign (1) mercenaries
    if iButtonId != iButtonCancel:
        if iButtonId == 0:
            CyMessageControl().sendModNetMessage(708, iCity, -1, -1, iPlayer)
        elif iButtonId == 1:
            CyMessageControl().sendModNetMessage(709, -1, -1, -1, iPlayer)

def popupMercenariesHire(argsList):
    # iData1 (cityID), iData2 = iUnitClassTyp, iData3 = iPlayer
    # iButtonID = iUnitClassTyp
    iButtonId = argsList[0]
    iCity = argsList[1]
    iData2 = argsList[2]
    iPlayer = argsList[3]
    iButtonCancel = argsList[4]

    # no back button between hire and assign
    # if iButtonId == iButtonCancel-1 and iData2 != -1: iButtonId = -1

    # Archers (0), Spearmen (1), Melee (2), Eles (3), Ships (4)
    if iButtonId != iButtonCancel:
        CyMessageControl().sendModNetMessage( 708, iCity, iButtonId, -1, iPlayer )

def popupMercenariesHireUnits(argsList):
    # iData1 (cityID), iData2 = iUnitClassTyp, iData3 = iPlayer
    # iButtonID = Unit
    iButtonId = argsList[0]
    iCity = argsList[1]
    iTypeButton = argsList[2]
    iPlayer = argsList[3]
    iButtonCancel = argsList[4]

    # back button
    if iButtonId == iButtonCancel - 1:
        iTypeButton = -1

    # iData2 = Archers (0), Melee (1), Mounted (2), Eles (3), Ships (4)
    # iButtonID = Unit
    if iButtonId != iButtonCancel:
        CyMessageControl().sendModNetMessage( 708, iCity, iTypeButton, iButtonId, iPlayer )

# Assign mercenaries ------

def popupMercenariesAssign1(argsList):
    # iData3 = iPlayer, iData4 = Cancel
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonId = CIV
    if iButtonId != iData4:
        CyMessageControl().sendModNetMessage( 709, iButtonId, -1, -1, iData3 )
        # von 709 geht es direkt weiter zu 710

def popupMercenariesAssign2(argsList):
    # iData1 = iTargetCIV, iData3 = iPlayer, iData4 = Cancel
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonId = Inter/nationality
    if iButtonId != iData4:
        iFaktor = iButtonId + 1
        CyMessageControl().sendModNetMessage( 711, iData1, iFaktor, -1, iData3 )

def popupMercenariesAssign3(argsList):
    # iData1 = iTargetCIV, iData2 = iFaktor, iData3 = iPlayer, iData4 = Cancel
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonId = mercenary groups size
    if iButtonId != iData4:
        iFaktor = iData2 + (iButtonId + 1) * 10
        CyMessageControl().sendModNetMessage( 712, iData1, iFaktor, -1, iData3 )

def popupMercenariesAssign4(argsList):
    # iData1 = iTargetCIV, iData2 = iFaktor, iData3 = iPlayer, iData4 = Cancel
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonId = unit types (offensive/defensive/naval)
    if iButtonId != iData4:
        iFaktor = iData2 + (iButtonId + 1) * 100
        # Naval units (ignore next window: siege units)
        if iButtonId == 4:
            iFaktor += 1000
            CyMessageControl().sendModNetMessage( 714, iData1, iFaktor, -1, iData3 )
        # Land units
        else:
            CyMessageControl().sendModNetMessage( 713, iData1, iFaktor, -1, iData3 )

def popupMercenariesAssign5(argsList):
    # iData1 = iTargetCIV, iData2 = iFaktor, iData3 = iPlayer, iData4 = Cancel
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonId = siege units
    if iButtonId != iData4:
        iFaktor = iData2 + (iButtonId + 1) * 1000
        CyMessageControl().sendModNetMessage( 714, iData1, iFaktor, -1, iData3 )

def popupMercenariesAssign6(argsList):
    # iData1 = iTargetCIV, iData2 = iFaktor, iData3 = iPlayer, iData4 = Cancel
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonId = confirmation
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage( 715, iData1, iData2, -1, iData3 )

def popupMercenaryTorture(argsList):
    # iData1 (iMercenaryCiv), iData2 (iPlayer)
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # Begin Torture (0)
    if iButtonId == 0:
        CyMessageControl().sendModNetMessage(716, iData1, iData2, -1, -1)

def popupMercenaryTorture2(argsList):
    # iData1 (iMercenaryCiv), iData2 (iPlayer)
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # Begin Torture (0)
    if iButtonId <= 2:
        CyMessageControl().sendModNetMessage(717, iData1, iData2, iButtonId, -1)

def popupReservists(argsList):
    # iData1 (iCityID), iData2 (iPlayer)
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonID = Unit
    if iButtonId != iData4:
       CyMessageControl().sendModNetMessage( 725, iData1, iData2, iButtonId, 0 )

def popupBonusverbreitung(argsList):
    # iData1 (iPlayer), iData2 (iUnitId), iData3 (Page)
    # Page: 0: First Page, 1: Getreide, 2: Vieh, ...)
    iButtonId = argsList[0]
    iData1 = argsList[1]
    iData2 = argsList[2]
    iData3 = argsList[3]
    iData4 = argsList[4]

    # iButtonID = Bonus (First: bonus types)
    if iButtonId != iData4:
        # back button
        if iData3 != -1 and iButtonId == 0:
            CyMessageControl().sendModNetMessage(726, -1, -1, iData1, iData2)
        # first page (bonus types)
        elif iData3 == -1:
            CyMessageControl().sendModNetMessage(726, iButtonId, -1, iData1, iData2)
        # pages
        else:
            CyMessageControl().sendModNetMessage(726, iData3, iButtonId, iData1, iData2)

# Cultivation / Trade / Boggy
# Called when player has selected bonus to buy
def popupTradeChooseBonus(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    pPlayer = gc.getPlayer(iUnitOwner)
    pUnit = pPlayer.getUnit(iUnitId)
    # Since CyPopup can only store 3 values, the city needs to be identified by the merchant's position...
    pCity = CyMap().plot(pUnit.getX(), pUnit.getY()).getPlotCity()
    lGoods = PAE_Trade.getCitySaleableGoods(pCity, iUnitOwner)
    if iButtonId < len(lGoods): # Otherwise: Cancel button
        CyMessageControl().sendModNetMessage( 742, lGoods[iButtonId], pCity.getOwner(), iUnitOwner, iUnitId )

# Cultivation / Trade / Boggy
# Called when player has selected cultivation bonus to buy
def popupTradeChooseBonus4Cultivation(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    pPlayer = gc.getPlayer(iUnitOwner)
    pUnit = pPlayer.getUnit(iUnitId)
    # Since CyPopup can only store 3 values, the city needs to be identified by the merchant's position...
    pCity = CyMap().plot(pUnit.getX(), pUnit.getY()).getPlotCity()
    lGoods = PAE_Cultivation.getCollectableGoods4Cultivation(pUnit)
    if iButtonId < len(lGoods): # Otherwise: Cancel button
        CyMessageControl().sendModNetMessage( 739, lGoods[iButtonId], 0, iUnitOwner, iUnitId )

# Called when player has selected civ to trade with. Next step: Select city.
def popupTradeRouteChooseCiv(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    bFirst = argsList[3]
    pUnit = gc.getPlayer(iUnitOwner).getUnit(iUnitId)
    lCivList = PAE_Trade.getPossibleTradeCivs(iUnitOwner)

    if bFirst and not pUnit.plot().isCity():
        # In the first panel, there are :
        # - 1 button for the local city
        # - x buttons for x civ
        # - 1 cancel button
        # but if the unit isn't in a city, the first button doesn't exists
        iShift = 0
    else:
        iShift = 1

    if iButtonId < len(lCivList) + iShift:
        #CyMessageControl().sendModNetMessage( 745, lCivList[iButtonId], -1, iUnitOwner, iUnitId )
        # Next step: if bFirst: choose city 1, else: choose city 2
        iNewType = 0
        if bFirst:
          # Diese Stadt oder Abbruch
          if iButtonId == 0:
            if pUnit.plot().isCity():
              pCity = pUnit.plot().getPlotCity()
              CyMessageControl().sendModNetMessage( 745, pCity.getOwner(), pCity.getID(), iUnitOwner, iUnitId )
            else:
              iNewType = 2
          else:
            iNewType = 2
        else:
          # Own nation or back to step 1
          if iButtonId == 0:
            #iX = int(CvUtil.getScriptData(pUnit, ["autX1"], -1))
            #iY = int(CvUtil.getScriptData(pUnit, ["autY1"], -1))
            #if CyMap().plot(iX, iY).getPlotCity().getOwner() != pUnit.getOwner():
            #PAE_Trade.doPopupAutomatedTradeRoute(pUnit, 5, iUnitOwner, 0)
            #else:
            PAE_Trade.doPopupAutomatedTradeRoute(pUnit, 1, 0, 0)
          else:
            iNewType = 5

        if iNewType:
          PAE_Trade.doPopupAutomatedTradeRoute(pUnit, iNewType, lCivList[iButtonId - iShift], -1)

# Called when player has selected city to trade with. Next step: Select bonus.
def popupTradeRouteChooseCity1(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    iCityOwner = argsList[3]
    pUnit = gc.getPlayer(iUnitOwner).getUnit(iUnitId)
    lCityList = PAE_Trade.getPossibleTradeCitiesForCiv(pUnit, iCityOwner, 1)
    if iButtonId < len(lCityList):
        CyMessageControl().sendModNetMessage( 745, iCityOwner, lCityList[iButtonId].getID(), iUnitOwner, iUnitId )

# Same as above, but for second city in trade route. Two functions are needed bc. popupInfo only stores 4 values (5 needed)
def popupTradeRouteChooseCity2(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    iCityOwner = argsList[3]
    pUnit = gc.getPlayer(iUnitOwner).getUnit(iUnitId)
    lCityList = PAE_Trade.getPossibleTradeCitiesForCiv(pUnit, iCityOwner, 2)
    if iButtonId < len(lCityList):
        CyMessageControl().sendModNetMessage( 746, iCityOwner, lCityList[iButtonId].getID(), iUnitOwner, iUnitId )

# Called when has selected bonus to buy in city. Next step: Select civ 2 or start trade route (if finished)
def popupTradeRouteChooseBonus(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    bFirst = argsList[3]
    pUnit = gc.getPlayer(iUnitOwner).getUnit(iUnitId)
    if bFirst:
        iX = int(CvUtil.getScriptData(pUnit, ["autX1"], -1))
        iY = int(CvUtil.getScriptData(pUnit, ["autY1"], -1))
    else:
        iX = int(CvUtil.getScriptData(pUnit, ["autX2"], -1))
        iY = int(CvUtil.getScriptData(pUnit, ["autY2"], -1))


    pCity = CyMap().plot(iX, iY).getPlotCity()
    lGoods = PAE_Trade.getCitySaleableGoods(pCity, -1)
    lGoods.append(-1)
    if iButtonId < len(lGoods):
      CyMessageControl().sendModNetMessage( 747, lGoods[iButtonId], bFirst, iUnitOwner, iUnitId )

# --- End of cultivation / trade

def popupKartenzeichnungen(argsList):
        # iData1 (iPlayer), iData2 (iUnitId)
        iButtonId = argsList[0]
        iData1 = argsList[1]
        iData2 = argsList[2]
        iData3 = argsList[3]
        iData4 = argsList[4]
        if iButtonId != iData4:
          CyMessageControl().sendModNetMessage( 728, iButtonId, -1, iData1, iData2 )

def popupReleaseSlaves(argsList):
        # iData1 (iCityID), iData2 (iPlayer)
        iButtonId = argsList[0]
        iData1 = argsList[1]
        iData2 = argsList[2]
        iData3 = argsList[3]
        iData4 = argsList[4]

        # iButtonID = type of slave
        if iButtonId != iData4:
           CyMessageControl().sendModNetMessage( 730, iData1, 0, iData2, iButtonId )

def popupBuildLimes(argsList):
        # iData1 (iPlayer), iData2 (iUnitID)
        iButtonId = argsList[0]
        iData1 = argsList[1]
        iData2 = argsList[2]
        iData3 = argsList[3]
        iData4 = argsList[4]

        # iButtonID = type of limes
        if iButtonId != iData4:
           CyMessageControl().sendModNetMessage( 733, iButtonId, 0, iData1, iData2 )

# Sold/Salae/Decimatio
# iOwner, iUnitID, Typ: Salae(1) or Decimatio(2)
def popupActionSalaeDecimatio(argsList):
        iButtonId = argsList[0]
        iData1 = argsList[1]
        iData2 = argsList[2]
        iData3 = argsList[3]
        iData4 = argsList[4]
        szText = argsList[5]
        bOption1 = argsList[6]
        bOption2 = argsList[7]

        # NetID , Typ, confirm = 1, iPlayer, iUnitID
        if iButtonId == 0:
          CyMessageControl().sendModNetMessage( 735, iData3, 1, iData1, iData2 )

# Provinzstatthalter / Tribut
# iCityID, iOwner, iTyp (-1, 0 = Einfluss, 1 = Tribut)
# Statische iButtonId Werte
def popupStatthalterTribut(argsList):
        iButtonId = argsList[0]
        iData1 = argsList[1]
        iData2 = argsList[2]
        iData3 = argsList[3]
        iData4 = argsList[4]

        # NetID , iCity, iOwner, iButton, -1
        if iData3 == -1:
          CyMessageControl().sendModNetMessage( 737, iData1, iData2, iButtonId, -1 )
        # NetID, iCity, iOwner, iTyp, iButton
        elif iButtonId != iData4:
          CyMessageControl().sendModNetMessage( 737, iData1, iData2, iData3, iButtonId )

# Vasallen kuendigen oder Staedte schenken
# -1, iPlayer, iVasall
# Dynamische iButtonId Werte
def popupVasallen(argsList):
        iButtonId = argsList[0]
        iData1 = argsList[1]
        iData2 = argsList[2]
        iData3 = argsList[3]
        iData4 = argsList[4]

        if iButtonId != -1 and iButtonId != iData4:
          # NetID , iPlayer, -1, -1, -1
          if iData2 == -1:
            CyMessageControl().sendModNetMessage( 764, iData1, iButtonId, -1, -1 )
          # NetID, iPlayer, iVasall, -1, -1
          else:
            CyMessageControl().sendModNetMessage( 764, iData1, iData2, iButtonId, iData4 )

# Heldendenkmal / Siegesdenkmal
def popupChooseHeldendenkmal(argsList):
    iButtonId = argsList[0]
    iUnitOwner = argsList[1]
    iUnitId = argsList[2]
    pPlayer = gc.getPlayer(iUnitOwner)
    pUnit = pPlayer.getUnit(iUnitId)
    # Since CyPopup can only store 3 values, the city needs to be identified by the unit's position.
    pCity = CyMap().plot(pUnit.getX(), pUnit.getY()).getPlotCity()
    lBuildings = PAE_City.getHeldendenkmalList(pCity)

    if iButtonId < len(lBuildings): # Otherwise: Cancel button
        CyMessageControl().sendModNetMessage( 758, 0, lBuildings[iButtonId], iUnitOwner, iUnitId )



##############################################################
####################### for scenarios ########################
##############################################################
# ----- Scenario Peloponnesian War ----------------
import PeloponnesianWarKeinpferd
def peloponnesianWarKeinpferd_Poteidaia1(argsList):
    PeloponnesianWarKeinpferd.Poteidaia1(argsList)
def peloponnesianWarKeinpferd_Poteidaia2(argsList):
    PeloponnesianWarKeinpferd.Poteidaia2(argsList)
def peloponnesianWarKeinpferd_Poteidaia3(argsList):
    PeloponnesianWarKeinpferd.Poteidaia3(argsList)
def peloponnesianWarKeinpferd_Megara1(argsList):
    PeloponnesianWarKeinpferd.Megara1(argsList)
def peloponnesianWarKeinpferd_Megara2(argsList):
    PeloponnesianWarKeinpferd.Megara2(argsList)
def peloponnesianWarKeinpferd_Plataiai1(argsList):
    PeloponnesianWarKeinpferd.Plataiai1(argsList)
def peloponnesianWarKeinpferd_Syra1(argsList):
    PeloponnesianWarKeinpferd.Syra1(argsList)

# --------------------

#######################################################################################
## Handle Close Map
#######################################################################################
HandleCloseMap = {DAWN_OF_MAN : dawnOfMan,
                  SPACE_SHIP_SCREEN : spaceShip,
                  TECH_CHOOSER : techChooser,
                  # add new screens here
                 }

#######################################################################################
## Handle Input Map
#######################################################################################
HandleInputMap = {  MAIN_INTERFACE : mainInterface,
                    # DOMESTIC_ADVISOR : domesticAdvisor,
                    RELIGION_SCREEN : religionScreen,
                    CORPORATION_SCREEN : corporationScreen,
                    CIVICS_SCREEN : civicScreen,
                    TECH_CHOOSER : techChooser,
                    FOREIGN_ADVISOR : foreignAdvisor,
                    # FINANCE_ADVISOR : financeAdvisor,
                    # MILITARY_ADVISOR : militaryAdvisor,
                    DAWN_OF_MAN : dawnOfMan,
                    WONDER_MOVIE_SCREEN : wonderMovie,
                    ERA_MOVIE_SCREEN : eraMovie,
                    SPACE_SHIP_SCREEN : spaceShip,
                    INTRO_MOVIE_SCREEN : introMovie,
                    OPTIONS_SCREEN : optionsScreen,
                    INFO_SCREEN : infoScreen,
                    # PAE
                    # TECH_SPLASH : techSplashScreen,
                    REPLAY_SCREEN : replayScreen,
                    VICTORY_SCREEN : victoryScreen,
                    TOP_CIVS : topCivs,
                    HALL_OF_FAME : hallOfFameScreen,
                    VICTORY_MOVIE_SCREEN : victoryMovie,
                    ESPIONAGE_ADVISOR : espionageAdvisor,
                    DAN_QUAYLE_SCREEN : danQuayleScreen,
                    # PAE
                    PEDIA_MAIN : pediaMainScreen,
                    PEDIA_TECH : pediaMainScreen,
                    PEDIA_UNIT : pediaMainScreen,
                    PEDIA_BUILDING : pediaMainScreen,
                    PEDIA_PROMOTION : pediaMainScreen,
                    PEDIA_PROJECT : pediaMainScreen,
                    PEDIA_UNIT_CHART : pediaMainScreen,
                    PEDIA_BONUS : pediaMainScreen,
                    PEDIA_IMPROVEMENT : pediaMainScreen,
                    PEDIA_TERRAIN : pediaMainScreen,
                    PEDIA_FEATURE : pediaMainScreen,
                    PEDIA_CIVIC : pediaMainScreen,
                    PEDIA_CIVILIZATION : pediaMainScreen,
                    PEDIA_LEADER : pediaMainScreen,
                    PEDIA_RELIGION : pediaMainScreen,
                    PEDIA_CORPORATION : pediaMainScreen,
                    PEDIA_HISTORY : pediaMainScreen,

                    WORLDBUILDER_SCREEN : worldBuilderScreen,
                    # Platy
                    # WORLDBUILDER_DIPLOMACY_SCREEN : worldBuilderDiplomacyScreen,

                    DEBUG_INFO_SCREEN : debugInfoScreen,

                    ## Platy World Builder ##
                    WB_PLOT : WBPlotScreen.WBPlotScreen(),
                    WB_PLOT_RIVER : WBRiverScreen.WBRiverScreen(),
                    WB_EVENT: WBEventScreen.WBEventScreen(),
                    WB_BUILDING : WBBuildingScreen.WBBuildingScreen(),
                    WB_CITYDATA : WBCityDataScreen.WBCityDataScreen(),
                    WB_CITYEDIT : WBCityEditScreen.WBCityEditScreen(),
                    WB_TECH : WBTechScreen.WBTechScreen(),
                    WB_PROJECT : WBProjectScreen.WBProjectScreen(),
                    WB_TEAM : WBTeamScreen.WBTeamScreen(),
                    WB_PLAYER : WBPlayerScreen.WBPlayerScreen(),
                    WB_UNIT : WBUnitScreen.WBUnitScreen(worldBuilderScreen),
                    WB_PROMOTION : WBPromotionScreen.WBPromotionScreen(),
                    WB_DIPLOMACY : WBDiplomacyScreen.WBDiplomacyScreen(),
                    WB_GAMEDATA : WBGameDataScreen.WBGameDataScreen(worldBuilderScreen),
                    WB_UNITLIST : WBPlayerUnits.WBPlayerUnits(),
                    WB_RELIGION : WBReligionScreen.WBReligionScreen(),
                    WB_CORPORATION : WBCorporationScreen.WBCorporationScreen(),
                    WB_INFO : WBInfoScreen.WBInfoScreen(),
                    WB_TRADE : WBTradeScreen.WBTradeScreen(),
                    # PAE Trade routes
                    TRADEROUTE_ADVISOR : traderouteAdvisor,
                    TRADEROUTE_ADVISOR2 : traderouteAdvisor2,

                                }

#######################################################################################
## Handle Navigation Map
#######################################################################################

# HandleNavigationMap = {}

# BUG - Options - start
def init():
    createDomesticAdvisor()
    createFinanceAdvisor()
    createMilitaryAdvisor()
    createCivilopedia()
    createTechSplash()
# BUG - Options - end
