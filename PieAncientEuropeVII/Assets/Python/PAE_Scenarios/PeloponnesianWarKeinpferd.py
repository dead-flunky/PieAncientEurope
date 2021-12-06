# Scenario PeloponnesianWarKeinpferd

# Imports
from CvPythonExtensions import *
import CvEventInterface
import CvScreensInterface
import CvUtil
import PyHelpers

import PAE_City
# Defines
gc = CyGlobalContext()


def onEndGameTurn(iGameTurn):
	if iGameTurn == 228:
		# Athen (0) soll von 414 an mit Sparta (1) ewig den dekeleischen Krieg fuehren
		gc.getTeam(gc.getPlayer(0).getTeam()).setPermanentWarPeace(gc.getPlayer(1).getTeam(), true)


def onBeginPlayerTurn(iGameTurn, pPlayer):

	iTeam = pPlayer.getTeam()
	iAthen = 0
	iSparta = 1
	iKorinth = 2
	iTheben = 4
	iSyrakus = 16
	# Event 1: Poteidaia verlangt geringere Abgaben
	iTurnPotei = 8  # Runde, in der das Popup fuer den Menschen erscheinen soll
	# Die KI reagiert sofort noch in dieser Runde, der Mensch erhaelt erst in der naechsten Runde das Popup
	# Nur, wenn Poteidaia existiert + von Athen kontrolliert wird
	pPoteidaia = CyMap().plot(56, 46).getPlotCity()
	if iTeam == iAthen and ((iGameTurn == iTurnPotei-1 and pPlayer.isHuman()) or (iGameTurn == iTurnPotei and not pPlayer.isHuman())) and pPoteidaia and not pPoteidaia.isNone():
	   if pPoteidaia.getOwner() == iAthen:
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_DESC", ()))
				popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Poteidaia1")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_OPTION_1", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_OPTION_2", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_OPTION_3", ()), "")
				popupInfo.addPopup(iPlayer)
			else:
				iAiDecision = CvUtil.myRandom(3, "Poteidaia1")
				Poteidaia1([iAiDecision])
	# Event 2: Krieg um Poteidaia
	iTurnPotei = 18  # Runde, in der die Popups fuer den Menschen erscheinen sollen
	# Nur, wenn Poteidaia existiert + von Athen kontrolliert wird
	if iTeam == iAthen and ((iGameTurn == iTurnPotei-1 and pPlayer.isHuman()) or (iGameTurn == iTurnPotei and not pPlayer.isHuman())) and pPoteidaia and not pPoteidaia.isNone():
		if pPoteidaia.getOwner() == iAthen:
			# Event 2.1: Reaktion Athens
			# Poteidaia wechselt zu Korinth (Team 2)
			PAE_City.doRenegadeCity(pPoteidaia, 2, None)
			pKorinth = gc.getPlayer(iKorinth)
			ePantodapoi = gc.getInfoTypeForString("UNIT_AUXILIAR_MACEDON")
			iRange = CvUtil.myRandom(3, "num ePantodapoi")
			# Korinth erhaelt 0 - 2 zusaetzliche makedonische Hilfstrupps in Poteidaia
			for _ in xrange(iRange):
				pKorinth.initUnit(ePantodapoi, 56, 46, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_WORLDNEWS", ()), None, 2, None, ColorTypes(11), 0, 0, False, False)
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_DESC", ()))
				popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Poteidaia2")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_1", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_2", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_3", ()), "")
				popupInfo.addPopup(iPlayer)
			else:
				iAiDecision = CvUtil.myRandom(3, "Poteidaia2")
				Poteidaia2([iAiDecision])
	# Nur, wenn Poteidaia existiert + von Korinth oder Athen kontrolliert wird (menschlicher Spieler spielt Korinth: zu diesem Zeitpunkt gehoert Poteidaia noch Athen; KI spielt Korinth: ist bereits zu Korinth gewechselt)
	elif iTeam == iKorinth and ((iGameTurn == iTurnPotei-1 and pPlayer.isHuman()) or (iGameTurn == iTurnPotei and not pPlayer.isHuman())) and pPoteidaia and not pPoteidaia.isNone():
		if pPoteidaia.getOwner() == iKorinth or pPoteidaia.getOwner() == iAthen:
			# Event 2.2: Reaktion Korinths
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_DESC", ()))
				popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Poteidaia3")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_1", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_2", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_3", ()), "")
				popupInfo.addPopup(iPlayer)
			else:
				iAiDecision = CvUtil.myRandom(3, "Poteidaia3")
				Poteidaia3([iAiDecision])
	# Event 3: Megara unterstuetzt Korinth
	iTurnMegaraAthen = 22  # Runde, in der die Popups fuer den Menschen erscheinen sollen
	# Nur, wenn Megara existiert + von Korinth kontrolliert wird
	pMegara = CyMap().plot(55, 30).getPlotCity()
	if pMegara and not pMegara.isNone():
		if iTeam == iAthen and ((iGameTurn == iTurnMegaraAthen-1 and pPlayer.isHuman()) or (iGameTurn == iTurnMegaraAthen and not pPlayer.isHuman())):
			if pMegara.getOwner() == iKorinth:
				# Event 3.1: Reaktion Athens
				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_DESC", ()))
					popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Megara1")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_1", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_2", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_3", ()), "")
					popupInfo.addPopup(iPlayer)
				else:
					iAiDecision = CvUtil.myRandom(3, "Megara1")
					Megara1([iAiDecision])
		# Event 3.2: Reaktion Spartas (nur wenn Sparta noch keinen Krieg mit Athen hat)
		iTurnMegaraSparta = 23  # Runde, in der die Popups fuer den Menschen erscheinen sollen
		# Nur, wenn Megara existiert + von Korinth kontrolliert wird
		if iTeam == iSparta and ((iGameTurn == iTurnMegaraSparta-1 and pPlayer.isHuman()) or (iGameTurn == iTurnMegaraSparta and not pPlayer.isHuman())):
			if pMegara.getOwner() == iKorinth and not gc.getTeam(iTeam).isAtWar(iAthen):
				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_DESC", ()))
					popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Megara2")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_1", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_2", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3", ()), "")
					popupInfo.addPopup(iPlayer)
				else:
					iAiDecision = CvUtil.myRandom(3, "Megara2")
					Megara2([iAiDecision])
	# Event 4: Kriegseintritt Thebens
	iTurnPlataiai = 28  # Runde, in der die Popups fuer den Menschen erscheinen sollen
	if iTeam == iTheben and ((iGameTurn == iTurnPlataiai-1 and pPlayer.isHuman()) or (iGameTurn == iTurnPlataiai and not pPlayer.isHuman())):
		if not gc.getTeam(iTeam).isAtWar(iAthen):  # Nur wenn Theben und Athen Frieden haben
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_THEBEN_DESC", ()))
				popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Plataiai1")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_THEBEN_OPTION_1", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_THEBEN_OPTION_2", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_THEBEN_OPTION_3", ()), "")
				popupInfo.addPopup(iPlayer)
			else:
				iAiDecision = CvUtil.myRandom(3, "Plataiai1")
				Plataiai1([iAiDecision])
	# Event 5: Volksversammlung Athens will Krieg gegen Syrakus
	# Event 5.1: Ankuendigung fuer Athen
	iTurnSyra1 = 194  # Runde, in der die Popups fuer den Menschen erscheinen sollen
	pSyrakus = CyMap().plot(15, 24).getPlotCity()
	# Nur wenn Syrakus (Stadt) noch existiert und der Civ Syrakus gehoert
	if pSyrakus and not pSyrakus.isNone():
		if iTeam == iAthen and (iGameTurn == iTurnSyra1 - 1):
			if pSyrakus.getOwner() == iSyrakus:
				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_SAVEMONEY", ()))
					popupInfo.addPopup(iPlayer)
	# Event 5.2: Athen waehlt Groesse der Flotte
	iTurnSyra2 = 204  # Runde, in der die Popups fuer den Menschen erscheinen sollen
	if iTeam == iAthen and ((iGameTurn == iTurnSyra2 - 1 and pPlayer.isHuman()) or (iGameTurn == iTurnSyra2 and not pPlayer.isHuman())):
		if not gc.getTeam(iTeam).isAtWar(iSyrakus):  # Nur wenn Syrakus und Athen Frieden haben
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_DESC", ()))
				popupInfo.setOnClickedPythonCallback("peloponnesianWarKeinpferd_Syra1")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_1", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_2", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_3", ()), "")
				popupInfo.addPopup(iPlayer)
			else:
				iAiDecision = CvUtil.myRandom(3, "Syra1")
				Syra1([iAiDecision])

	# Temporaere Effekte der Events rueckgaengig machen (Event 3.1 Handelsboykott, Event 3.2 Bronze fuer Sparta)
	if iGameTurn == iTurnMegaraAthen + 10:
		iAthen = 0
		iNordIonien = 12
		iSuedIonien = 13
		eHafen = gc.getInfoTypeForString("BUILDING_HARBOR")
		eMarkt = gc.getInfoTypeForString("BUILDING_MARKET")
		eHafenClass = gc.getBuildingInfo(eHafen).getBuildingClassType()
		eMarktClass = gc.getBuildingInfo(eMarkt).getBuildingClassType()
		lPlayer = [iAthen, iNordIonien, iSuedIonien]
		for iPlayer in lPlayer:
			pPlayer = gc.getPlayer(iPlayer)
			iNumCities = pPlayer.getNumCities()
			for iCity in xrange(iNumCities):
				pCity = pPlayer.getCity(iCity)
				if pCity is not None and not pCity.isNone():
					if pCity.isHasBuilding(eHafen):
						iStandard = 0  # Normaler Goldertrag ohne Event
						pCity.setBuildingCommerceChange(eHafenClass, 0, iStandard)  # 0 = Gold
					if pCity.isHasBuilding(eMarkt):
						iStandard = 0
						pCity.setBuildingCommerceChange(eMarktClass, 0, iStandard)  # 0 = Gold
	if iGameTurn == iTurnMegaraSparta + 10:
		# Bronze wird a
		eBronze = gc.getInfoTypeForString("BONUS_BRONZE")
		pCity = CyMap().plot(52, 23).getPlotCity()
		if pCity and not pCity.isNone():
			if pCity.getFreeBonus(eBronze) > 1:
				pCity.changeFreeBonus(eBronze, -1)


