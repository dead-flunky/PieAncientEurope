# Trade and Cultivation feature
# Trade and Cultivation feature
# From BoggyB
# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface, CyGame,
								CyTranslator, CyMap, DirectionTypes,
								ColorTypes, UnitAITypes, CyPopupInfo,
								ButtonPopupTypes, plotDirection,
								CyAudioGame, InterfaceDirtyBits,
								plotDistance, FontSymbols, DomainTypes,
								MissionTypes, MissionAITypes)
# import CvEventInterface
import CvUtil
import PAE_Unit
import PAE_Lists as L
import PAE_City

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

# Defines
gc = CyGlobalContext()

# Globals
bInitialized = False  # Whether global variables are already initialised
iMaxCitiesSpecialBonus = 3
iCitiesSpecialBonus = 0  # Cities with Special Trade Bonus

# Update (Ramk): CvUtil-Functions unpack an dict. You could directly use int, etc.

# Used keys for UnitScriptData:
# "x"/"y": coordinates of plots where bonus was picked up (merchants)
# "b": index of bonus stored in merchant/cultivation unit (only one at a time)
# "originCiv": original owner of the bonus stored in merchant (owner of the city where it was bought)

# For automated trade routes:
# "autX1"/"autX2"/"autY1"/"autY2": coordinates of cities in trade route
# "autB1": bonus bought in city 1/sold in city 2
# "autB2": bonus bought in city 2/sold in city 1
# "autA": if False, automated route is currently inactive
# "autLTC": latest turn when "doAutomateMerchant" was called for this unit. Sometimes it is called multiple times per turn, this prevents unnecessary calculations

# Used keys for CityScriptData:
# "b": free bonuses acquired via turns and until which turn they are available,
# e.g. {43:4, 23:8, 12:10} key: bonus index (int), value: num turns (int)


def init():
	global bInitialized
	global iCitiesSpecialBonus
	global iMaxCitiesSpecialBonus

	if not bInitialized:
		# Cities mit Special Trade Bonus herausfinden
		iRange = gc.getMAX_PLAYERS()
		for i in xrange(iRange):
			loopPlayer = gc.getPlayer(i)
			if loopPlayer.isAlive() and not loopPlayer.isBarbarian():
				(loopCity, pIter) = loopPlayer.firstCity(False)
				while loopCity:
					if not loopCity.isNone() and loopCity.getOwner() == loopPlayer.getID():  # only valid cities
						if CvUtil.getScriptData(loopCity, ["tsb"], -1) != -1:
							iCitiesSpecialBonus += 1
							if iCitiesSpecialBonus == iMaxCitiesSpecialBonus:
								break
					(loopCity, pIter) = loopPlayer.nextCity(pIter, False)
			if iCitiesSpecialBonus == iMaxCitiesSpecialBonus:
				break
		bInitialized = True

# --- Trade in cities ---

# Unit stores bonus, owner pays, if UnitOwner != CityOwner: city owner gets money


def doBuyBonus(pUnit, eBonus, iCityOwner):

	if not pUnit.getUnitType() in L.LTradeUnits:
		return

	if eBonus != -1:
		iBuyer = pUnit.getOwner()
		pBuyer = gc.getPlayer(iBuyer)

		eUnitBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
		if eBonus == eUnitBonus:
			#CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Das haben wir bereits geladen.",)), None, 2, None, ColorTypes(10), 0, 0, False, False)
			return
		if eUnitBonus != -1:
			# Geladene Ressource automatisch verkaufen
			#CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Die Einheit hat bereits eine Ressource geladen.",)), None, 2, None, ColorTypes(10), 0, 0, False, False)
			if pUnit.plot().isCity():
				doSellBonus(pUnit, pUnit.plot().getPlotCity())
			else:
				CvUtil.removeScriptData(pUnit, "b")

		iPrice = int(_calculateBonusBuyingPrice(eBonus, iBuyer, iCityOwner))
		if pBuyer.getGold() < iPrice:
			CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_COLLECT_NO_GOODS", ("",)),
				None, 2, "Art/Interface/PlotPicker/Warning.dds", ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
			return
		pBuyer.changeGold(-iPrice)

		iGewinnGold = iPrice

		pSeller = gc.getPlayer(iCityOwner)
		if iBuyer != iCityOwner:
			# 20%
			iGewinnGold = int(iPrice / 5)  # * pSeller.getCurrentEra())
			pSeller.changeGold(iGewinnGold)

		CvUtil.addScriptData(pUnit, "b", eBonus)
		CvUtil.addScriptData(pUnit, "originCiv", iCityOwner)
		CvUtil.addScriptData(pUnit, "x", pUnit.getX())
		CvUtil.addScriptData(pUnit, "y", pUnit.getY())
		if pSeller.isHuman() and iBuyer != iCityOwner:
			sBonusName = gc.getBonusInfo(eBonus).getDescription()
			CyInterface().addMessage(iCityOwner, True, 10, CyTranslator().getText("TXT_KEY_BONUS_BOUGHT", (pBuyer.getName(), pBuyer.getCivilizationShortDescriptionKey(),
				pUnit.plot().getPlotCity().getName(), sBonusName, iGewinnGold)), "AS2D_COINS", 2, pUnit.getButton(), ColorTypes(8), pUnit.getX(), pUnit.getY(), True, True)

		if pBuyer.isHuman():
			CyInterface().addMessage(iBuyer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_COLLECT_GOODS",
				(gc.getBonusInfo(eBonus).getDescription(), -iPrice)), "AS2D_COINS", 2, None, ColorTypes(13), 0, 0, False, False)

		pUnit.finishMoves()
		if pUnit.isHuman():
			PAE_Unit.doGoToNextUnit(pUnit)


def doSellBonus(pUnit, pCity):
	"""Unit's store is emptied, unit owner gets money, city gets bonus, research push"""
	eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
	if eBonus != -1:
		iPrice = int(calculateBonusSellingPrice(pUnit, pCity, 0))
		iBuyer = pCity.getOwner()
		pBuyer = gc.getPlayer(iBuyer)
		iSeller = pUnit.getOwner()
		pSeller = gc.getPlayer(iSeller)

		pSeller.changeGold(iPrice)
		sBonusName = gc.getBonusInfo(eBonus).getDescription()

		# default: iSeller weil auch der Getreidekarren sein Gut abladen kann
		iOriginCiv = CvUtil.getScriptData(pUnit, ["originCiv"], iSeller)  # where the goods come from
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Trade: OriginCiv: " + str(iOriginCiv) + " | Buyer: " + str(iBuyer) + " | " + pSeller.getName() + " | " + gc.getBonusInfo(eBonus).getDescription(), None, 2, None, ColorTypes(8), 0, 0, False, False)

		# Forschungbonus
		iGewinnWissen = 0
		# Handelsstrasse
		# City Free Bonus
		# Bonus Spezialauftrag

		if iOriginCiv != iBuyer:
			iGewinnWissen = int((iPrice / 10) * pSeller.getCurrentEra())
			_doResearchPush(iBuyer, iGewinnWissen)

			# Trade route / Handelsstrasse
			doBuildTradeRoad(pUnit, pCity)

			_doCityProvideBonus(pCity, eBonus, 3)

			# Special Order Check
			if eBonus in L.LBonusLuxury + L.LBonusRarity:
				_doCheckCitySpecialBonus(pUnit, pCity, eBonus)

			# Buyer bekommt +1 zum Seller: 5%
			if not pBuyer.isHuman() and eBonus in L.LBonus4Units and not pBuyer.hasBonus(eBonus):
				if CvUtil.myRandom(20, "LBonus4Units") == 1:
					pBuyer.AI_changeAttitudeExtra(iSeller, 1)
					if pSeller.isHuman():
						CyInterface().addMessage(iSeller, True, 10, CyTranslator().getText("TXT_KEY_BONUS_SOLD3", (pBuyer.getName(),
							pBuyer.getCivilizationShortDescriptionKey(), sBonusName)), None, 2, None, ColorTypes(13), pUnit.getX(), pUnit.getY(), False, False)

		if pBuyer.isHuman() and iBuyer != iSeller:
			CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_BONUS_SOLD", (pSeller.getName(), pSeller.getCivilizationShortDescriptionKey(),
				pCity.getName(), sBonusName, iGewinnWissen)), None, 2, None, ColorTypes(8), pUnit.getX(), pUnit.getY(), False, False)
		elif pSeller.isHuman():
			CyInterface().addMessage(iSeller, True, 10, CyTranslator().getText("TXT_KEY_BONUS_SOLD2", (pCity.getName(), pBuyer.getCivilizationShortDescriptionKey(),
				sBonusName, iPrice, iGewinnWissen)), None, 2, None, ColorTypes(8), pUnit.getX(), pUnit.getY(), False, False)

		# Coin sound
		if iSeller == gc.getGame().getActivePlayer() or iBuyer == gc.getGame().getActivePlayer():
			CyAudioGame().Play2DSound("AS2D_COINS")

		CvUtil.removeScriptData(pUnit, "b")
		# pUnit.finishMoves()
		# PAE_Unit.doGoToNextUnit(pUnit)

		# Dertuek : Refresh the unit info panel
		CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, True)

# Handelsstrasse erstellen


