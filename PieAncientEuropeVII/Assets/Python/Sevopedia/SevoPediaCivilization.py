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
# Panel and other changes for PAE (Pie) Dec 2021

from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
								FontTypes, GenericButtonSizes,
								WidgetTypes, PanelStyles, CivilopediaPageTypes)
import CvUtil
import SevoScreenEnums

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaCivilization:

	def __init__(self, main):
		self.iCivilization = -1
		self.top = main

		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE
		self.Y_MAIN_PANE = self.top.Y_PEDIA_PAGE

		self.Y_LEADER = self.Y_MAIN_PANE
		self.H_LEADER = 110

		self.Y_BUILDING = self.Y_LEADER + self.H_LEADER + 10
		self.H_BUILDING = 110

		self.H_MAIN_PANE = self.Y_BUILDING + self.H_BUILDING - self.Y_MAIN_PANE
		self.W_MAIN_PANE = self.H_MAIN_PANE

		self.X_LEADER = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.W_LEADER = self.top.R_PEDIA_PAGE - self.X_LEADER

		self.X_BUILDING = self.X_LEADER
		self.W_BUILDING = self.W_LEADER

		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_MAIN_PANE + (self.H_MAIN_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_MAIN_PANE + (self.H_MAIN_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_TECH = self.X_MAIN_PANE
		self.Y_TECH = self.Y_BUILDING + self.H_BUILDING + 10
		self.W_TECH = self.W_MAIN_PANE
		self.H_TECH = 110

		self.X_UNIT = self.X_BUILDING
		self.Y_UNIT = self.Y_BUILDING + self.H_BUILDING + 10
		self.W_UNIT = self.W_BUILDING
		self.H_UNIT = 110

		self.X_TEXT = self.X_MAIN_PANE
		self.Y_TEXT = self.Y_UNIT + self.H_UNIT + 10
		self.W_TEXT = self.top.R_PEDIA_PAGE - self.X_TEXT
		self.H_TEXT = self.top.B_PEDIA_PAGE - self.Y_TEXT



	def interfaceScreen(self, iCivilization):
		self.iCivilization = iCivilization
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.iCivilization).getArtDefineTag()).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placeTech()
		self.placeBuilding()
		self.placeUnit()
		self.placeLeader()
		self.placeText()



	def placeTech(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_FREE_TECHS", ()), "", False, True, self.X_TECH, self.Y_TECH, self.W_TECH, self.H_TECH, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for iTech in xrange(gc.getNumTechInfos()):
			if (gc.getCivilizationInfo(self.iCivilization).isCivilizationFreeTechs(iTech)):
				screen.attachImageButton(panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)



	def placeBuilding(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_UNIQUE_BUILDINGS", ()), "", False, True, self.X_BUILDING, self.Y_BUILDING, self.W_BUILDING, self.H_BUILDING, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for iBuilding in xrange(gc.getNumBuildingClassInfos()):
			iUniqueBuilding = gc.getCivilizationInfo(self.iCivilization).getCivilizationBuildings(iBuilding)
			iDefaultBuilding = gc.getBuildingClassInfo(iBuilding).getDefaultBuildingIndex()
			if (iDefaultBuilding > -1 and iUniqueBuilding > -1 and iDefaultBuilding != iUniqueBuilding):
				screen.attachImageButton(panelName, "", gc.getBuildingInfo(iUniqueBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iUniqueBuilding, 1, False)



	def placeUnit(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_FREE_UNITS", ()), "", False, True, self.X_UNIT, self.Y_UNIT, self.W_UNIT, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for iUnit in xrange(gc.getNumUnitClassInfos()):
			iUniqueUnit = gc.getCivilizationInfo(self.iCivilization).getCivilizationUnits(iUnit)
			iDefaultUnit = gc.getUnitClassInfo(iUnit).getDefaultUnitIndex()
			if (iDefaultUnit > -1 and iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit):
				# PAE: ethnic unit button
				szButton = gc.getUnitInfo(iUniqueUnit).getButton()
				if self.top.iActivePlayer != -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iUniqueUnit)
				screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUniqueUnit, 1, False)

		# PAE Rang/Promo/Special Units (Sondereinheiten mit eigener UnitClass, aber iCost -1)
		LUnits = []
		# ROME
		if self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_ROME") or self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_HASTATI"),
				gc.getInfoTypeForString("UNIT_PRINCIPES"),
				gc.getInfoTypeForString("UNIT_TRIARII"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3"),

				gc.getInfoTypeForString("UNIT_LEGION"),
				gc.getInfoTypeForString("UNIT_LEGION2"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO"),
				#gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"),
				#gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"),
				gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"),

				gc.getInfoTypeForString("UNIT_PRAETORIAN"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"),
				gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3"),

				gc.getInfoTypeForString("UNIT_ROME_COMITATENSES"),
				gc.getInfoTypeForString("UNIT_ROME_LIMITANEI"),
				gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"),
				gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"),
				gc.getInfoTypeForString("UNIT_ROME_PALATINI"),
				gc.getInfoTypeForString("UNIT_ROME_LIMITANEI_GARDE"),
				gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"),

				gc.getInfoTypeForString("UNIT_ARCHER_LEGION"),
				gc.getInfoTypeForString("UNIT_CROSSBOWMAN_ROME")
			]
		elif (self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_GREECE")
			or self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_ATHENS")
			or self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_THEBAI")):
			LUnits = [
				gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"),
				gc.getInfoTypeForString("UNIT_HOPLIT_2"),
				gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"),
				gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS")
			]
		elif self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_SPARTA"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_SPARTA_3")
			]
		elif self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_PEZHETAIROI2"),
				gc.getInfoTypeForString("UNIT_PEZHETAIROI3"),
				gc.getInfoTypeForString("UNIT_PEZHETAIROI4"),
				gc.getInfoTypeForString("UNIT_HYPASPIST2"),
				gc.getInfoTypeForString("UNIT_HYPASPIST3"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"),
				gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH")
			]
		elif self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_APFELTRAEGER"),
				gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"),
				gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"),
				gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2")
			]
		elif self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"),
				gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"),
				gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER")
			]
		elif self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_ASSYRIA") or self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_BABYLON"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_ASSUR_RANG1"),
				gc.getInfoTypeForString("UNIT_ASSUR_RANG2"),
				gc.getInfoTypeForString("UNIT_ASSUR_RANG3"),
				gc.getInfoTypeForString("UNIT_ELITE_ASSUR")
			]
		elif self.iCivilization == gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
			LUnits = [
				gc.getInfoTypeForString("UNIT_SUMER_RANG1"),
				gc.getInfoTypeForString("UNIT_SUMER_RANG2"),
				gc.getInfoTypeForString("UNIT_ELITE_SUMER")
			]

		# PAE Sondereinheiten anzeigen
		for iUniqueUnit in LUnits:
			szButton = gc.getUnitInfo(iUniqueUnit).getButton()
			screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUniqueUnit, 1, False )



	def placeLeader(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_CONCEPT_LEADERS", ()), "", False, True, self.X_LEADER, self.Y_LEADER, self.W_LEADER, self.H_LEADER, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			civ = gc.getCivilizationInfo(self.iCivilization)
			if civ.isLeaders(iLeader):
				screen.attachImageButton(panelName, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, self.iCivilization, False)



	def placeText(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50)
		szText = gc.getCivilizationInfo(self.iCivilization).getCivilopedia()
		screen.attachMultilineText(panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