def onEndPlayerTurn(iPlayer, iGameTurn):
	# Runde 1: In Runde 5 soll das mit Korkyra im Krieg liegende Epidamnos Vasall von Korinth werden
	if iGameTurn == 5:
		iCivKorinth = 2
		iCivKorkyra = 6
		iCivEpidamnos = 7
		iCivSparta = 1
		if iPlayer == iCivEpidamnos:

			iTeamKorinth = gc.getPlayer(iCivKorinth).getTeam()
			iTeamEpidamnos = gc.getPlayer(iCivEpidamnos).getTeam()
			pTeamEpidamnos = gc.getTeam(iTeamEpidamnos)

			if not pTeamEpidamnos.isVassal(iTeamKorinth):

				iTeamKorinth = gc.getPlayer(iCivKorinth).getTeam()
				gc.getTeam(iTeamKorinth).assignVassal(iTeamEpidamnos, 0)  # Vassal, but no surrender

				# Meldungen an die Spieler
				iRange = gc.getMAX_PLAYERS()
				for iLoopPlayer in xrange(iRange):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isHuman():
						# Meldung Korkyra Human
						if iLoopPlayer == iCivKorkyra:
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_EPIDAMNOS_PLAYER_KERKYRA", ("",)))
							popupInfo.addPopup(iLoopPlayer)
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_WAR_PLAYER_KORKYRA", ("",)))
							popupInfo.addPopup(iThisPlayer)
						elif iLoopPlayer == iCivKorinth:
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_EPIDAMNOS_PLAYER_ALL", ("",)))
							popupInfo.addPopup(iLoopPlayer)
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_WAR_PLAYER_KORINTH", ("",)))
							popupInfo.addPopup(iLoopPlayer)
						# Meldung an alle Humans
						else:
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_EPIDAMNOS_PLAYER_ALL", ("",)))
							popupInfo.addPopup(iLoopPlayer)