def doBuildTradeRoad(pUnit, pCity):
	# Inits
	eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
	iBuyer = pCity.getOwner()
	pBuyer = gc.getPlayer(iBuyer)
	iSeller = pUnit.getOwner()
	pSeller = gc.getPlayer(iSeller)

	#iTech = gc.getInfoTypeForString("TECH_THE_WHEEL2")
	# if not gc.getTeam(pBuyer.getTeam()).isHasTech(iTech) or not gc.getTeam(pSeller.getTeam()).isHasTech(iTech): return

	# Chance
	if pBuyer.hasBonus(eBonus):
		iChance = 10
	else:
		iChance = 25
	# wenn die Stadt den Bonus bereits hat
	if CvUtil.hasBonusIgnoreFreeBonuses(pCity, eBonus):
		iChance -= 10
	# Better resources increase chance
	if eBonus in L.LBonusLuxury:
		iChance += 15
	elif eBonus in L.LBonusRarity:
		iChance += 25

	iRand = CvUtil.myRandom(100, "Handelsstrasse")
	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Trade Route: " + str(iRand) + " : " + str(iChance) + " | " + pSeller.getName(), None, 2, None, ColorTypes(8), 0, 0, False, False)
	#iChance = 100
	if iRand <= iChance:
		iRouteType = gc.getInfoTypeForString("ROUTE_TRADE_ROAD")
		iRouteType2 = gc.getInfoTypeForString("ROUTE_RAILROAD")  # Roman Road
		pCity2 = None

		# Schiffe: Hafenstadt -> Hauptstadt
		if pUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA"):
			pCity2 = pBuyer.getCapitalCity()
			pSource = pCity2.plot()
			# Nur zur Hauptstadt, wenn diese in einem bestimmten Bereich liegt
			#  0 = WORLDSIZE_DUEL
			#  1 = WORLDSIZE_TINY
			#  2 = WORLDSIZE_SMALL
			#  3 = WORLDSIZE_STANDARD
			#  4 = WORLDSIZE_LARGE
			#  5 = WORLDSIZE_HUGE
			iMapSize = gc.getMap().getWorldSize()
			iDistance = gc.getMap().calculatePathDistance(pCity.plot(), pSource)
			if iDistance == -1 or iDistance > 8 + iMapSize * 2:
				pSource = None
		# Landeinheiten: Stadt A -> B
		else:
			iOriginX = CvUtil.getScriptData(pUnit, ["x"], -1)
			iOriginY = CvUtil.getScriptData(pUnit, ["y"], -1)
			pSource = CyMap().plot(iOriginX, iOriginY)
		pDest = pCity.plot()

		if pSource is not None and not pSource.isNone():
			if pSource.isCity():
				#CyInterface().addMessage(iSeller, True, 10, "Vor Traderoute", None, 2, None, ColorTypes(8), pUnit.getX(), pUnit.getY(), False, False)
				pPlotTradeRoad = getPlotTradingRoad(pSource, pDest)
				if pCity2 == None:
					pCity2 = pSource.getPlotCity()

				# Debug
				# if pPlotTradeRoad == None:
				#     CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Keine Handelsstrasse moeglich.", None, 2, "Art/Terrain/Routes/handelsstrasse/button_handelsstrasse.dds", ColorTypes(10), -1, -1, False, False)
				# else:
				#    sz = "TRADEROAD x|y: " + str(pPlotTradeRoad.getX()) + "|" + str(pPlotTradeRoad.getY())
				#    CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, sz, None, 2, "Art/Terrain/Routes/handelsstrasse/button_handelsstrasse.dds", ColorTypes(10), pPlotTradeRoad.getX(), pPlotTradeRoad.getY(), True, True)
				# CyInterface().addMessage(iSeller, True, 10, "Nach Traderoute", None, 2, None, ColorTypes(8), pUnit.getX(), pUnit.getY(), False, False)

				if pPlotTradeRoad != None:
					pPlotTradeRoad.setRouteType(iRouteType)
					if pBuyer.isHuman():
						CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_TRADE_ROUTE_BUILT", (pSeller.getName(), pSeller.getCivilizationShortDescriptionKey(), pCity.getName(),
							pCity2.getName())), "AS2D_WELOVEKING", 2, "Art/Terrain/Routes/handelsstrasse/button_handelsstrasse.dds", ColorTypes(10), pPlotTradeRoad.getX(), pPlotTradeRoad.getY(), True, True)
					if pSeller.isHuman() and iBuyer != iSeller:
						CyInterface().addMessage(iSeller, True, 10, CyTranslator().getText("TXT_KEY_TRADE_ROUTE_BUILT2", (pCity.getName(), pCity2.getName())), "AS2D_WELOVEKING",
							2, "Art/Terrain/Routes/handelsstrasse/button_handelsstrasse.dds", ColorTypes(10), pPlotTradeRoad.getX(), pPlotTradeRoad.getY(), True, True)
					if iBuyer != iSeller and iSeller == gc.getGame().getActivePlayer() or iBuyer == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound("AS2D_WELOVEKING")

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Handelsroute erstellt", None, 2, "Art/Terrain/Routes/handelsstrasse/button_handelsstrasse.dds", ColorTypes(10), pPlotTradeRoad.getX(), pPlotTradeRoad.getY(), True, True)

		# Sobald von einer Stadt 3 Handelsstrassen (bzw 2 bei einer Kuestenstadt) weggehen,
		# wird es zum Handelszentrum (Building: 100% auf Trade Routes)
		iBuilding = gc.getInfoTypeForString("BUILDING_HANDELSZENTRUM")
		if not pCity.isHasBuilding(iBuilding):
			iAnz = 0
			iMax = 3
			if pCity.isCoastal(4):
				iMax = 2
			for i in xrange(8):
				pLoopPlot = plotDirection(pCity.getX(), pCity.getY(), DirectionTypes(i))
				if pLoopPlot is not None and not pLoopPlot.isNone():
					if pLoopPlot.getRouteType() == iRouteType or pLoopPlot.getRouteType() == iRouteType2:
						iAnz += 1
					if iAnz >= iMax:
						break
			if iAnz >= iMax:
				pCity.setNumRealBuilding(iBuilding, 1)
				if pCity.getOwner() == gc.getGame().getActivePlayer():
					CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_TRADE_ROUTE_HANDELSZENTRUM", (pCity.getName(),)),
						"AS2D_WELOVEKING", 2, gc.getBuildingInfo(iBuilding).getButton(), ColorTypes(10), pCity.getX(), pCity.getY(), True, True)

# Gibt Plot zurueck, auf dem das naechste Handelsstrassen-Stueck entstehen soll bzw. ob die Strasse schon fertig ist. Von Pie.


def getPlotTradingRoad(pSource, pDest):
	# Nur auf gleichem Kontinent
	if pSource.getArea() == pDest.getArea():
		iSourceX = pSource.getX()
		iSourceY = pSource.getY()
		iDestX = pDest.getX()
		iDestY = pDest.getY()

		# Die nähesten 3 Plots zur Source-Stadt
		p = [None, None, None]
		# Ob diese Hills sind
		h = [0, 0, 0]

		# wenn pSource = pTarget (Haendler ueber Schiff im Hafen)
		if iSourceX != iDestX or iSourceY != iDestY:
			iTradeRoad = gc.getInfoTypeForString("ROUTE_TRADE_ROAD")
			iTradeRoad2 = gc.getInfoTypeForString("ROUTE_RAILROAD")  # Roman Road
			bSourceGerade = False
			# bTradeRoute = False

			# Wenn die Stadt noch keine Handelsstrasse hat
			if pDest.getRouteType() != iTradeRoad and pDest.getRouteType() != iTradeRoad2:
				return pDest

			# Update 6.10 - Liegt eine Stadt im Vektorbereich, wird diese die temporäre Destination (sofern sie noch keine Handelsstraße hat)
			iX = iSourceX
			iY = iSourceY
			if iDestX > iSourceX:
				i = 1
			else:
				i = -1
			if iDestY > iSourceY:
				j = 1
			else:
				j = -1
			bBreak = False
			while iX != iDestX:
				iY = iSourceY
				bNoRoadOnYAxis = True
				while iY != iDestY:
					loopPlot = gc.getMap().plot(iX, iY)
					if not loopPlot.isNone():
						if not loopPlot.isPeak() and not loopPlot.isWater():

							if loopPlot.isCity():
								# wenn die Stadt keine Handelsstrasse hat, is sie fix
								# oder wenn sie eine hat, aber noch keine von der Quelle hinführt
								if not (loopPlot.getRouteType() == iTradeRoad or loopPlot.getRouteType() == iTradeRoad2) or bNoRoadOnYAxis:
									pDest = loopPlot
									iDestX = pDest.getX()
									iDestY = pDest.getY()
									bBreak = True
									break

							# gibt es bereits eine Strasse an der Y-Achse dieses Vektorbereichs?
							if loopPlot.getRouteType() == iTradeRoad or loopPlot.getRouteType() == iTradeRoad2:
								bNoRoadOnYAxis = False

					iY += j
				if bBreak:
					break
				iX += i

			# Herausfinden, ob bei pSource eine GERADE Strasse gebaut wurde
			# um zu verhindern, dass 2 Routen erstellt werden:
			#-------#
			#   --X #
			#  / /  #
			# X--   #
			#-------#
			# wenn es noch keine Strasse in der Stadt gibt => egal
			# wenn es eine Strasse gibt, dann den Umkreis checken
			if pSource.getRouteType() == iTradeRoad or pSource.getRouteType() == iTradeRoad2:
				iBest = 0
				for i in xrange(3):
					for j in xrange(3):
						loopPlot = gc.getMap().plot(iSourceX + i - 1, iSourceY + j - 1)
						if not loopPlot.isNone():
							if loopPlot.getRouteType() == iTradeRoad or loopPlot.getRouteType() == iTradeRoad2:
								iTmp = gc.getMap().calculatePathDistance(loopPlot, pDest)
								if iBest == 0:
									iBest = iTmp

								if iTmp == iBest and (i == 1 or j == 1):
									bSourceGerade = True
								elif iTmp < iBest:
									bSourceGerade = (i == 1 or j == 1)

			# Den naechsten Plot fuer die Handelsstrasse herausfinden
			iBestX = iDestX
			iBestY = iDestY
			pBest = None
			while iBestX != iSourceX or iBestY != iSourceY:
				i = 0
				j = 0
				iBest = 0
				for i in xrange(3):
					for j in xrange(3):
						iX = iBestX + i - 1
						iY = iBestY + j - 1
						loopPlot = gc.getMap().plot(iX, iY)
						if not loopPlot.isNone():
							if not loopPlot.isPeak() and not loopPlot.isWater():
								# nur Plot mit Strasse zulassen
								# if loopPlot.getRouteType() != -1:
								iTmp = gc.getMap().calculatePathDistance(loopPlot, pSource)

								# Debug
								#sz = "S:" + str(iSourceX)+"|"+str(iSourceY) + " D:" + str(iDestX)+"|"+str(iDestY)
								#sz += " x|y:" + str(iX) + "|" + str(iY)
								#sz += " iTmp:" + str(iTmp) + " iBest:" + str(iBest) + " bSG:" + str(bSourceGerade) + " bTR:" + str(bTradeRoute)
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, sz, None, 2, "", ColorTypes(10), 0, 0, 0, 0)

								# Beenden, wenn kein Weg moeglich
								if iTmp == -1:
									return None
								# wenn Distanz null ist, wurde der letzte Plot gefunden
								elif iTmp == 0:
									if loopPlot.getRouteType() == iTradeRoad or loopPlot.getRouteType() == iTradeRoad2:
										return None
									return loopPlot

								if iBest == 0 or iTmp < iBest:
									iBest = iTmp
									pBest = loopPlot
									p = [loopPlot, None, None]
									if loopPlot.isHills():
										h[0] = 1
								elif iTmp == iBest:
									if p[1] == None:
										p[1] = loopPlot
										if loopPlot.isHills():
											h[1] = 1
									elif p[2] == None:
										p[2] = loopPlot
										if loopPlot.isHills():
											h[2] = 1

				if pBest == None:
					return None
				# Staedte immer bevorzugen
				elif p[0] != None and p[0].isCity():
					pBest = p[0]
				elif p[1] != None and p[1].isCity():
					pBest = p[1]
				elif p[2] != None and p[2].isCity():
					pBest = p[2]
				else:
					# Plots mit Hills ausnehmen
					if not ((p[0] == None or h[0]) and (p[1] == None or h[1]) and (p[2] == None or h[2])) or not (not h[0] and not h[1] and not h[2]):
						if h[0]:
							p[0] = None
						if h[1]:
							p[1] = None
						if h[2]:
							p[2] = None

					# Bei gleichen Entfernungen (max. 3 Moeglichkeiten: schraeg - gerade (- schraeg))
					# Wenn bei der Quelle eine GERADE Strasse verlaeuft, dann schraeg bauen. Sonst umgekehrt.
					if p[1] != None and not bSourceGerade:
						pBest = p[1]
					# wenn es nur mehr gerade zur Stadt geht (= ignoriert Hills)
					# elif p[0] != None and (p[0].getX() == iSourceX or p[0].getY() == iSourceY): pBest = p[0]
					# elif p[1] != None and (p[1].getX() == iSourceX or p[1].getY() == iSourceY): pBest = p[1]
					# elif p[2] != None and (p[2].getX() == iSourceX or p[2].getY() == iSourceY): pBest = p[2]
					else:
						if p[0] != None:
							pBest = p[0]
						if p[1] != None and (abs(pBest.getX() - iSourceX) > abs(p[1].getX() - iSourceX) or abs(pBest.getY() - iSourceY) > abs(p[1].getY() - iSourceY)):
							pBest = p[1]
						if p[2] != None and (abs(pBest.getX() - iSourceX) > abs(p[2].getX() - iSourceX) or abs(pBest.getY() - iSourceY) > abs(p[2].getY() - iSourceY)):
							pBest = p[2]

				if pBest.getRouteType() != iTradeRoad and pBest.getRouteType() != iTradeRoad2:
					return pBest

				iBestX = pBest.getX()
				iBestY = pBest.getY()
	return None

