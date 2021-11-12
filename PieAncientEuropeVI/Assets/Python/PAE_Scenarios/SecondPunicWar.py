# Scenario SecondPunicWar by Barcas

# Imports
from CvPythonExtensions import *
import CvEventInterface
import CvUtil
import PyHelpers

# Defines
gc = CyGlobalContext()


def onEndPlayerTurn(iPlayer, iGameTurn):
    # Event 1, Beginn Runde 2 (218 v.Chr.) Kriegserklärung Team 0 (Rom) an Team 1 (Karthago) 
    if iGameTurn == 2:
        
        # ewiger Krieg
        gc.getTeam(gc.getPlayer(0).getTeam()).setPermanentWarPeace(gc.getPlayer(1).getTeam(), True)
        
        # Meldung an die Spieler
        iRange = gc.getMAX_PLAYERS()
        for iLoopPlayer in xrange(iRange):
            pPlayer = gc.getPlayer(iLoopPlayer)
            if pPlayer.isHuman():
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
                popupInfo.setText(CyTranslator().getText("TXT_KEY_SCENARIO_SECOND_PUNIC_WAR_EVENT1", ("",)))
                popupInfo.addPopup(iLoopPlayer)

    # Event 2, Beginn Runde 45 (214 v.Chr.) Kriegserklärung Team 12 (Syrakus) an Team 0 (Rom)
    if iGameTurn == 45:
        
        # ewiger Krieg
        gc.getTeam(gc.getPlayer(12).getTeam()).setPermanentWarPeace(gc.getPlayer(0).getTeam(), True)
        
        # Meldung an die Spieler
        iRange = gc.getMAX_PLAYERS()
        for iLoopPlayer in xrange(iRange):
            pPlayer = gc.getPlayer(iLoopPlayer)
            if pPlayer.isHuman():
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
                popupInfo.setText(CyTranslator().getText("TXT_KEY_SCENARIO_SECOND_PUNIC_WAR_EVENT2", ("",)))
                popupInfo.addPopup(iLoopPlayer)


def onCityAcquired(pCity, iNewOwner):
    iCivRome = 0  # Capital: Rome
    iCivCarthage = 1  # Capital: Carthage
    sData = CvUtil.getScriptData(pCity.plot(), ["t"])
    if sData == "Rome" and iNewOwner == iCivCarthage or sData == "Carthage" and iNewOwner == iCivRome:

        # PAE Movie
        if gc.getPlayer(iNewOwner).isHuman():
            if iNewOwner == iCivRome:
                iMovie = 1
            else:
                iMovie = 2
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setData1(iMovie)  # dynamicID in CvWonderMovieScreen
            popupInfo.setData2(0)  # fix pCity.getID()
            popupInfo.setData3(3)  # fix PAE Movie ID for victory movies
            popupInfo.setText(u"showWonderMovie")
            popupInfo.addPopup(iNewOwner)

        gc.getGame().setWinner(gc.getPlayer(iNewOwner).getTeam(), 2)