def Poteidaia1(argsList):
		iButtonId = argsList[0]
		iAthen = 0
		iKorinth = 2
		iMakedonien = 10
		iNordIonien = 12
		pPlotPoteidaia = gc.getMap().plot(56,46)
		pCityPoteidaia = pPlotPoteidaia.getPlotCity()
		bIsHuman = gc.getPlayer(iAthen).isHuman()
		if iButtonId == 0:
			iGold = 500
			gc.getPlayer(iAthen).changeGold(iGold)
			gc.getPlayer(iNordIonien).AI_changeAttitudeExtra(iAthen,-3)
			pCityPoteidaia.changeHurryAngerTimer(pCityPoteidaia.hurryAngerLength(0)*3)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_OPTION_1_OUTCOME",()))
				popupInfo.addPopup(iAthen)
		elif iButtonId == 1:
			pCityPoteidaia.changeOccupationTimer(6)
			for i in xrange(gc.getMAX_PLAYERS()):
				if i != iKorinth:
					pPlotPoteidaia.setCulture(i, 0, True)
			gc.getPlayer(iKorinth).AI_changeAttitudeExtra(iAthen,-3)
			gc.getPlayer(iAthen).AI_changeAttitudeExtra(iKorinth,-3)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_OPTION_2_OUTCOME",()))
				popupInfo.addPopup(iAthen)
		elif iButtonId == 2:
			gc.getPlayer(iKorinth).AI_changeAttitudeExtra(iAthen,-5)
			gc.getPlayer(iAthen).AI_changeAttitudeExtra(iKorinth,-3)
			gc.getTeam(iKorinth).signDefensivePact(iMakedonien)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_TRIBUT_OPTION_3_OUTCOME",()))
				popupInfo.addPopup(iAthen)