# Player gets research points for current project (called when foreign goods are sold to player's cities)


def _doResearchPush(iPlayer1, iValue1):
	pPlayer1 = gc.getPlayer(iPlayer1)
	pTeam1 = gc.getTeam(pPlayer1.getTeam())
	eTech1 = pPlayer1.getCurrentResearch()
	if eTech1 != -1:
		pTeam1.changeResearchProgress(eTech1, iValue1, iPlayer1)

# City can use bonus for x turns
def _doCityProvideBonus(pCity, eBonus, iTurn):
	# ScriptData value is dict, e.g. {43:4; 23:8; 12:10}
	# Key is 'iBonus' and value is 'iTurns'
	bonusDict = CvUtil.getScriptData(pCity, ["b"], {})

	# compatibility
	if isinstance(bonusDict, str):
		# Konvertiere altes Format "iB,iTurn;..." in dict
		tmp = [paar.split(",") for paar in str(bonusDict).split(";")]
		bonusDict = dict([map(int, pair) for pair in tmp])

	if str(eBonus) not in bonusDict:
		pCity.changeFreeBonus(eBonus, 1)

	# Addiere alten und neuen Rundenwert
	iCurrentTurn = gc.getGame().getGameTurn()

	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "1 dict string: " + str(bonusDict), None, 2, None, ColorTypes(8), 0, 0, False, False)

	iTurn += iCurrentTurn
	dictNew = {str(eBonus): iTurn}
	bonusDict.update(dictNew)

	#bonusDict[eBonus] = iTurn + bonusDict.setdefault(eBonus, iCurrentTurn)
	#bonusDict[eBonus] = iTurn + iCurrentTurn
	CvUtil.addScriptData(pCity, "b", bonusDict)

	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "2 dict string: " + str(bonusDict), None, 2, None, ColorTypes(8), 0, 0, False, False)


# Called each turn (onCityDoTurn, EventManager), makes sure free bonus disappears after x turns
def doCityCheckFreeBonuses(pCity):
	bonusDict = CvUtil.getScriptData(pCity, ["b"], {})
	bUpdate = False
	# compatibility
	if isinstance(bonusDict, str):
		# Konvertiere altes Format "iB,iTurn;..." in dict
		tmp = [paar.split(",") for paar in str(bonusDict).split(";")]
		bonusDict = dict([map(int, pair) for pair in tmp])
		bUpdate = True

	lRemove = []
	lAdd = {}
	for eBonus in bonusDict:
		iTurn = bonusDict[eBonus]

		# alte Saves korrigieren str->int
		if isinstance(eBonus, str):
			lRemove.append(eBonus)
			eBonus = int(eBonus)
			lAdd[eBonus] = iTurn

		if iTurn <= gc.getGame().getGameTurn():
			pCity.changeFreeBonus(eBonus, -1)  # Time over: remove bonus from city
			lRemove.append(eBonus)
			bUpdate = True

	# alte Saves korrigieren str->int
	bonusDict.update(lAdd)

	for eBonus in lRemove:
		bonusDict.pop(eBonus, None)
	if bUpdate:
		CvUtil.addScriptData(pCity, "b", bonusDict)

	# Bonusgüter auf einsamen 1-Feld-Inseln (redge)
	addUnreachableBonusesToCity(pCity)

# ---------------------------------------------------------------
# Feature von redge
# Bsp: 1-Feld-Inseln: Bonusresourcen mit Wirtschaftsmodernisierungen sind nicht im Handelsnetz


def addUnreachableBonusesToCity(pCity):

	# nur mit Handelsposten möglich
	if not pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_TRADEPOST")):
		return

	iCityTeam = pCity.getTeam()
	for i in xrange(gc.getNUM_CITY_PLOTS()):
		pLoopPlot = pCity.getCityIndexPlot(i)
		if pLoopPlot is not None and not pLoopPlot.isNone():

			# doch deaktiv weil Bsp: Bonus auf der Krim, Feind dazwischen.
			# if pLoopPlot.getArea() == pCity.plot().getArea(): continue

			if pLoopPlot.getRouteType() == -1:
				continue

			iBonus = pLoopPlot.getBonusType(iCityTeam)
			iImprovement = pLoopPlot.getImprovementType()

			if iBonus == -1 or iImprovement == -1:
				continue

			if pCity.hasBonus(iBonus):
				continue

			if gc.getImprovementInfo(iImprovement).isImprovementBonusMakesValid(iBonus):
				_doCityProvideBonus(pCity, iBonus, 1)
# ---------------------------------------------------

# Creates popup with all the affordable bonuses for UnitOwner (bonuses too expensive for UnitOwner are cut)
def doPopupChooseBonus(pUnit, pCity):
	if pCity is None or pCity.isNone() or pUnit is None or pUnit.isNone():
		return False

	iBuyer = pUnit.getOwner()

	# Dies soll doppelte Popups in PB-Spielen vermeiden.
	if iBuyer == gc.getGame().getActivePlayer():

		iSeller = pCity.getOwner()
		lGoods = getCitySaleableGoods(pCity, iBuyer)

		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_CHOOSE_BONUS", ("", )))
		popupInfo.setOnClickedPythonCallback("popupTradeChooseBonus")
		popupInfo.setData1(pUnit.getOwner())
		popupInfo.setData2(pUnit.getID())

		for eBonus in lGoods:
			sBonusDesc = gc.getBonusInfo(eBonus).getDescription()
			iPrice = _calculateBonusBuyingPrice(eBonus, iBuyer, iSeller)
			iBonusOwned = gc.getPlayer(iBuyer).getNumAvailableBonuses(eBonus)
			sText = CyTranslator().getText("TXT_KEY_BUY_BONUS", (sBonusDesc, iPrice, iBonusOwned))
			sBonusButton = gc.getBonusInfo(eBonus).getButton()
			popupInfo.addPythonButton(sText, sBonusButton)

		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
		popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
		popupInfo.addPopup(iBuyer)

# --- End of trade in cities

# --- Price stuff (trade) ---

# Basis value for each bonus
# auch in TXT_KEY_TRADE_ADVISOR_WERT_PANEL


def getBonusValue(eBonus):
	if eBonus == -1 or eBonus in L.LBonusUntradeable:
		return 0
	if eBonus in L.LBonusCorn + L.LBonusLivestock + L.LBonusPlantation:
		return 20
	elif eBonus in L.LBonusLuxury:
		return 40
	elif eBonus in L.LBonusRarity:
		return 50
	return 30  # strategic bonus ressource


# Price player pays for buying bonus
# Einkauf in eigener Stadt: Basiswert
# Einkauf in fremder Stadt: Basiswert + Haltung * 5%
def _calculateBonusBuyingPrice(eBonus, iBuyer, iSeller):
	if iBuyer == -1 or iSeller == -1:
		return -1
	iValue = getBonusValue(eBonus)
	if iBuyer == iSeller:
		return iValue
	else:
		# Vasallen ebenfalls iValue
		if gc.getTeam(gc.getPlayer(iSeller).getTeam()).isVassal(gc.getPlayer(iBuyer).getTeam()):
			return iValue

		# Furious = 0, Annoyed = 1, Cautious = 2, Pleased = 3, Friendly = 4
		iAttitudeModifier = 125 - 5 * gc.getPlayer(iBuyer).AI_getAttitude(iSeller)
	return (iValue * iAttitudeModifier) // 100


