# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#
# changes for PAE (Pie) Dec 2021

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaUnit:

	def __init__(self, main):
		self.iUnit = -1
		self.top = main

		self.X_UNIT_PANE = self.top.X_PEDIA_PAGE
		self.Y_UNIT_PANE = self.top.Y_PEDIA_PAGE
		self.W_UNIT_PANE = 350
		self.H_UNIT_PANE = 180

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_UNIT_PANE + 10
		self.Y_ICON = self.Y_UNIT_PANE + (self.H_UNIT_PANE - self.H_ICON) / 2

		self.ICON_SIZE = 64
		self.BUTTON_SIZE = 64
		self.PROMOTION_ICON_SIZE = 32

		self.X_STATS_PANE = self.X_ICON + self.W_ICON + 10
		self.Y_STATS_PANE = self.Y_UNIT_PANE + 42
		self.W_STATS_PANE = 250
		self.H_STATS_PANE = self.H_UNIT_PANE

		self.X_PROMO_PANE = self.X_UNIT_PANE + self.W_UNIT_PANE + 10
		self.Y_PROMO_PANE = self.Y_UNIT_PANE
		self.W_PROMO_PANE = 400
		self.H_PROMO_PANE = self.H_UNIT_PANE

		self.X_UNIT_ANIMATION = self.X_PROMO_PANE + self.W_PROMO_PANE + 10
		self.W_UNIT_ANIMATION = self.top.R_PEDIA_PAGE - self.X_UNIT_ANIMATION
		self.Y_UNIT_ANIMATION = self.Y_UNIT_PANE + 7
		self.H_UNIT_ANIMATION = self.H_UNIT_PANE - 7
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

		self.X_SPECIAL_PANE = self.X_UNIT_PANE
		self.Y_SPECIAL_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE + 10
		self.W_SPECIAL_PANE = self.W_UNIT_PANE
		self.H_SPECIAL_PANE = self.top.B_PEDIA_PAGE - self.Y_SPECIAL_PANE

		self.X_PREREQ_PANE = self.X_SPECIAL_PANE + self.W_UNIT_PANE + 10
		self.Y_PREREQ_PANE = self.Y_SPECIAL_PANE
		self.W_PREREQ_PANE = self.W_PROMO_PANE
		self.H_PREREQ_PANE = 100

		self.X_UPGRADES_TO_PANE = self.X_PREREQ_PANE + self.W_PREREQ_PANE + 10
		self.Y_UPGRADES_TO_PANE = self.Y_PREREQ_PANE
		self.W_UPGRADES_TO_PANE = self.top.R_PEDIA_PAGE - self.X_UPGRADES_TO_PANE
		self.H_UPGRADES_TO_PANE = self.H_PREREQ_PANE

		self.X_HISTORY_PANE = self.X_PREREQ_PANE
		self.Y_HISTORY_PANE = self.Y_PREREQ_PANE + self.H_PREREQ_PANE + 10
		self.W_HISTORY_PANE = self.top.R_PEDIA_PAGE - self.X_HISTORY_PANE
		self.H_HISTORY_PANE = self.top.B_PEDIA_PAGE - self.Y_HISTORY_PANE



	def interfaceScreen(self, iUnit):
		self.iUnit = iUnit
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		# PAE correct button for CIV
		szButton = gc.getUnitInfo(self.iUnit).getButton()
		if self.top.iActivePlayer != -1:
			szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(self.iUnit)
		screen.addDDSGFC(self.top.getNextWidgetName(), szButton, self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addUnitGraphicGFC(self.top.getNextWidgetName(), self.iUnit, self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		self.placeUpgradesTo()
		self.placeRequires()
		self.placeSpecial()
		self.placePromotions()
		self.placeHistory()



	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		iCombatType = gc.getUnitInfo(self.iUnit).getUnitCombatType()
		if (iCombatType != -1):
			screen.setImageButton(self.top.getNextWidgetName(), gc.getUnitCombatInfo(iCombatType).getButton(), self.X_STATS_PANE, self.Y_STATS_PANE - 35, 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=4>" + gc.getUnitCombatInfo(iCombatType).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 37, self.Y_STATS_PANE - 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		if (gc.getUnitInfo(self.iUnit).getAirCombat() > 0 and gc.getUnitInfo(self.iUnit).getCombat() == 0):
			iStrength = gc.getUnitInfo(self.iUnit).getAirCombat()
		else:
			iStrength = gc.getUnitInfo(self.iUnit).getCombat()
		szName = self.top.getNextWidgetName()
		szStrength = localText.getText("TXT_KEY_PEDIA_STRENGTH", (iStrength,))
		screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szStrength.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		szName = self.top.getNextWidgetName()
		szMovement = localText.getText("TXT_KEY_PEDIA_MOVEMENT", (gc.getUnitInfo(self.iUnit).getMoves(),))
		screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szMovement.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# PAE: not buildable units
		if gc.getUnitInfo(self.iUnit).getProductionCost() == -1:
			szText = localText.getText("TXT_KEY_PEDIA_NOCOST", ())
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		elif (gc.getUnitInfo(self.iUnit).getProductionCost() >= 0 and not gc.getUnitInfo(self.iUnit).isFound()):
			if self.top.iActivePlayer == -1:
				iKosten = gc.getUnitInfo(self.iUnit).getProductionCost() * gc.getDefineINT("UNIT_PRODUCTION_PERCENT") / 100
			else:
				iKosten = gc.getActivePlayer().getUnitProductionNeeded(self.iUnit)
			szCost = localText.getText("TXT_KEY_PEDIA_COST", ( iKosten, ) )
			szText = u"<font=3>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
			if gc.getUnitInfo(self.iUnit).isMilitaryHappiness():
				if self.iUnit == gc.getInfoTypeForString("UNIT_WARRIOR") or self.iUnit == gc.getInfoTypeForString("UNIT_HUNTER"): iKosten = 0
				szText += u" %d%c" % (iKosten / 2, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
			szText += u"</font>"
			screen.appendListBoxStringNoUpdate(panelName, szText, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getUnitInfo(self.iUnit).getAirRange() > 0):
			szRange = localText.getText("TXT_KEY_PEDIA_RANGE", (gc.getUnitInfo(self.iUnit).getAirRange(),))
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szRange.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# PAE more infos
		iUnitClass = gc.getUnitInfo(self.iUnit).getUnitClassType()
		if gc.getUnitClassInfo(iUnitClass).getMaxPlayerInstances() != -1:
			szText = localText.getText("TXT_KEY_PEDIA_MAX_PLAYER", ( gc.getUnitClassInfo(iUnitClass).getMaxPlayerInstances(), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if gc.getUnitClassInfo(iUnitClass).getMaxGlobalInstances() != -1:
			szText = localText.getText("TXT_KEY_PEDIA_MAX_GLOBAL", ( gc.getUnitClassInfo(iUnitClass).getMaxGlobalInstances(), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if gc.getUnitInfo(self.iUnit).getExtraCost() > 0:
			szText = localText.getText("TXT_KEY_UNIT_EXTRA_COST", ( gc.getUnitInfo(self.iUnit).getExtraCost(), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		screen.updateListBox(panelName)



	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")

		# BTS was: Tech | Bonus | Religion | Building
		# PAE swaps displayed requirements: Tech | Religion | Building | Coorp | Bonus (Bonus at last because of AND and OR)

		# add tech buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTech()
		if (iPrereq >= 0):
			screen.attachImageButton(panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False)
		for j in xrange(gc.getDefineINT("NUM_UNIT_AND_TECH_PREREQS")):
			iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTechs(j)
			if (iPrereq >= 0):
				screen.attachImageButton(panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, -1, False)

		# Religion
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqReligion()
		if (iPrereq >= 0):
			screen.attachImageButton(panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_RELIGION, iPrereq, -1, False)

		# Building
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqBuilding()
		if (iPrereq >= 0):
			screen.attachImageButton(panelName, "", gc.getBuildingInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPrereq, -1, False)

		# Corporation
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqCorporation()
		if iPrereq >= 0:
				screen.attachImageButton( panelName, "", gc.getCorporationInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, iPrereq, -1, False )

		# Bonuses
		bFirst = True
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndBonus()
		if (iPrereq >= 0):
			bFirst = False
			screen.attachImageButton(panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)
		nOr = 0
		for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			if (gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j) > -1):
				nOr += 1
		szLeftDelimeter = ""
		szRightDelimeter = ""
		if (not bFirst):
			if (nOr > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "("
				szRightDelimeter = ") "
			elif (nOr > 0):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ())
		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panelName, "", szLeftDelimeter)
		bFirst = True
		for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			eBonus = gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j)
			if (eBonus > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton(panelName, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False)
		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)



	def placeUpgradesTo(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_UPGRADES_TO", ()), "", False, True, self.X_UPGRADES_TO_PANE, self.Y_UPGRADES_TO_PANE, self.W_UPGRADES_TO_PANE, self.H_UPGRADES_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for k in xrange(gc.getNumUnitClassInfos()):
			if self.top.iActivePlayer == -1:
				eLoopUnit = gc.getUnitClassInfo(k).getDefaultUnitIndex()
			else:
				eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(k)
			if eLoopUnit >= 0 and gc.getUnitInfo(self.iUnit).getUpgradeUnitClass(k):
				# PAE correct CIV unit button
				szButton = gc.getUnitInfo(eLoopUnit).getButton()
				if self.top.iActivePlayer != -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
				screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False)



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		listName = self.top.getNextWidgetName()
		szSpecialText = CyGameTextMgr().getUnitHelp(self.iUnit, True, False, False, None)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		textName = self.top.getNextWidgetName()
		szText = u""
		if len(gc.getUnitInfo(self.iUnit).getStrategy()) > 0:
			szText += localText.getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += gc.getUnitInfo(self.iUnit).getStrategy()
			szText += u"\n\n"
		szText += localText.getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		szText += gc.getUnitInfo(self.iUnit).getCivilopedia()
		screen.addMultilineText(textName, szText, self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40, self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placePromotions(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", True, True, self.X_PROMO_PANE, self.Y_PROMO_PANE, self.W_PROMO_PANE, self.H_PROMO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.X_PROMO_PANE+15, self.Y_PROMO_PANE+40, self.W_PROMO_PANE-20, self.H_PROMO_PANE-40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
		for k in xrange(gc.getNumPromotionInfos()):
			if isPromotionValid(k, self.iUnit, False) and not gc.getPromotionInfo(k).isGraphicalOnly():
				# PAE break at unit battle formations
				if "_FORM_" in gc.getPromotionInfo(k).getType():
					break
				screen.appendMultiListButton(rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, False)



	def handleInput (self, inputClass):
		return 0