def Poteidaia2(argsList):
	iButtonId = argsList[0]
	iAthen = 0
	pAthen = gc.getPlayer(iAthen)
	iKorinth = 2
	iMakedonien = 10
	pMakedonien = gc.getPlayer(iMakedonien)
	iThrakien = 11
	bIsHuman = pAthen.isHuman()
	if iButtonId == 0:
		if gc.getTeam(iAthen).canDeclareWar(iKorinth):
			gc.getTeam(iAthen).declareWar(iKorinth, 0, 5) #WARPLAN_TOTAL
		if gc.getTeam(iAthen).canDeclareWar(iMakedonien):
			gc.getTeam(iAthen).declareWar(iMakedonien, 0, 4) #WARPLAN_LIMITED
		iGold = pAthen.getGold()
		if iGold <= 5000:
			pAthen.setGold(0)
		else:
			pAthen.changeGold(-5000)
		iX = 55
		iY = 45
		eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
		eProdromoi = gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON")
		eSupply = gc.getInfoTypeForString("UNIT_SUPPLY_WAGON")
		eSkirmish = gc.getInfoTypeForString("UNIT_SKIRMISHER")
		eTrireme = gc.getInfoTypeForString("UNIT_TRIREME")
		for _ in xrange(2):
			pAthen.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		for i in xrange(3):
			pUnit = pAthen.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if i == 0:
				pUnit.setName("Pausanias")
			elif i == 1:
				pUnit.setName("Archestartos")
		pAthen.initUnit(eProdromoi, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pSupply = pAthen.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		PAE_Unit.setSupply(pUnit,200)
		pAthen.initUnit(eSkirmish, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# 500 Gold pro Hoplit+Trireme, 2 Triremen erhaelt man immer -> iPay beginnt bei 1000 und man benoetigt mind. 1500, um mehr zu erhalten
		# Maximal 10 Triremen
		iPay = 1000
		for i in xrange(8):
			iPay += 500
			if iPay > iGold:
				break
			pAthen.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			pAthen.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			if iGold < 2000:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_1_OUTCOME_LOW",()))
			elif iGold < 3500:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_1_OUTCOME_MEDIUM",()))
			else:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_1_OUTCOME_HIGH",()))
			popupInfo.addPopup(iAthen)
	elif iButtonId == 1:
		pThrakien = gc.getPlayer(iThrakien)
		bDefPact = gc.getTeam(iMakedonien).isDefensivePact(iKorinth)
		if gc.getTeam(iAthen).canDeclareWar(iKorinth):
			gc.getTeam(iAthen).declareWar(iKorinth, 0, 5) #WARPLAN_TOTAL
		pThrakien.AI_changeAttitudeExtra(iAthen,3)
		pMakedonien.AI_changeAttitudeExtra(iThrakien,-3)
		pAthen.changeGold(-250)
		pThrakien.changeGold(250)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			if not bDefPact:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_2_OUTCOME_SUCCESS",()))
			else:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_2_OUTCOME_FAILED",()))
			popupInfo.addPopup(iAthen)
	elif iButtonId == 2:
		if gc.getTeam(iAthen).canDeclareWar(iKorinth):
			gc.getTeam(iAthen).declareWar(iKorinth, 0, 5) #WARPLAN_TOTAL
		if gc.getTeam(iAthen).canDeclareWar(iMakedonien):
			gc.getTeam(iAthen).declareWar(iMakedonien, 0, 4) #WARPLAN_LIMITED
		# General in Athen
		pGeneral = pAthen.initUnit(gc.getInfoTypeForString("UNIT_GREAT_GENERAL"), 57, 30, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pGeneral.setName("Kallias")
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_OPTION_3_OUTCOME",()))
			popupInfo.addPopup(iAthen)

def Poteidaia3(argsList):
	iButtonId = argsList[0]
	iKorinth = 2
	pKorinth = gc.getPlayer(iKorinth)
	bIsHuman = pKorinth.isHuman()
	if iButtonId == 0:
		iX = 53
		iY = 30
		iGold = pKorinth.getGold()
		if iGold <= 2000:
			pKorinth.setGold(0)
		else:
			pKorinth.changeGold(-2000)
		eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
		eHorseman = gc.getInfoTypeForString("UNIT_HORSEMAN")
		eSkirmisher = gc.getInfoTypeForString("UNIT_SKIRMISHER")
		eSupply = gc.getInfoTypeForString("UNIT_SUPPLY_WAGON")
		pKorinth.initUnit(eHorseman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pSupply = pKorinth.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		PAE_Unit.setSupply(pSupply,200)
		pKorinth.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pKorinth.initUnit(eSkirmisher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# 250 Gold pro Hoplit+Skirmisher, jeweils 1 erhaelt man immer -> iPay beginnt bei 250 und man benoetigt mind. 500, um mehr zu erhalten
		# Maximal 8 Hopliten und Skirmisher (insgesamt)
		iPay = 250
		for _ in xrange(7):
			iPay += 250
			if iPay > iGold:
				break
			pKorinth.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			pKorinth.initUnit(eSkirmisher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			if iGold < 750:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_1_OUTCOME_LOW",()))
			elif iGold < 1500:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_1_OUTCOME_MEDIUM",()))
			else:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_ATHEN_KORINTH_1_OUTCOME_HIGH",()))
			popupInfo.addPopup(iKorinth)
	elif iButtonId == 1:
		pKorinth.changeGold(-150)
		iX = 36
		iY = 48
		eGallier = gc.getInfoTypeForString("UNIT_HOPLIT")
		pKorinth.initUnit(eGallier, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_2_OUTCOME",()))
			popupInfo.addPopup(iKorinth)
	elif iButtonId == 2:
		pKorinth.changeGold(-250)
		iX = 55
		iY = 46
		eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
		eProdromoi = gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON")
		eSkirmish = gc.getInfoTypeForString("UNIT_SKIRMISHER")
		eSupply = gc.getInfoTypeForString("UNIT_SUPPLY_WAGON")
		eGeneral = gc.getInfoTypeForString("UNIT_GREAT_GENERAL")
		eTrireme = gc.getInfoTypeForString("UNIT_TRIREME")
		for _ in xrange(2):
			pKorinth.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		for _ in xrange(2):
			pKorinth.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pKorinth.initUnit(eProdromoi, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pKorinth.initUnit(eSkirmish, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pSupply = pKorinth.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		PAE_Unit.setSupply(pSupply,200)
		pGeneral = pKorinth.initUnit(eGeneral, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pGeneral.setName("Iolaos")
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_POTEIDAIA_KRIEG_KORINTH_OPTION_3_OUTCOME",()))
			popupInfo.addPopup(iKorinth)

def Megara1(argsList):
	iButtonId = argsList[0]
	iAthen = 0
	iSparta = 1
	iKorinth = 2
	iTheben = 4
	iNordIonien = 12
	iSuedIonien = 13
	bIsHuman = gc.getPlayer(iAthen).isHuman()
	bNordIsVassal = gc.getTeam(iNordIonien).isVassal(iAthen)
	bSuedIsVassal = gc.getTeam(iSuedIonien).isVassal(iAthen)
	if iButtonId == 0:
		# Verschlechterung der Beziehungen zwischen Athen und ionischen Vasallen um -2 (nur wenn sie noch Vasallen sind)
		if bNordIsVassal:
			gc.getPlayer(iNordIonien).AI_changeAttitudeExtra(iAthen, -2)
		if bSuedIsVassal:
			gc.getPlayer(iSuedIonien).AI_changeAttitudeExtra(iAthen, -2)
		# Verringerte Ertraege in Markt und Hafen fuer Athen und Ionier (verschwindet langsam)
		iVerlust = -5
		eHafen = gc.getInfoTypeForString("BUILDING_HARBOR")
		eMarkt = gc.getInfoTypeForString("BUILDING_MARKET")
		eHafenClass = gc.getBuildingInfo(eHafen).getBuildingClassType()
		eMarktClass = gc.getBuildingInfo(eMarkt).getBuildingClassType()
		lPlayer = [iAthen]
		if bNordIsVassal:
			lPlayer.append(iNordIonien)
		if bSuedIsVassal:
			lPlayer.append(iSuedIonien)
		for iPlayer in lPlayer:
			pPlayer = gc.getPlayer(iPlayer)
			iNumCities = pPlayer.getNumCities()
			for iCity in xrange(iNumCities):
				pCity = pPlayer.getCity(iCity)
				if pCity and not pCity.isNone():
					if pCity.isHasBuilding(eHafen):
						iStandard = pCity.getBuildingCommerceChange(eHafenClass, CommerceTypes.COMMERCE_GOLD) # 0 = Gold
						pCity.setBuildingCommerceChange(eHafenClass, CommerceTypes.COMMERCE_GOLD, iStandard + iVerlust)
					if pCity.isHasBuilding(eMarkt):
						iStandard = pCity.getBuildingCommerceChange(eMarktClass, CommerceTypes.COMMERCE_GOLD) # 0 = Gold
						pCity.setBuildingCommerceChange(eMarktClass, CommerceTypes.COMMERCE_GOLD, iStandard + iVerlust)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_1_OUTCOME",()))
			popupInfo.addPopup(iAthen)
		if gc.getPlayer(iNordIonien).isHuman() and bNordIsVassal:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_1_OUTCOME_UPPER_IONIEN",()))
			popupInfo.addPopup(iNordIonien)
		if gc.getPlayer(iSuedIonien).isHuman() and bSuedIsVassal:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_1_OUTCOME_LOWER_IONIEN",()))
			popupInfo.addPopup(iSuedIonien)
	elif iButtonId == 1:
		# Kultur fuer Athen in Megara
		pPlotMegara = gc.getMap().plot(55,30)
		pPlotMegara.changeCulture(iAthen, 500, 1)
		# Verbesserung der Beziehungen
		gc.getPlayer(iKorinth).AI_changeAttitudeExtra(iAthen, 2)
		gc.getPlayer(iAthen).AI_changeAttitudeExtra(iKorinth, 2)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_2_OUTCOME",()))
			popupInfo.addPopup(iAthen)
		if gc.getPlayer(iKorinth).isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_2_OUTCOME_KORINTH",()))
			popupInfo.addPopup(iKorinth)
	elif iButtonId == 2:
		# Verschlechterung der Beziehungen zu Sparta und Theben
		gc.getPlayer(iSparta).AI_changeAttitudeExtra(iAthen, -6)
		gc.getPlayer(iTheben).AI_changeAttitudeExtra(iAthen, -6)
		if bIsHuman:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_ATHEN_OPTION_3_OUTCOME",()))
			popupInfo.addPopup(iAthen)

def Megara2(argsList):
		iButtonId = argsList[0]
		iAthen = 0
		iSparta = 1
		iKorinth = 2
		iTheben = 4
		pSparta = gc.getPlayer(iSparta)
		bIsHuman = pSparta.isHuman()
		if iButtonId == 0:
			iRand = CvUtil.myRandom(2, "pelo_1")
			if not gc.getTeam(iSparta).canDeclareWar(iAthen):
				if bIsHuman:
					# Kein Krieg moeglich -> Kein Gold/Bronze
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_1_NO_WAR_POSSIBLE",()))
					popupInfo.addPopup(iSparta)
			# Wenig Gold
			elif iRand == 0:
				pSparta.changeGold(200)
				gc.getTeam(iSparta).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_1_OUTCOME_LOW",()))
					popupInfo.addPopup(iSparta)
			# Viel Gold
			elif iRand == 1:
				pSparta.changeGold(1000)
				gc.getTeam(iSparta).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_1_OUTCOME_HIGH",()))
					popupInfo.addPopup(iSparta)
			# 10 Bronze
			else:
				# 10 freie Bronze in der Hauptstadt -> in allen Staedten am Handelsnetz verfuegbar
				gc.getTeam(iSparta).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
				iNumCities = pSparta.getNumCities()
				eBronze = gc.getInfoTypeForString("BONUS_BRONZE")
				pCapital = pSparta.getCapitalCity()
				pCapital.changeFreeBonus(eBronze, 10)
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_1_OUTCOME_BRONZE",()))
					popupInfo.addPopup(iSparta)
		elif iButtonId == 1:
			iRand = CvUtil.myRandom(1, "pelo_2")
			if not gc.getTeam(iTheben).canDeclareWar(iAthen):
				iRand = 1 # Theben kann nicht
			# Theben ist einverstanden -> Krieg
			if iRand == 0:
				if gc.getTeam(iSparta).canDeclareWar(iAthen):
					gc.getTeam(iSparta).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
					gc.getTeam(iTheben).declareWar(iAthen, 0, 5)
					if bIsHuman:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_2_OUTCOME_SUCCESS",()))
						popupInfo.addPopup(iSparta)
					if gc.getTeam(iTheben).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_2_OUTCOME_SUCCESS_THEBEN",()))
						popupInfo.addPopup(iTheben)
				elif bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_2_NO_WAR_POSSIBLE",()))
					popupInfo.addPopup(iSparta)
			else:
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_2_OUTCOME_FAILED",()))
					popupInfo.addPopup(iSparta)
		elif iButtonId == 2:
			gc.getPlayer(iKorinth).AI_changeAttitudeExtra(iSparta, -3)
			if gc.getTeam(iSparta).canDeclareWar(iAthen):
				# Sparta und Theben ziehen gemeinsam in den Krieg
				if gc.getTeam(iTheben).canDeclareWar(iAthen):
					gc.getTeam(iTheben).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
					gc.getTeam(iSparta).declareWar(iAthen, 0, 5)
					if gc.getTeam(iTheben).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3_OUTCOME_THEBEN",()))
						popupInfo.addPopup(iTheben)
					if bIsHuman:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3_OUTCOME_SPARTA",()))
						popupInfo.addPopup(iSparta)
					if gc.getTeam(iKorinth).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3_OUTCOME_KORINTH",()))
						popupInfo.addPopup(iKorinth)
				# Theben hat Friedensvertrag mit Athen
				elif gc.getTeam(iSparta).canDeclareWar(iAthen):
					gc.getTeam(iSparta).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
					if gc.getTeam(iSparta).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3_OUTCOME_SPARTA_NO_THEBEN",()))
						popupInfo.addPopup(iSparta)
					if gc.getTeam(iKorinth).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3_OUTCOME_KORINTH_NO_THEBEN",()))
						popupInfo.addPopup(iKorinth)
			elif bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MEGARA_SPARTA_OPTION_3_NO_WAR_POSSIBLE",()))
				popupInfo.addPopup(iSparta)


def Plataiai1(argsList):
	iButtonId = argsList[0]
	iAthen = 0
	iTheben = 4
	pTheben = gc.getPlayer(iTheben)
	iX = 55
	iY = 33
	pPlotPlataiai = CyMap().plot(iX, iY)
	bIsHuman = pTheben.isHuman()
	bAthenIsHuman = gc.getPlayer(iAthen).isHuman()
	# Unabhaengig von Auswahloption wird Krieg erklaert
	bWar = False
	if gc.getTeam(iTheben).canDeclareWar(iAthen):
		gc.getTeam(iTheben).declareWar(iAthen, 0, 5) # WARPLAN_TOTAL
		bWar = True
	# Wird kein Krieg erklaert, passiert nichts
	if bWar:
		if iButtonId == 0:
			iRand = CvUtil.myRandom(2, "pelo_3")
			# Klein
			if iRand == 0:
				iCultTheben = pPlotPlataiai.getCulture(iTheben)
				iCultAthen = pPlotPlataiai.getCulture(iAthen)
				# Garantieren, dass Theben den Plot besitzt
				pPlotPlataiai.changeCulture(iTheben, iCultAthen, 1)
				eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
				pTheben.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_1_OUTCOME_LOW",()))
					popupInfo.addPopup(iTheben)
				if bAthenIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_1_OUTCOME_LOW_ATHEN",()))
					popupInfo.addPopup(iAthen)
			# Mittel
			elif iRand == 1:
				# Athen erhaelt Plot und 1 Hoplit
				eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
				iCultTheben = pPlotPlataiai.getCulture(iTheben)
				iCultAthen = pPlotPlataiai.getCulture(iAthen)
				pPlotPlataiai.changeCulture(iAthen, iCultTheben, 1)
				gc.getPlayer(iAthen).initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				eSkirmisher = gc.getInfoTypeForString("UNIT_SKIRMISHER")
				eHorseman = gc.getInfoTypeForString("UNIT_HORSEMAN")
				for _ in xrange(5):
					pTheben.initUnit(eHoplit, iX-1, iY-1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(3):
					pTheben.initUnit(eSkirmisher, iX-1, iY-1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pTheben.initUnit(eHorseman, iX-1, iY-1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_1_OUTCOME_MEDIUM",()))
					popupInfo.addPopup(iTheben)
				if bAthenIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_1_OUTCOME_MEDIUM_ATHEN",()))
					popupInfo.addPopup(iAthen)
			elif iRand == 2:
				# Theben erhaelt Plot und grosse Armee
				iCultTheben = pPlotPlataiai.getCulture(iTheben)
				iCultAthen = pPlotPlataiai.getCulture(iAthen)
				pPlotPlataiai.changeCulture(iTheben, iCultAthen, 1)
				eSkirmisher = gc.getInfoTypeForString("UNIT_SKIRMISHER")
				eHorseman = gc.getInfoTypeForString("UNIT_HORSEMAN")
				eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
				eSupply = gc.getInfoTypeForString("UNIT_SUPPLY_WAGON")
				eGeneral = gc.getInfoTypeForString("UNIT_GREAT_GENERAL")
				for _ in xrange(10):
					pTheben.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(5):
					pTheben.initUnit(eSkirmisher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(4):
					pTheben.initUnit(eHorseman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(2):
					pTheben.initUnit(eGeneral, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pUnit = pTheben.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				PAE_Unit.setSupply(pUnit,200)
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_1_OUTCOME_HIGH",()))
					popupInfo.addPopup(iTheben)
				if bAthenIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_1_OUTCOME_HIGH_ATHEN",()))
					popupInfo.addPopup(iAthen)
		elif iButtonId == 1:
			# Athen erhaelt Plot und 1 Hoplit
			eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
			iCultTheben = pPlotPlataiai.getCulture(iTheben)
			iCultAthen = pPlotPlataiai.getCulture(iAthen)
			pPlotPlataiai.changeCulture(iAthen, iCultTheben, 1)
			gc.getPlayer(iAthen).initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_2_OUTCOME",()))
				popupInfo.addPopup(iTheben)
			if bAthenIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_2_OUTCOME_ATHEN",()))
				popupInfo.addPopup(iAthen)
		elif iButtonId == 2:
			iAthenX = 57
			iAthenY = 30
			pAthenCity = CyMap().plot(iAthenX, iAthenY).getPlotCity()
			if pAthenCity and not pAthenCity.isNone():
				if pAthenCity.getOwner() == iAthen:
					# Fluechtlinge
					pAthenCity.changePopulation(1)
					if bIsHuman:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_3_OUTCOME",()))
						popupInfo.addPopup(iTheben)
					if bAthenIsHuman:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_3_OUTCOME_ATHEN",()))
						popupInfo.addPopup(iAthen)
				else:
					if bIsHuman:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_3_OUTCOME_NO_ATHEN",()))
						popupInfo.addPopup(iTheben)
					if bAthenIsHuman:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_3_OUTCOME_NO_ATHEN_ATHEN",()))
						popupInfo.addPopup(iAthen)
			else:
				if bIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_3_OUTCOME_NO_ATHEN",()))
					popupInfo.addPopup(iTheben)
				if bAthenIsHuman:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_OPTION_3_OUTCOME_NO_ATHEN_ATHEN",()))
					popupInfo.addPopup(iAthen)
	elif bIsHuman:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_PLATAIAI_NO_WAR",()))
		popupInfo.addPopup(iTheben)

def Syra1(argsList):
	iButtonId = argsList[0]
	iAthen = 0
	pAthen = gc.getPlayer(iAthen)
	iSyrakus = 16
	bIsHuman = pAthen.isHuman()
	bWar = gc.getTeam(iAthen).canDeclareWar(iSyrakus)
	eTrireme = gc.getInfoTypeForString("UNIT_TRIREME")
	eBireme = gc.getInfoTypeForString("UNIT_BIREME")
	eHoplit = gc.getInfoTypeForString("UNIT_HOPLIT")
	eHippeus = gc.getInfoTypeForString("UNIT_ELITE_HOPLIT")
	eSupply = gc.getInfoTypeForString("UNIT_SUPPLY_WAGON")
	eRam = gc.getInfoTypeForString("UNIT_BATTERING_RAM")
	eArcher = gc.getInfoTypeForString("UNIT_ARCHER")
	eSpy = gc.getInfoTypeForString("UNIT_SPY")
	eHorseman = gc.getInfoTypeForString("UNIT_HORSEMAN")
	eRang1 = gc.getInfoTypeForString("PROMOTION_COMBAT1")
	eRang2 = gc.getInfoTypeForString("PROMOTION_COMBAT2")
	eRang3 = gc.getInfoTypeForString("PROMOTION_COMBAT3")
	eRang4 = gc.getInfoTypeForString("PROMOTION_COMBAT4")
	eRang5 = gc.getInfoTypeForString("PROMOTION_COMBAT5")
	eCityRaid1 = gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1")
	eFlank1 = gc.getInfoTypeForString("PROMOTION_FLANKING1")
	eFlank2 = gc.getInfoTypeForString("PROMOTION_FLANKING2")
	eHero = gc.getInfoTypeForString("PROMOTION_HERO")
	iX = 57
	iY = 30
	if bWar:
		gc.getTeam(iAthen).declareWar(iSyrakus, 0, 5) #WARPLAN_LIMITED
		if iButtonId == 0:
			iGold = pAthen.getGold()
			# Mind. 2500 Gold, max. 5000 Gold
			if iGold <= 2500:
				pAthen.changeGold(-2500)
			elif iGold <= 5000:
				pAthen.setGold(0)
			else:
				pAthen.changeGold(-5000)
			# Einheiten, die man immer erhaelt
			for _ in xrange(12):
				pAthen.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(1):
				pUnit = pAthen.initUnit(eHippeus, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pUnit.setHasPromotion(eRang1, True)
				pUnit.setHasPromotion(eRang2, True)
				pUnit.setHasPromotion(eRang3, True)
				pUnit.setHasPromotion(eRang4, True)
				pUnit.setHasPromotion(eRang5, True)
				pUnit.setHasPromotion(eHero, True)
				pUnit.setHasPromotion(eCityRaid1, True)
				pUnit.setName("Nikias")
			for _ in xrange(8):
				pUnit = pAthen.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pUnit.setHasPromotion(eRang1, True)
				pUnit.setHasPromotion(eRang2, True)
				pUnit.setHasPromotion(eRang3, True)
			for _ in xrange(8):
				pAthen.initUnit(eArcher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(12):
				pAthen.initUnit(eRam, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(4):
				pUnit = pAthen.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				PAE_Unit.setSupply(pUnit,200)
			for _ in xrange(2):
				pUnit = pAthen.initUnit(eHorseman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pUnit.setHasPromotion(eFlank1, True)
				pUnit.setHasPromotion(eFlank2, True)
			for _ in xrange(1):
				pAthen.initUnit(eSpy, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			# Ab 2500 zusaetzliche Einheiten fuer je 500 Gold (max. 5000 Gold)
			iPay = 2500
			for _ in xrange(5):
				iPay += 500
				if iPay > iGold:
					break
				for _ in xrange(2):
					pAthen.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(1):
					pAthen.initUnit(eBireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(3):
					pAthen.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pUnit.setHasPromotion(eRang1, True)
					pUnit.setHasPromotion(eRang2, True)
					pUnit.setHasPromotion(eRang3, True)
				for _ in xrange(2):
					pAthen.initUnit(eArcher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				for _ in xrange(1):
					pUnit = pAthen.initUnit(eHorseman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pUnit.setHasPromotion(eFlank1, True)
					pUnit.setHasPromotion(eFlank2, True)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				if iGold < 3000:
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_1_OUTCOME_LOW",()))
				elif iGold < 4000:
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_1_OUTCOME_MEDIUM",()))
				else:
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_1_OUTCOME_HIGH",()))
				popupInfo.addPopup(iAthen)
		elif iButtonId == 1:
			pAthen.changeGold(-2000)
			for _ in xrange(9):
					pAthen.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(8):
					pUnit = pAthen.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pUnit.setHasPromotion(eRang1, True)
					pUnit.setHasPromotion(eRang2, True)
			for _ in xrange(8):
					pAthen.initUnit(eArcher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(6):
					pAthen.initUnit(eRam, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(2):
					pUnit = pAthen.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					PAE_Unit.setSupply(pUnit,200)
			for _ in xrange(2):
					pUnit = pAthen.initUnit(eHorseman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pUnit.setHasPromotion(eFlank1, True)
					pUnit.setHasPromotion(eFlank2, True)
			for _ in xrange (1):
					pAthen.initUnit(eSpy, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_2_OUTCOME",()))
				popupInfo.addPopup(iAthen)
		elif iButtonId == 2:
			pAthen.changeGold(-1000)
			for _ in xrange(4):
				pAthen.initUnit(eTrireme, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(5):
				pUnit = pAthen.initUnit(eHoplit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pUnit.setHasPromotion(eRang1, True)
			for _ in xrange(4):
				pAthen.initUnit(eArcher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(2):
				pAthen.initUnit(eRam, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for _ in xrange(1):
				pUnit = pAthen.initUnit(eSupply, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				PAE_Unit.setSupply(pUnit,200)
			if bIsHuman:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_OPTION_3_OUTCOME",()))
				popupInfo.addPopup(iAthen)
	elif bIsHuman:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_SYRAKUS_ATHEN_NO_WAR",()))
		popupInfo.addPopup(iAthen)