# Money player gets for selling bonus
# Verkauf: Basiswert
# Distanzbonus
# pro Stadtpop: +1%
# Resi nicht vorhanden: +20%
# pro Wunder: 5%
# pro Haltung des Gegenübers (interner Handel = 0%): +5%
# -----------------------
# Gewinn = ZwSumme - calculateDistanceMaintenanceTimes100() / 10 (in %)
def calculateBonusSellingPrice(pUnit, pCity, bCalcOnly, iBonus2=-1):

	if not pUnit.getUnitType() in L.LTradeUnits:
		return -1
	if bCalcOnly:
		if iBonus2 == -1:
			# Selling Bonus1 from city 1 to city 2
			eBonus = CvUtil.getScriptData(pUnit, ["autB1"], -1)
			iX = CvUtil.getScriptData(pUnit, ["autX1"], -1)
			iY = CvUtil.getScriptData(pUnit, ["autY1"], -1)
		else:
			# Selling Bonus2 from city 2 to city 1
			eBonus = iBonus2
			iX = CvUtil.getScriptData(pUnit, ["autX2"], -1)
			iY = CvUtil.getScriptData(pUnit, ["autY2"], -1)
	else:
		eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
		iX = CvUtil.getScriptData(pUnit, ["x"], -1)
		iY = CvUtil.getScriptData(pUnit, ["y"], -1)
	if eBonus == -1:
		return -1
	iSeller = CvUtil.getScriptData(pUnit, ["originCiv"], pUnit.getOwner())
	iBuyer = pCity.getOwner()
	iBasis = getBonusValue(eBonus)  # Grundwert
	iModifier = 100

	# if CvUtil.hasBonusIgnoreFreeBonuses(pCity, eBonus): # allows "cancellation" of buying / Bonus direkt nach Einkauf wieder verkaufen (ohne Gewinn)
	#    return _calculateBonusBuyingPrice(eBonus, iSeller, iBuyer) # Switch positions of seller and buyer

	# Einkauf und Verkauf in der gleichen Stadt (=> undo)
	if not bCalcOnly and pUnit.getX() == iX and pUnit.getY() == iY:
		return _calculateBonusBuyingPrice(eBonus, iSeller, iBuyer)  # Switch positions of seller and buyer

	# Basiswert + Population + Distanz + Wunderbonus + Haltung + Verfügbarkeit - Korruption

	# iDistance = CyMap().calculatePathDistance(gc.getMap().plot(iX, iY), pCity.plot()) # nimmt Landweg bei einer Bucht
	iDistance = plotDistance(iX, iY, pCity.getX(), pCity.getY()) - 1
	iPop = pCity.getPopulation()

	# Stadt hat dieses Bonusgut nicht im Handelsnetz
	if not pCity.hasBonus(eBonus):
		iModifier += 20
	# Wunderbonus
	iModifier += pCity.getNumWorldWonders() * 5
	# Furious = 0, Annoyed = 1, Cautious = 2, Pleased = 3, Friendly = 4
	if iSeller != iBuyer:
		iModifier += 5 * gc.getPlayer(iSeller).AI_getAttitude(iBuyer)

	# Zwischensumme
	iSum = iBasis * (iPop + iModifier)/100 + iBasis*iDistance // (75 - iBasis)

	iKorruption = pCity.calculateDistanceMaintenance() * 2

	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iBasis",iBasis)), None, 2, None, ColorTypes(10), 0, 0, False, False)
	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iBasis + iPop + Modi",(iBasis * (iPop + iModifier)/100))), None, 2, None, ColorTypes(10), 0, 0, False, False)
	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Distanzbonus",(iBasis*iDistance // (70 - iBasis)))), None, 2, None, ColorTypes(10), 0, 0, False, False)
	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iKorruption",iKorruption)), None, 2, None, ColorTypes(10), 0, 0, False, False)
	#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iSum",int(iSum - iKorruption))), None, 2, None, ColorTypes(10), 0, 0, False, False)

	return int(iSum - iKorruption)
# --- End of price stuff (trade) ---


# --- Automated trade routes (popups for HI) ---

# Erzeugt Popup fuer Erstellung einer automatisierten Handelsroute, wird insgesamt sechsmal pro Route aufgerufen:
# Civ waehlen => Stadt waehlen => Bonus waehlen => Civ waehlen => Stadt waehlen => Bonus waehlen
# iType = 1, 2, ...., 6 gibt an, an welcher Stelle im Prozess man gerade ist (1: erste Civ waehlen, ..., 6: zweiten Bonus waehlen)
# iData1/2: Ggf. noetige, zusaetzliche Informationen
def doPopupAutomatedTradeRoute(pUnit, iType, iData1, iData2):
	iUnitOwner = pUnit.getOwner()

	# Dies soll doppelte Popups in PB-Spielen vermeiden.
	if iUnitOwner != gc.getGame().getActivePlayer():
		return

	# Nation auswählen, 1 = erste Nation, 4 = zweite Nation
	# Choose civilization 1 (iType == 1) or civilization 2 (iType == 4)
	if iType == 1 or iType == 4:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		if iType == 1:
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_ROUTE_CHOOSE_CIV_1", ("", )))
		else:
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_ROUTE_CHOOSE_CIV_2", ("", )))
		popupInfo.setOnClickedPythonCallback("popupTradeRouteChooseCiv")
		popupInfo.setData1(iUnitOwner)
		popupInfo.setData2(pUnit.getID())
		popupInfo.setData3(iType == 1)

		iBonus = int(CvUtil.getScriptData(pUnit, ["autB1"], -1))

		# Erster Button type 1: Diese Stadt oder Abbrechen (damit Button Anzahl in ScreenInterface stimmt)
		if iType == 1:
			if pUnit.plot().isCity():
				sText = CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_5", (pUnit.plot().getPlotCity().getName(),))
				popupInfo.addPythonButton(sText, PAE_City.getCityStatus(pUnit.plot().getPlotCity(), 0, 0, True))
			# else:
			#  popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ()), "Art/Interface/Buttons/Actions/Cancel.dds")
		# Erster Button type 4: Unsere CIV oder zu Schritt 1
		else:
			#iX = int(CvUtil.getScriptData(pUnit, ["autX1"], -1))
			#iY = int(CvUtil.getScriptData(pUnit, ["autY1"], -1))
			# if CyMap().plot(iX, iY).getPlotCity().getOwner() != pUnit.getOwner():
			#sText = CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_6", (gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0),))
			#if not gc.getPlayer(pUnit.getOwner()).hasBonus(iBonus): sText += u" %c" % (CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
			#popupInfo.addPythonButton(sText, gc.getCivilizationInfo(gc.getPlayer(pUnit.getOwner()).getCivilizationType()).getButton())
			# else:
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_BACK_STEP_1", ()), "Art/Interface/Buttons/Actions/Cancel.dds")

		# weitere Buttons (CIVs)
		lCivs = getPossibleTradeCivs(iUnitOwner)
		for iPlayer in lCivs:
			pPlayer = gc.getPlayer(iPlayer)
			if iPlayer == iUnitOwner:
				sText = CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_6", (gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0),))
			else:
				sText = pPlayer.getCivilizationDescription(0)
			if iType == 1:
				sText += u" (%s)" % pPlayer.getName()
			else:
				if iBonus != -1:
					if pPlayer.hasBonus(iBonus):
						sText += u" %c (%s %c)" % (CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 6,
							CyTranslator().getText("TXT_KEY_CIV_HABEN_BEREITS", ()), gc.getBonusInfo(iBonus).getChar())
					else:
						sText += u" %c" % (CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
			sButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
			popupInfo.addPythonButton(sText, sButton)

		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ()), "Art/Interface/Buttons/Actions/Cancel.dds")
		popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
		popupInfo.addPopup(iUnitOwner)

	# Stadt auswählen: 2 = erste Stadt, 5 = zweite Stadt
	# Choose city 1 (iType == 2) or city 2 (iType == 5)
	elif iType == 2 or iType == 5:
		iCityOwner = iData1
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_ROUTE_CHOOSE_CITY", ()))
		if iType == 2:
			popupInfo.setOnClickedPythonCallback("popupTradeRouteChooseCity1")
			iStep = 1
		else:
			popupInfo.setOnClickedPythonCallback("popupTradeRouteChooseCity2")
			iStep = 2
		popupInfo.setData1(iUnitOwner)
		popupInfo.setData2(pUnit.getID())
		popupInfo.setData3(iCityOwner)
		lCities = getPossibleTradeCitiesForCiv(pUnit, iCityOwner, iStep)
		#sButton = ",Art/Interface/Buttons/Actions/FoundCity.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,1,4"
		for pCity in lCities:
			sText = pCity.getName()
			sButton = PAE_City.getCityStatus(pCity, 0, 0, True)
			if pCity.isCapital():
				sText += CyTranslator().getText(" [ICON_STAR]", ())
			elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")):
				sText += CyTranslator().getText(" [ICON_SILVER_STAR]", ())
			if iType == 5:
				iPrice = calculateBonusSellingPrice(pUnit, pCity, 1)
				if iPrice == -1:
					iPrice = 0
				sText += u"  +" + str(iPrice) + CyTranslator().getText("[ICON_GOLD]", ())
				iX = int(CvUtil.getScriptData(pUnit, ["autX1"], -1))
				iY = int(CvUtil.getScriptData(pUnit, ["autY1"], -1))
				iDistance = max(1, int((plotDistance(iX, iY, pCity.getX(), pCity.getY()) - 1) / pUnit.baseMoves()))
				sText += u", %d%c" % (iDistance, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
			popupInfo.addPythonButton(sText, sButton)
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ()), "Art/Interface/Buttons/Actions/Cancel.dds")
		popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
		popupInfo.addPopup(iUnitOwner)

	# Bonus auswählen: 3 = erste Stadt, 6 = zweite Stadt
	# Choose bonus to buy in selected city.
	elif iType == 3 or iType == 6:
		pCity = gc.getPlayer(iData1).getCity(iData2)
		sCityName = pCity.getName()
		lGoods = getCitySaleableGoods(pCity, -1)
		lGoods.append(-1)
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_ROUTE_CHOOSE_BONUS", (sCityName, )))
		popupInfo.setOnClickedPythonCallback("popupTradeRouteChooseBonus")
		popupInfo.setData1(iUnitOwner)
		popupInfo.setData2(pUnit.getID())
		popupInfo.setData3(iType == 3)
		for eBonus in lGoods:
			if eBonus != -1:
				sBonusDesc = gc.getBonusInfo(eBonus).getDescription()
				iPrice = _calculateBonusBuyingPrice(eBonus, iUnitOwner, iData1)
				# Erste Stadt, eigene Stadt => keine Vergleich-CIV => keine Anzeige, wer das Bonusgut hat oder nicht hat
				if iType == 3 and iData1 == iUnitOwner:
					sText = sBonusDesc + u" (-" + str(iPrice) + CyTranslator().getText("[ICON_GOLD])", ())
				else:
					if iData1 != iUnitOwner:
						iBonusOwned = gc.getPlayer(iUnitOwner).getNumAvailableBonuses(eBonus)
						#sText = CyTranslator().getText("TXT_KEY_BUY_BONUS", (sBonusDesc, iPrice, iBonusOwned))
					else:
						iX1 = CvUtil.getScriptData(pUnit, ["autX1"], -1)
						iY1 = CvUtil.getScriptData(pUnit, ["autY1"], -1)
						pCityPlot1 = CyMap().plot(iX1, iY1)
						iBonusOwned = gc.getPlayer(pCityPlot1.getOwner()).getNumAvailableBonuses(eBonus)
						#sText = CyTranslator().getText("TXT_KEY_BUY_BONUS2", (sBonusDesc, iPrice, iBonusOwned))

					if iType == 6:
						if not "iX1" in locals():
							iX1 = CvUtil.getScriptData(pUnit, ["autX1"], -1)
							iY1 = CvUtil.getScriptData(pUnit, ["autY1"], -1)
							pCityPlot1 = CyMap().plot(iX1, iY1)

						pFirstCity = pCityPlot1.getPlotCity()
						iPrice2 = calculateBonusSellingPrice(pUnit, pFirstCity, 1, eBonus)

						if iData1 != iUnitOwner:
							sText = CyTranslator().getText("TXT_KEY_BUY_BONUS_SELL", (sBonusDesc, iPrice, iBonusOwned, iPrice2-iPrice))
						else:
							sText = CyTranslator().getText("TXT_KEY_BUY_BONUS2_SELL", (sBonusDesc, iPrice, iBonusOwned, iPrice2-iPrice))
					else:
						if iData1 != iUnitOwner:
							sText = CyTranslator().getText("TXT_KEY_BUY_BONUS", (sBonusDesc, iPrice, iBonusOwned))
						else:
							sText = CyTranslator().getText("TXT_KEY_BUY_BONUS2", (sBonusDesc, iPrice, iBonusOwned))

					if iBonusOwned == 0:
						sText += u" " + CyTranslator().getText("[ICON_HAPPY]", ())

				sButton = gc.getBonusInfo(eBonus).getButton()
				popupInfo.addPythonButton(sText, sButton)
			else:
				sText = CyTranslator().getText("TXT_KEY_NO_BONUS", ())
				sButton = "Art/Interface/Buttons/Techs/button_x.dds"
				popupInfo.addPythonButton(sText, sButton)
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ()), "Art/Interface/Buttons/Actions/Cancel.dds")
		popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
		popupInfo.addPopup(iUnitOwner)
