# Scenario brettschmitt's XXXL

# Imports 
from CvPythonExtensions import * 
import CvEventInterface
import CvUtil
import PyHelpers

# Defines 
gc = CyGlobalContext() 

def onGameStart():
	
	eBuilding = gc.getInfoTypeForString("BUILDING_SIEDLUNG") # BUILDING_PALACE
	eTechJagd = gc.getInfoTypeForString("TECH_HUNTING")
	eTechFischen = gc.getInfoTypeForString("TECH_FISHING")
	eUnitHunter = gc.getInfoTypeForString("UNIT_HUNTER")
	eUnitBoot = gc.getInfoTypeForString("UNIT_WORKBOAT")
	
	iRange = gc.getMAX_PLAYERS()
	for iPlayer in xrange(iRange):
	
		iResearchBoost = 0
		pPlayer = gc.getPlayer(iPlayer)
		eTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(eTeam)
		
		pCity = pPlayer.getCity(0)
		if pCity != None and pCity.isHasBuilding(eBuilding):
			
			if iPlayer == gc.getInfoTypeForString("CIVILIZATION_ROME"):
				# Palace
				if CvUtil.myRandom(10, "PalaceBoost") < 3: iResearchBoost = 15
				else: iResearchBoost = 10
				
				# Jagd
				if CvUtil.myRandom(10, "GiveTech") < 6:
					# pTeam.setHasTech(TechType eIndex, BOOL bNewValue, PlayerType ePlayer, BOOL bFirst, BOOL bAnnounce)
					pTeam.setHasTech(eTechJagd, 1, iPlayer, 0, 1)
					if CvUtil.myRandom(10, "CreateUnit") < 6:
						pPlayer.initUnit(eUnitHunter, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			   
			if iPlayer == gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"):
				# Palace
				if CvUtil.myRandom(10, "PalaceBoost") < 3: iResearchBoost = 5
				else: iResearchBoost = 10
				
				# Fischen
				if CvUtil.myRandom(10, "GiveTech") < 6:
					pTeam.setHasTech(eTechFischen, 1, iPlayer, 0, 1)
				
				# Jagd
				if CvUtil.myRandom(10, "GiveTech") < 6:
					pTeam.setHasTech(eTechJagd, 1, iPlayer, 0, 1)
					if CvUtil.myRandom(10, "CreateUnit") < 6:
						pPlayer.initUnit(eUnitHunter, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
			if iPlayer == gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
				# Palace
				iRand = CvUtil.myRandom(10, "PalaceBoost")
				if iRand < 2: iResearchBoost = 5
				elif iRand < 3: iResearchBoost = 10
				else: iResearchBoost = 15
				
				# Fischen
				if CvUtil.myRandom(10, "GiveTech") < 8:
					pTeam.setHasTech(eTechFischen, 1, iPlayer, 0, 1)
				
				# Jagd
				if CvUtil.myRandom(10, "GiveTech") < 6:
					pTeam.setHasTech(eTechJagd, 1, iPlayer, 0, 1)
					if CvUtil.myRandom(10, "CreateUnit") < 6:
						pPlayer.initUnit(eUnitHunter, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
			if iPlayer == gc.getInfoTypeForString("CIVILIZATION_GREECE"):
				# Palace
				if CvUtil.myRandom(10, "PalaceBoost") < 3: iResearchBoost = 15
				else: iResearchBoost = 10
				
				# Fischen
				if CvUtil.myRandom(10, "GiveTech") < 8:
					pTeam.setHasTech(eTechFischen, 1, iPlayer, 0, 1)
					if CvUtil.myRandom(10, "CreateUnit") < 6:
						pPlayer.initUnit(eUnitBoot, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
			# alle anderen Spieler: 30% Chance +5 Forschung im Palast
			elif CvUtil.myRandom(10, "PalaceBoost") < 3: iResearchBoost = 5
			
			
			if iResearchBoost > 0:
				eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
				iResearch = pCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_RESEARCH) + iResearchBoost
				pCity.setBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_RESEARCH, iResearch)