# --- End of automated trade routes for HI ---

# --- Helper functions ---


def getCitySaleableGoods(pCity, iBuyer):
	""" Returns a list of the tradeable bonuses within pCity's range (radius of 2) + bonuses from buildings (bronze etc.). Only goods within the team's culture are considered.
		if iBuyer != -1: Bonuses the buying player cannot afford (not enough money) are excluded
	"""
	if pCity is None or pCity.isNone():
		return []
	iCityOwnerTeam = pCity.getTeam()
	iCityOwner = pCity.getOwner()
	# pCityOwner = gc.getPlayer(iCityOwner)
	if iBuyer != -1:
		iMaxPrice = gc.getPlayer(iBuyer).getGold()

	lGoods = []
	for i in xrange(gc.getNUM_CITY_PLOTS()):
		pLoopPlot = pCity.getCityIndexPlot(i)
		if pLoopPlot is not None and not pLoopPlot.isNone():
			if pLoopPlot.getTeam() != iCityOwnerTeam:
				continue
			# plot needs to have suitable improvement and city needs to have access to bonus (=> connection via trade route (road))
			eBonus = pLoopPlot.getBonusType(iCityOwnerTeam)
			eImprovement = pLoopPlot.getImprovementType()
			if eBonus != -1 and eBonus not in lGoods and eBonus not in L.LBonusUntradeable:
				# if CvUtil.hasBonusIgnoreFreeBonuses(pCity, eBonus):
				if pLoopPlot.isCity() or eImprovement != -1 and gc.getImprovementInfo(eImprovement).isImprovementBonusMakesValid(eBonus):
					if iBuyer == -1 or _calculateBonusBuyingPrice(eBonus, iBuyer, iCityOwner) <= iMaxPrice:  # Max price
						lGoods.append(eBonus)

	iMaxNumBuildings = gc.getNumBuildingInfos()
	for iBuilding in xrange(iMaxNumBuildings):  # check buildings
		if pCity.isHasBuilding(iBuilding):
			eBonus = gc.getBuildingInfo(iBuilding).getFreeBonus()
			# and CvUtil.hasBonusIgnoreFreeBonuses(pCity, eBonus):
			if eBonus != -1 and eBonus not in L.LBonusUntradeable and eBonus not in lGoods:
				if iBuyer == -1 or _calculateBonusBuyingPrice(eBonus, iBuyer, iCityOwner) <= iMaxPrice:  # Max price
					lGoods.append(eBonus)
	return lGoods

# Returns list of civs iPlayer can trade with (has met and peace with). List always includes iPlayer himself.


def getPossibleTradeCivs(iPlayer):
	pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
	lCivList = []
	for iCiv in xrange(gc.getMAX_PLAYERS()):
		if gc.getPlayer(iCiv).isAlive():
			iCivTeam = gc.getPlayer(iCiv).getTeam()
			if iPlayer == iCiv or pTeam.isHasMet(iCivTeam) and pTeam.isOpenBorders(iCivTeam) and not pTeam.isAtWar(iCivTeam):
				lCivList.append(iCiv)
	return lCivList

# Returns list of cities which 1. belong to iCityOwner and 2. are visible to UnitOwner


def getPossibleTradeCitiesForCiv(pUnit, iCityOwner, iStep):
	iArea = pUnit.plot().getArea()
	bWater = pUnit.getDomainType() == DomainTypes.DOMAIN_SEA
	iTeam1 = gc.getPlayer(pUnit.getOwner()).getTeam()
	pPlayer2 = gc.getPlayer(iCityOwner)

	if iStep == 2:
		# Choice of the second city
		# We can't choose the same city as the first
		iX = int(CvUtil.getScriptData(pUnit, ["autX1"], -1))
		iY = int(CvUtil.getScriptData(pUnit, ["autY1"], -1))
	else:
		iX = -1
		iY = -1

	lCityList = []
	(loopCity, pIter) = pPlayer2.firstCity(False)
	while loopCity:
		if not loopCity.isNone() and loopCity.getOwner() == iCityOwner:  # only valid cities
			if loopCity.getX() != iX or loopCity.getY() != iY:
				if loopCity.isRevealed(iTeam1, 0):
					if bWater and loopCity.isCoastal(4) or not bWater and loopCity.plot().getArea() == iArea:
						lCityList.append(loopCity)
		(loopCity, pIter) = pPlayer2.nextCity(pIter, False)
	return lCityList


# --- AI and automated trade routes ---

# Lets pUnit shuttle between two cities (defined by UnitScriptData). Used by AI and by HI (automated trade routes).
def doAutomateMerchant(pUnit):
	# DEBUG
	# iHumanPlayer = gc.getGame().getActivePlayer()
	# CyInterface().addMessage(iHumanPlayer, True, 10, "Player: " + str(pUnit.getOwner()) + " Unit-ID: " + str(pUnit.getID()), None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
	# if pUnit.getOwner() == iHumanPlayer:
	#   CyInterface().addMessage(iHumanPlayer, True, 10, "Unit is active", None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
	bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA", "t"], 0))
	if bTradeRouteActive:  # and pUnit.getGroup().getLengthMissionQueue() == 0:

		iPlayer = pUnit.getOwner()
		pUnitPlot = pUnit.plot()
		# iTurn = gc.getGame().getGameTurn()
		# pUnit.getGroup().clearMissionQueue()

		# if iPlayer == iHumanPlayer:
		# CyInterface().addMessage(iHumanPlayer, True, 10, "Unit autLTC: " + str(CvUtil.getScriptData(pUnit, ["autLTC"], -1)), None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)

		# Verhindern, dass mehrmals pro Runden geprueft wird, um Rundenzeit zu sparen
		# Z.B. bei bedrohten Einheiten ruft Civ die Funktion sonst 100 Mal auf, weiss nicht wieso...
		# iLastTurnChecked = CvUtil.getScriptData(pUnit, ["autLTC"], -1)
		# if iLastTurnChecked >= iTurn: # and not pUnit.isHuman():
		#     return False
		# else:
		#   CvUtil.addScriptData(pUnit, "autLTC", iTurn)

		eStoredBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
		iX1 = CvUtil.getScriptData(pUnit, ["autX1"], -1)
		iY1 = CvUtil.getScriptData(pUnit, ["autY1"], -1)
		iX2 = CvUtil.getScriptData(pUnit, ["autX2"], -1)
		iY2 = CvUtil.getScriptData(pUnit, ["autY2"], -1)
		eBonus1 = CvUtil.getScriptData(pUnit, ["autB1"], -1)  # bonus bought in city 1
		eBonus2 = CvUtil.getScriptData(pUnit, ["autB2"], -1)  # bonus bought in city 2
		pCityPlot1 = CyMap().plot(iX1, iY1)
		pCityPlot2 = CyMap().plot(iX2, iY2)
		pCity1 = pCityPlot1.getPlotCity()
		pCity2 = pCityPlot2.getPlotCity()

		# if iPlayer == iHumanPlayer:
		#txt = u"Player: %d | Bonus: %d, (x1:%d|y1:%d|b:%d) -> (x2:%d|y2:%d|b:%d) autLTC:%d" % (iPlayer,eStoredBonus,iX1,iY1,eBonus1,iX2,iY2,eBonus2,iLastTurnChecked)
		#CyInterface().addMessage(iHumanPlayer, True, 10, txt, None, 2, pUnit.getButton(), ColorTypes(10), pUnit.getX(), pUnit.getY(), True, True)

		bWar = False
		bOpenBorders = True
		if not pCity1.isNone() and not pCity2.isNone():
			if pCity1.getOwner() != pCity2.getOwner():
				# Städte haben untereinander Krieg
				if gc.getTeam(gc.getPlayer(pCity1.getOwner()).getTeam()).isAtWar(gc.getPlayer(pCity2.getOwner()).getTeam()):
					bWar = True

				# Städte haben kein Durchreiserecht mehr
				pTeam1 = gc.getTeam(gc.getPlayer(pCity1.getOwner()).getTeam())
				if not pTeam1.isOpenBorders(gc.getPlayer(pCity2.getOwner()).getTeam()):
					bOpenBorders = False

		if pCity1 is None or pCity1.isNone() or pCity2 is None or pCity2.isNone() or bWar or not bOpenBorders:
			# delete invalid trade route
			CvUtil.removeScriptData(pUnit, "autA")
			CvUtil.removeScriptData(pUnit, "autLTC")
			CvUtil.removeScriptData(pUnit, "autX1")
			CvUtil.removeScriptData(pUnit, "autY1")
			CvUtil.removeScriptData(pUnit, "autX2")
			CvUtil.removeScriptData(pUnit, "autY2")
			CvUtil.removeScriptData(pUnit, "autB1")
			CvUtil.removeScriptData(pUnit, "autB2")

			# Messages
			if pUnit.isHuman():
				# Message: Eure Handelsstadt verbietet Durchreiserecht
				if not bOpenBorders:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_4", ()))
					popupInfo.addPopup(iPlayer)
				# Message: Eure Handelsstadt wurde dem Erdboden gleich gemacht
				elif not bWar:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_1", ()))
					popupInfo.addPopup(iPlayer)

			return False

		# Unit steht in einer Handelsstadt
		if pUnit.atPlot(pCityPlot1) or pUnit.atPlot(pCityPlot2):
			if pUnit.atPlot(pCityPlot1):
				pCurrentCity = pCity1
				pNewCity = pCity2
				eBonusBuy = eBonus1
				# eBonusSell = eBonus2
			elif pUnit.atPlot(pCityPlot2):
				pCurrentCity = pCity2
				pNewCity = pCity1
				eBonusBuy = eBonus2
				# eBonusSell = eBonus1

			# if eBonusSell != -1 and eStoredBonus == eBonusSell:
			if eStoredBonus != -1 and eStoredBonus != eBonusBuy:
				doSellBonus(pUnit, pCurrentCity)
				# if iPlayer == iHumanPlayer:
				# CyInterface().addMessage(iHumanPlayer, True, 10, "Unit sold bonus in city", None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)

			# if iPlayer == iHumanPlayer:
			#   CyInterface().addMessage(iHumanPlayer, True, 10, "Unit is in City", None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)

			# HI: if player does not have enough money, trade route is cancelled
			# AI: if AI does not have enough money, AI buys bonus nonetheless (causes no known errors)
			# doBuyBonus doesn't work this way. AIs traderoute will be deactivated as well.
			if pUnit.isHuman():
				iBuyer = iPlayer
			else:
				iBuyer = -1
			lCitySaleableGoods = getCitySaleableGoods(pCurrentCity, iBuyer)

			if eBonusBuy == -1:
				# CyInterface().addMessage(iHumanPlayer, True, 10, "Mission eBonusBuy == -1 ", None, 2, None, ColorTypes(7), 0, 0, False, False)
				# pUnit.getGroup().pushMoveToMission(pNewCity.getX(), pNewCity.getY())
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pNewCity.getX(), pNewCity.getY(),
					1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
			elif eStoredBonus == eBonusBuy:
				# CyInterface().addMessage(iHumanPlayer, True, 10, "Mission eBonusBuy == eStoredBonus | got to " + pNewCity.getName(), None, 2, None, ColorTypes(7), 0, 0, False, False)
				# pUnit.getGroup().pushMoveToMission(pNewCity.getX(), pNewCity.getY())
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pNewCity.getX(), pNewCity.getY(),
					1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
			elif eBonusBuy in lCitySaleableGoods:
				# if iPlayer == iHumanPlayer: CyInterface().addMessage(iHumanPlayer, True, 10, "Mission eBonusBuy in lCitySaleable ", None, 2, None, ColorTypes(7), 0, 0, False, False)
				if eStoredBonus != eBonusBuy:
					# if not already acquired / Wenn Bonus nicht bereits gekauft wurde
					# if not pUnit.hasMoved():
					doBuyBonus(pUnit, eBonusBuy, pCurrentCity.getOwner())
					pUnit.finishMoves()
				# CyInterface().addMessage(iHumanPlayer, True, 10, "Mission eBonusBuy MOVE to new city ", None, 2, None, ColorTypes(7), 0, 0, False, False)
				# pUnit.getGroup().pushMoveToMission(pNewCity.getX(), pNewCity.getY())
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pNewCity.getX(), pNewCity.getY(),
					1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
				return True
			else:
				# bonus is no longer available (or player does not have enough money) => cancel automated trade route
				CvUtil.addScriptData(pUnit, "autA", 0)  # deactivate route

				# Messages:
				if pUnit.isHuman() and iBuyer != -1:
					if _calculateBonusBuyingPrice(eBonusBuy, iBuyer, pCurrentCity.getOwner()) > gc.getPlayer(iBuyer).getGold():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_2",
							(gc.getBonusInfo(eBonusBuy).getDescription(), pCurrentCity.getName())))
						popupInfo.addPopup(iPlayer)
					elif eBonusBuy not in lCitySaleableGoods:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_INFO_3",
							(gc.getBonusInfo(eBonusBuy).getDescription(), pCurrentCity.getName())))
						popupInfo.addPopup(iPlayer)

				#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant False: Bonus no longer available", None, 2, None, ColorTypes(7), 0, 0, False, False)
				return False

		else:
			# unit is anywhere
			# if iPlayer == 0:
			#  CyInterface().addMessage(iHumanPlayer, True, 10, "Unit is anywhere", None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
			if eStoredBonus == eBonus1:
				#pUnit.getGroup().pushMoveToMission(pCityPlot2.getX(), pCityPlot2.getY())
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX2, iY2, 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
				# if iPlayer == 12:
				#  CyInterface().addMessage(iHumanPlayer, True, 10, "Unit is anywhere: eStoredBonus == eBonus1", None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
			elif eStoredBonus == eBonus2:
				#pUnit.getGroup().pushMoveToMission(pCityPlot1.getX(), pCityPlot1.getY())
				# VOID pushMission (MissionType eMission, INT iData1, INT iData2, INT iFlags, BOOL bAppend, BOOL bManual, MissionAIType eMissionAI, CyPlot pMissionAIPlot, CyUnit pMissionAIUnit)
				# iFlags = 1: MOVE_THROUGH_ENEMY
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX1, iY1, 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
				# if iPlayer == 12:
				#  CyInterface().addMessage(iHumanPlayer, True, 10, "Unit is anywhere: eStoredBonus == eBonus2", None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
			else:
				# auch wenn eBonus = -1
				#iDistance1 = CyMap().calculatePathDistance(pUnitPlot, pCityPlot1)
				iDistance1 = plotDistance(pUnitPlot.getX(), pUnitPlot.getY(), pCityPlot1.getX(), pCityPlot1.getY()) - 1
				#iDistance2 = CyMap().calculatePathDistance(pUnitPlot, pCityPlot2)
				iDistance2 = plotDistance(pUnitPlot.getX(), pUnitPlot.getY(), pCityPlot2.getX(), pCityPlot2.getY()) - 1
				# if iPlayer == 0:
				#  CyInterface().addMessage(iHumanPlayer, True, 10, "Unit is anywhere: else: Distance1: "+str(iDistance1) + u" Distanz2: "+str(iDistance2), None, 2, None, ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
				if iDistance1 == -1 and iDistance2 == -1:
					#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant False: Plot unreachable", None, 2, None, ColorTypes(7), 0, 0, False, False)
					return False  # plot unreachable
				elif iDistance1 == -1:
					#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant iDistance1 == -1 ", None, 2, None, ColorTypes(6), 0, 0, False, False)
					#pUnit.getGroup().pushMoveToMission(pCityPlot2.getX(), pCityPlot2.getY())
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX2, iY2, 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
				elif iDistance2 == -1 or iDistance1 <= iDistance2:
					#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant iDistance1 smaller than iDistance2 ", None, 2, None, ColorTypes(6), 0, 0, False, False)
					#pUnit.getGroup().pushMoveToMission(pCityPlot1.getX(), pCityPlot1.getY())
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX1, iY1, 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
				else:
					#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant else ", None, 2, None, ColorTypes(6), 0, 0, False, False)
					#pUnit.getGroup().pushMoveToMission(pCityPlot2.getX(), pCityPlot2.getY())
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX2, iY2, 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)

		#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant returns True ", None, 2, None, ColorTypes(6), 0, 0, False, False)
		return True

	#CyInterface().addMessage(iHumanPlayer, True, 10, "doAutomateMerchant returns False " + str(pUnit.getOwner()), None, 2, None, ColorTypes(7), 0, 0, False, False)
	return False

# Weist der Einheit eine moeglichst kurze Handelsroute zu, die moeglichst so verlaeuft, dass an beiden Stationen ein Luxusgut eingeladen wird


def doAssignTradeRoute_AI(pUnit):
	# iHumanPlayer = -1 (Needed for test messages, otherwise unnecessary)
	iPlayer = pUnit.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pUnitPlot = pUnit.plot()
	bWater = pUnit.getDomainType() == DomainTypes.DOMAIN_SEA

	if pPlayer.getGold() < 50:
		return False

	bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA", "t"], 0))
	if bTradeRouteActive:
		return False

	# friedliche Nachbarn raussuchen
	lNeighbors = []
	iRange = gc.getMAX_PLAYERS()
	for iLoopPlayer in xrange(iRange):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive() and iLoopPlayer != iPlayer:
			if pTeam.isHasMet(pLoopPlayer.getTeam()):
				if pTeam.isOpenBorders(pLoopPlayer.getTeam()):
					# widerspricht ohnehin open borders
					# if not pTeam.isAtWar(pLoopPlayer.getTeam()):
					# Distanz mittels Abstand zur Hauptstadt herausfinden
					(loopCity, pIter) = pLoopPlayer.firstCity(False)
					while loopCity:
						if not loopCity.isNone() and loopCity.getOwner() == iLoopPlayer:  # only valid cities
							if loopCity.isCapital():
								if bWater:
									iDistance = plotDistance(pUnitPlot.getX(), pUnitPlot.getY(), loopCity.getX(), loopCity.getY()) - 1
								else:
									iDistance = CyMap().calculatePathDistance(pUnitPlot, loopCity.plot())

								if iDistance != -1:
									lNeighbors.append([iDistance, iLoopPlayer])
						(loopCity, pIter) = pLoopPlayer.nextCity(pIter, False)
					# if not pLoopPlayer.getCity(0).isNone():
						# iDistance = CyMap().calculatePathDistance(pUnitPlot, pLoopPlayer.getCity(0).plot())
						# if iDistance != -1:
						# lNeighbors.append([iDistance, iLoopPlayer])

	lNeighbors.sort()  # sort by distance
	lNeighbors = lNeighbors[:5]  # only check max. 5 neighbors
	# Liste aller Staedte des Spielers mit verfuegbaren Luxusguetern. Staedte ohne Luxusgut ausgelassen.
	lPlayerLuxuryCities = _getPlayerLuxuryCities(iPlayer)
	iMaxDistance = 15  # Wie weit die KI einen Haendler max. schickt
	iMinDistance = -1
	bBothDirections = False
	pBestPlayerCity = None
	pBestNeighborCity = None
	for [iDistance, iNeighbor] in lNeighbors:
		lNeighborLuxuryCities = _getPlayerLuxuryCities(iNeighbor)
		# Sucht nach Paar von Staedten, zwischen denen Luxushandel moeglich ist, mit min. Distanz.
		# Routen, bei denen in beiden Staedten Luxus eingekauft werden kann, der in der anderen Stadt wieder verkauft
		# werden kann (=> Bonus NICHT in beiden Staedten), werden bevorzugt (dann ist bBothDirections = True).
		# Sonst wird eine Route gewaehlt, bei der der Haendler nur in eine Richtung handelt (andere Richtung Leertransport)
		for [pNeighborCity, lNeighborCityLuxury] in lNeighborLuxuryCities:
			for [pPlayerCity, lPlayerCityLuxury] in lPlayerLuxuryCities:
				pCityPlotPlayer = pPlayerCity.plot()
				pCityPlotNeighbor = pNeighborCity.plot()
				# Handelsstrasse existiert schon => andere Route waehlen
				if getPlotTradingRoad(pCityPlotPlayer, pCityPlotNeighbor) is None:
					continue

				if bWater and pNeighborCity.isCoastal(4):
					iDistance = plotDistance(pCityPlotPlayer.getX(), pCityPlotPlayer.getY(), pCityPlotNeighbor.getX(), pCityPlotNeighbor.getY()) - 1
				else:
					iDistance = CyMap().calculatePathDistance(pCityPlotPlayer, pCityPlotNeighbor)

				if iDistance == -1 or iDistance > iMaxDistance:
					continue

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Keine Handelsstrasse", None, 2, None, ColorTypes(8), pUnit.getX(), pUnit.getY(), False, False)
				bDirection1 = False
				bDirection2 = False
				for eBonus in lNeighborCityLuxury:
					if not pPlayerCity.hasBonus(eBonus):
						bDirection1 = True
						break
				for eBonus in lPlayerCityLuxury:
					if not pNeighborCity.hasBonus(eBonus):
						bDirection2 = True
						break

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "iDistance != -1", None, 2, None, ColorTypes(8), pUnit.getX(), pUnit.getY(), False, False)
				if bDirection1 and bDirection2:
					if iMinDistance == -1 or iDistance < iMinDistance or not bBothDirections:
						bBothDirections = True
						iMinDistance = iDistance
						pBestPlayerCity = pPlayerCity
						pBestNeighborCity = pNeighborCity
						# Wenn Route, die in beide Richtungen funktioniert, gefunden wurde, abbrechen (spart Rechenzeit)
						# Route ist zwar ggf. nicht optimal, aber gut genug (beide Richtungen, Abstand <= iMaxDistance)
						break
				elif (bDirection1 or bDirection2) and not bBothDirections:
					if iMinDistance == -1 or iDistance < iMinDistance:
						iMinDistance = iDistance
						pBestPlayerCity = pPlayerCity
						pBestNeighborCity = pNeighborCity
			# Wenn Route, die in beide Richtungen funktioniert, gefunden wurde, abbrechen (spart Rechenzeit)
			# Route ist zwar ggf. nicht optimal, aber gut genug (beide Richtungen, Abstand <= iMaxDistance)
			if bBothDirections:
				break
		if bBothDirections:
			break

	# Wenn KI keine Stadt findet, weil sie schon alles hat, dann auf zur groessten Stadt
	if pBestPlayerCity is None:
		pBestPlayerCity = _getBestCity4Trade(pUnit, iPlayer)
	if pBestNeighborCity is None:
		for [iDistance, iNeighbor] in lNeighbors:
			pBestNeighborCity = _getBestCity4Trade(pUnit, iNeighbor)
			break

	if pBestPlayerCity != None and pBestNeighborCity != None:

		if CyMap().calculatePathDistance(pBestPlayerCity.plot(), pBestNeighborCity.plot()) == -1:
			return False

		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Stadt gefunden " + pBestPlayerCity.getName()+" nach "+pBestNeighborCity.getName(), None, 2, None, ColorTypes(10), 0, 0, False, False)
		lPlayerLuxuries = _getCityLuxuries(pBestPlayerCity)
		lNeighborLuxuries = _getCityLuxuries(pBestNeighborCity)
		lBonus1 = []
		lBonus2 = []
		for eBonus in lPlayerLuxuries:
			if not pBestNeighborCity.hasBonus(eBonus):
				lBonus1.append(eBonus)
		for eBonus in lNeighborLuxuries:
			if not pBestPlayerCity.hasBonus(eBonus):
				lBonus2.append(eBonus)

		if not lBonus1:
			lBonus1 = getCitySaleableGoods(pBestPlayerCity, -1)
		eBonus1 = lBonus1[CvUtil.myRandom(len(lBonus1), "get any bonus 4 trade")]
		if not lBonus2:
			lBonus2 = getCitySaleableGoods(pBestNeighborCity, -1)
		eBonus2 = lBonus2[CvUtil.myRandom(len(lBonus2), "get any bonus 4 trade")]

		CvUtil.addScriptData(pUnit, "autX1", pBestPlayerCity.getX())
		CvUtil.addScriptData(pUnit, "autY1", pBestPlayerCity.getY())
		CvUtil.addScriptData(pUnit, "autX2", pBestNeighborCity.getX())
		CvUtil.addScriptData(pUnit, "autY2", pBestNeighborCity.getY())
		CvUtil.addScriptData(pUnit, "autB1", eBonus1)  # bonus bought in city 1
		CvUtil.addScriptData(pUnit, "autB2", eBonus2)  # bonus bought in city 2
		CvUtil.addScriptData(pUnit, "autA", 1)

		#pUnit.getGroup().pushMoveToMission(pBestPlayerCity.getX(), pBestPlayerCity.getY())
		pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pBestPlayerCity.getX(),
			pBestPlayerCity.getY(), 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
		return True

	return False

# Returns list of iPlayer's cities and the luxuries in their reach (saleable). Cities without luxuries are skipped.
# e.g. returns [ [pCity1, [3, 34, 7]], [pCity2, [3, 7, 13] ]


def _getPlayerLuxuryCities(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	lCityList = []
	(loopCity, pIter) = pPlayer.firstCity(False)
	while loopCity:
		if not loopCity.isNone() and loopCity.getOwner() == pPlayer.getID():  # only valid cities
			lLuxuryGoods = _getCityLuxuries(loopCity)
			if lLuxuryGoods:
				lCityList.append([loopCity, lLuxuryGoods])
		(loopCity, pIter) = pPlayer.nextCity(pIter, False)
	return lCityList

# Returns list of the luxuries in reach of pCity (saleable). Used by AI trade route determination.


def _getCityLuxuries(pCity):
	lBonuses = getCitySaleableGoods(pCity, -1)
	lBonuses2 = CvUtil.getIntersection(L.LBonusStrategic, lBonuses)
	lBonuses2 += CvUtil.getIntersection(L.LBonusRarity, lBonuses)
	lBonuses2 += CvUtil.getIntersection(L.LBonusLuxury, lBonuses)
	if lBonuses2:
		return lBonuses2
	lBonuses2 = CvUtil.getIntersection(L.LBonusPlantation, lBonuses)
	if lBonuses2:
		return lBonuses2
	return lBonuses

# Returns the iPlayer's biggest city depending on distance of pUnit


def _getBestCity4Trade(pUnit, iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	pUnitPlot = pUnit.plot()
	bWater = pUnit.getDomainType() == DomainTypes.DOMAIN_SEA

	iDistance = 99
	iPop = 0
	pCity = None
	(loopCity, pIter) = pPlayer.firstCity(False)
	while loopCity:
		if not loopCity.isNone():
			lBonuses = getCitySaleableGoods(loopCity, -1)
			if len(lBonuses) > 0:

				if bWater and loopCity.isCoastal(4):
					iLoopCityDistance = plotDistance(pUnitPlot.getX(), pUnitPlot.getY(), loopCity.getX(), loopCity.getY()) - 1
				else:
					iLoopCityDistance = CyMap().calculatePathDistance(pUnitPlot, loopCity.plot())

				iLoopCityPop = loopCity.getPopulation()
				if iLoopCityDistance > -1 and (iLoopCityPop > iPop or iLoopCityPop == iPop) and iLoopCityDistance < iDistance:
					iDistance = iLoopCityDistance
					iPop = iLoopCityPop
					pCity = loopCity
		(loopCity, pIter) = pPlayer.nextCity(pIter, False)
	return pCity

############# Cities with special bonus order #################
# tsb: TradeSpecialBonus
# tst: TradeSpecialTurns


def doUpdateCitiesWithSpecialBonus(iGameTurn):
	global iCitiesSpecialBonus
	# Cities mit Special Trade Bonus herausfinden
	for i in xrange(gc.getMAX_PLAYERS()):
		loopPlayer = gc.getPlayer(i)
		if loopPlayer.isAlive() and not loopPlayer.isBarbarian():
			(loopCity, pIter) = loopPlayer.firstCity(False)
			while loopCity:
				if not loopCity.isNone() and loopCity.getOwner() == loopPlayer.getID():  # only valid cities
					iTurn = CvUtil.getScriptData(loopCity, ["tst"], -1)
					if iTurn != -1 and iTurn <= iGameTurn:
						eBonus = CvUtil.getScriptData(loopCity, ["tsb"], -1)
						CvUtil.removeScriptData(loopCity, "tsb")
						CvUtil.removeScriptData(loopCity, "tst")
						iCitiesSpecialBonus -= 1
						if eBonus != -1:
							iCityOwner = loopCity.getOwner()
							pPlayer = gc.getPlayer(iCityOwner)
							pTeam = gc.getTeam(pPlayer.getTeam())
							iActivePlayer = gc.getGame().getActivePlayer()
							if pTeam.isHasMet(gc.getPlayer(iActivePlayer).getTeam()):
								CyInterface().addMessage(iActivePlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_SPECIAL_1",
									(loopCity.getName(), gc.getBonusInfo(eBonus).getDescription())), None, 2, None, ColorTypes(13), 0, 0, False, False)
				(loopCity, pIter) = loopPlayer.nextCity(pIter, False)


def addCityWithSpecialBonus(iGameTurn):
	global iCitiesSpecialBonus
	global iMaxCitiesSpecialBonus
	lTurns = [20, 25, 30, 35, 40]
	# Max 3 cities
	if iCitiesSpecialBonus >= iMaxCitiesSpecialBonus:
		return

	LSpecialBonuses = L.LBonusLuxury + L.LBonusRarity

	lAllSpecialBonuses = []
	lNewCities = []
	for i in xrange(gc.getMAX_PLAYERS()):
		loopPlayer = gc.getPlayer(i)
		if loopPlayer.isAlive():
			# get cities
			if not loopPlayer.isHuman() and not loopPlayer.isBarbarian():
				(loopCity, pIter) = loopPlayer.firstCity(False)
				while loopCity:
					if not loopCity.isNone() and loopCity.getOwner() == loopPlayer.getID():  # only valid cities
						iTurn = CvUtil.getScriptData(loopCity, ["tst"], -1)
						if iTurn == -1:
							lNewCities.append(loopCity)
					(loopCity, pIter) = loopPlayer.nextCity(pIter, False)
			# get available special bonuses
			for iBonus in LSpecialBonuses:
				if loopPlayer.hasBonus(iBonus) and iBonus not in lAllSpecialBonuses:
					lAllSpecialBonuses.append(iBonus)

	lNewBonus = []
	iTry = 0
	while lNewCities and iTry < 3:
		# Stadt auswaehlen
		pCity = lNewCities[CvUtil.myRandom(len(lNewCities), "city addCityWithSpecialBonus")]
		# Dauer auswaehlen
		iTurns = lTurns[CvUtil.myRandom(len(lTurns), "turns addCityWithSpecialBonus")]
		# Bonusgut herausfinden
		for iBonus in lAllSpecialBonuses:
			if not pCity.hasBonus(iBonus):
				lNewBonus.append(iBonus)
		# Bonus setzen wenn die Stadt nicht eh schon alles hat.
		if len(lNewBonus) > 0:
			# Globale Variable setzen
			iCitiesSpecialBonus += 1
			CvUtil.addScriptData(pCity, "tst", iGameTurn+iTurns)
			eBonus = lNewBonus[CvUtil.myRandom(len(lNewBonus), "bonus addCityWithSpecialBonus")]
			CvUtil.addScriptData(pCity, "tsb", eBonus)
			iCityOwner = pCity.getOwner()
			pPlayer = gc.getPlayer(iCityOwner)
			pTeam = gc.getTeam(pPlayer.getTeam())
			iActivePlayer = gc.getGame().getActivePlayer()
			if pTeam.isHasMet(gc.getPlayer(iActivePlayer).getTeam()):
				CyInterface().addMessage(iActivePlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_SPECIAL_2",
					(pCity.getName(), gc.getBonusInfo(eBonus).getDescription())), None, 2, None, ColorTypes(11), 0, 0, False, False)
			break
		else:
			iTry += 1
			lNewCities.remove(pCity)

# ---------------

# In doSellBonus


def _doCheckCitySpecialBonus(pUnit, pCity, eBonus):
	global iCitiesSpecialBonus
	eCityBonus = CvUtil.getScriptData(pCity, ["tsb"], -1)
	if eCityBonus != -1 and eCityBonus == eBonus:
		iCitiesSpecialBonus -= 1
		CvUtil.removeScriptData(pCity, "tsb")
		CvUtil.removeScriptData(pCity, "tst")
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		if iPlayer != gc.getGame().getActivePlayer():
			CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText(
				"TXT_KEY_MESSAGE_TRADE_SPECIAL_3", (pPlayer.getName(),)), None, 2, None, ColorTypes(13), 0, 0, False, False)
		else:
			CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText(
				"TXT_KEY_MESSAGE_TRADE_SPECIAL_4", ("",)), "AS2D_WELOVEKING", 2, None, ColorTypes(13), 0, 0, False, False)

		# Belohnungen
		lGift = []

		# Military unit as gift:
		eCiv = gc.getCivilizationInfo(gc.getPlayer(pCity.getOwner()).getCivilizationType())
		#eOrigCiv = gc.getCivilizationInfo(gc.getPlayer(pCity.getOriginalOwner()).getCivilizationType())
		lUnits = [
			gc.getInfoTypeForString("UNIT_WAR_ELEPHANT"),
			gc.getInfoTypeForString("UNIT_CAMEL_ARCHER"),
			gc.getInfoTypeForString("UNITCLASS_CAMEL_CATAPHRACT"),
			gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
			gc.getInfoTypeForString("UNIT_SWORDSMAN"),
			gc.getInfoTypeForString("UNIT_COMPOSITE_ARCHER")
		]
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SPECIAL1"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SPECIAL2"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SPECIAL3"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SPECIAL4"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ELITE1"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ELITE2"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ELITE3"))
		if iUnit != -1:
			lUnits.append(iUnit)
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_AXEMAN2"))
		if iUnit != -1:
			lUnits.append(iUnit)
		else:
			lUnits.append(gc.getInfoTypeForString("UNIT_AXEMAN2"))
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_REFLEX_ARCHER"))
		if iUnit != -1:
			lUnits.append(iUnit)
		else:
			lUnits.append(gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"))
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_KAMPFHUND"))
		if iUnit != -1:
			lUnits.append(iUnit)
		else:
			lUnits.append(gc.getInfoTypeForString("UNIT_KAMPFHUND"))
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SKIRMISHER"))
		if iUnit != -1:
			lUnits.append(iUnit)
		else:
			lUnits.append(gc.getInfoTypeForString("UNIT_SKIRMISHER"))
		iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_AUXILIAR"))
		if iUnit != -1:
			lUnits.append(iUnit)
		else:
			lUnits.append(gc.getInfoTypeForString("UNIT_AUXILIAR"))

		# Mounted
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STABLE")):
			lGift.append(gc.getInfoTypeForString("UNIT_HORSE"))
			lUnits.append(gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN"))
			lUnits.append(gc.getInfoTypeForString("UNIT_CHARIOT"))
			lUnits.append(gc.getInfoTypeForString("UNIT_HORSE_ARCHER"))

		for iUnit in lUnits:
			if pCity.canTrain(iUnit, 0, 0):
				lGift.append(iUnit)

		# Standard gifts
		lGift.append(gc.getInfoTypeForString("UNIT_GOLDKARREN"))
		lGift.append(gc.getInfoTypeForString("UNIT_GOLDKARREN"))
		lGift.append(gc.getInfoTypeForString("UNIT_GOLDKARREN"))
		lGift.append(gc.getInfoTypeForString("UNIT_GOLDKARREN"))

		# Slave
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")) and not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_CHRISTIANITY")):
			lGift.append(gc.getInfoTypeForString("UNIT_SLAVE"))
		# Elefant
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE")):
			lGift.append(gc.getInfoTypeForString("UNIT_ELEFANT"))
		# Kamel
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CAMEL_STABLE")):
			lGift.append(gc.getInfoTypeForString("UNIT_CAMEL"))

		# Schenke Tech oder Units
		pTeamMerchant = gc.getTeam(pPlayer.getTeam())
		pTeamCity = gc.getTeam(gc.getPlayer(pCity.getOwner()).getTeam())
		TechArray = []
		for i in xrange(gc.getNumTechInfos()):
			if pTeamCity.isHasTech(i) and not pTeamMerchant.isHasTech(i):
				if gc.getTechInfo(i) is not None and gc.getTechInfo(i).isTrade():
					TechArray.append(i)
		# Tech schenken
		if TechArray and len(TechArray) > 0:
			iTechRand = CvUtil.myRandom(len(TechArray), "getTechOnSpecialTrade")
			iTech = TechArray[iTechRand]
			if pPlayer.getCurrentResearch() == iTech:
				pTeamMerchant.setResearchProgress(iTech, gc.getTechInfo(iTech).getResearchCost()-1, iPlayer)
			pTeamMerchant.setHasTech(iTech, 1, iPlayer, 0, 1)
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_POPUP_GETTING_TECH_2", (gc.getTechInfo(iTech).getDescription(), )))
				popupInfo.addPopup(iPlayer)
			else:
				pPlayer.clearResearchQueue()

		# Units schenken
		else:

			#  0 = WORLDSIZE_DUEL
			#  1 = WORLDSIZE_TINY
			#  2 = WORLDSIZE_SMALL
			#  3 = WORLDSIZE_STANDARD
			#  4 = WORLDSIZE_LARGE
			#  5 = WORLDSIZE_HUGE
			iRange = gc.getMap().getWorldSize() + 3

			for _ in xrange(iRange):
				# Choose gift
				iRand = CvUtil.myRandom(len(lGift), "Choose gift units")
				iNewUnit = lGift[iRand]

				if lGift[iRand] in lUnits:
					iNewUnitAIType = UnitAITypes.UNITAI_ATTACK
					# Message : Stadt schenkt Truppen
					if pPlayer.isHuman():
						CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText(
							"TXT_KEY_MESSAGE_TRADE_SPECIAL_5", ("",)), "AS2D_WELOVEKING", 2, None, ColorTypes(13), 0, 0, False, False)
				else:
					iNewUnitAIType = UnitAITypes.NO_UNITAI
					# Message : Stadt schenkt Kostbarkeiten
					if pPlayer.isHuman():
						CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText(
							"TXT_KEY_MESSAGE_TRADE_SPECIAL_6", ("",)), "AS2D_WELOVEKING", 2, None, ColorTypes(13), 0, 0, False, False)
				# Create unit
				pPlayer.initUnit(iNewUnit, pCity.getX(), pCity.getY(), iNewUnitAIType, DirectionTypes.DIRECTION_SOUTH)


def doMerchantRobbery(pUnit, pPlot, pOldPlot):
	"""Merchant units robbery / Handelskarren ausrauben"""

	# Merchant can be robbed
	eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
	if eBonus != -1 and pPlot.getNumUnits() == 1 and pOldPlot.getNumUnits() == 0 and not pPlot.isCity():

		barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		iBarbCities = barbPlayer.getNumCities()
		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMapSize = gc.getMap().getWorldSize() + 1

		# Chance in %
		iMinimumChance = 1
		if iBarbCities > 6 * iMapSize:
			iChance = 4
		elif iBarbCities > 3 * iMapSize:
			iChance = 2
		else:
			iChance = iMinimumChance

		iCalcChance = int(100/iChance)

		iRand = CvUtil.myRandom(iCalcChance, "Handelskarren-Ueberfall")
		if iRand == 1:
			bKill = False
			iPlayer = pUnit.getOwner()
			iPromo = gc.getInfoTypeForString("PROMOTION_SCHUTZ")  # Begleitschutz / Escort

			# ohne Begleitschutz
			if not pUnit.isHasPromotion(iPromo):

				if gc.getPlayer(iPlayer).isHuman():
					iRand = CvUtil.myRandom(5, "Handelskarren ausgeraubt Text")
					if iRand == 1:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_1", (0, 0))
						bKill = True
					elif iRand == 2:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_2", (0, 0))
						bKill = True
					elif iRand == 3:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_3", (0, 0))
					elif iRand == 4:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_4", (0, 0))
						bKill = True
					else:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_0", (0, 0))
					CyInterface().addMessage(iPlayer, True, 5, text, "AS2D_UNITCAPTURE", 2,
						"Art/Interface/Buttons/Units/button_merchant.dds", ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)

					# PopUp Message
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(text)
					popupInfo.addPopup(iPlayer)

				elif pPlot.getOwner() != -1:
					if gc.getPlayer(pPlot.getOwner()).isHuman():
						CyInterface().addMessage(pPlot.getOwner(), True, 5, CyTranslator().getText(
							"TXT_KEY_MESSAGE_MERCHANT_ROBBERY_1_1", (gc.getPlayer(pUnit.getOwner()).getCivilizationAdjective(3), 0)), None, 2, "Art/Interface/Buttons/Units/button_merchant.dds", ColorTypes(14), pPlot.getX(), pPlot.getY(), True, True)

				# PAE Trade: Einheit leeren
				CvUtil.removeScriptData(pUnit, "b")

			# mit Begleitschutz
			else:
				iRand = CvUtil.myRandom(5, "Handelskarren ausgeraubt mit Begleitschutz")
				if iRand < 3:
					pUnit.setHasPromotion(iPromo, False)
				if gc.getPlayer(iPlayer).isHuman():
					text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_" + str(5 + iRand), (0, 0))
					CyInterface().addMessage(iPlayer, True, 5, text, "AS2D_COMBAT_UNIT", 2,
						"Art/Interface/Buttons/Units/button_merchant.dds", ColorTypes(14), pPlot.getX(), pPlot.getY(), True, True)

					# PopUp Message
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(text)
					popupInfo.addPopup(iPlayer)

			# Generelle Info zur Chance
			text = CyTranslator().getText("TXT_KEY_MESSAGE_MERCHANT_ROBBERY_INFO", (iChance, iMinimumChance))
			CyInterface().addMessage(iPlayer, True, 5, text, None, 2, None, ColorTypes(13), 0, 0, False, False)

			# Einheit killen
			if bKill:
				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, 1, 1)
				pUnit.kill(True, -1)
				return
