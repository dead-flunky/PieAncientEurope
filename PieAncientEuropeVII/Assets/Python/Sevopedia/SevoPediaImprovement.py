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

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums
import string

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaImprovement:

	def __init__(self, main):
		self.iImprovement = -1
		self.top = main

		self.X_UPPER_PANE = self.top.X_PEDIA_PAGE
		self.Y_UPPER_PANE = self.top.Y_PEDIA_PAGE
		self.W_UPPER_PANE = 210
		self.H_UPPER_PANE = 210

		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_UPPER_PANE + (self.H_UPPER_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_UPPER_PANE + (self.H_UPPER_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.W_BONUS_YIELDS_PANE = 200
		self.X_BONUS_YIELDS_PANE = self.top.R_PEDIA_PAGE - self.W_BONUS_YIELDS_PANE + 5
		self.Y_BONUS_YIELDS_PANE = self.Y_UPPER_PANE
		self.H_BONUS_YIELDS_PANE = self.top.B_PEDIA_PAGE - self.Y_BONUS_YIELDS_PANE

		self.X_IMPROVENEMT_ANIMATION = self.X_UPPER_PANE + self.W_UPPER_PANE + 10
		self.W_IMPROVENEMT_ANIMATION = self.top.R_PEDIA_PAGE - self.X_IMPROVENEMT_ANIMATION - self.W_BONUS_YIELDS_PANE - 10
		self.Y_IMPROVENEMT_ANIMATION = self.Y_UPPER_PANE + 7
		self.H_IMPROVENEMT_ANIMATION = self.H_UPPER_PANE - 7
		self.X_ROTATION_IMPROVENEMT_ANIMATION = -20
		self.Z_ROTATION_IMPROVENEMT_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		self.X_REQUIRES = self.X_UPPER_PANE
		self.Y_REQUIRES = self.Y_UPPER_PANE + self.H_UPPER_PANE + 10
		self.W_REQUIRES = 400
		self.H_REQUIRES = 110

		self.X_IMPROVEMENTS_PANE = self.X_UPPER_PANE
		self.Y_IMPROVEMENTS_PANE = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_IMPROVEMENTS_PANE = self.W_REQUIRES
		self.H_IMPROVEMENTS_PANE = self.top.B_PEDIA_PAGE - self.Y_IMPROVEMENTS_PANE

		self.X_EFFECTS = self.X_UPPER_PANE + self.W_REQUIRES + 10
		self.Y_EFFECTS = self.Y_REQUIRES
		self.W_EFFECTS = self.top.R_PEDIA_PAGE - self.X_EFFECTS - self.W_BONUS_YIELDS_PANE - 5
		self.H_EFFECTS = self.top.B_PEDIA_PAGE - self.Y_EFFECTS


	def interfaceScreen(self, iImprovement):
	
		# PAE
		global Latifundien
		Latifundien = [
			gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1"),
			gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM2"),
			gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM3"),
			gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4"),
			gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5")
		]
		global LImprFortSentry
		LImprFortSentry = [
			gc.getInfoTypeForString("IMPROVEMENT_TURM"),
			gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
			gc.getInfoTypeForString("IMPROVEMENT_FORT"),
			gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
			gc.getInfoTypeForString("IMPROVEMENT_LIMES9"),
			gc.getInfoTypeForString("IMPROVEMENT_LIMES2_9"),
			gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
		]
	
		self.iImprovement = iImprovement
		screen = self.top.getScreen()

		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_UPPER_PANE, self.Y_UPPER_PANE, self.W_UPPER_PANE, self.H_UPPER_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getImprovementInfo(self.iImprovement).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addImprovementGraphicGFC(self.top.getNextWidgetName(), self.iImprovement, self.X_IMPROVENEMT_ANIMATION, self.Y_IMPROVENEMT_ANIMATION, self.W_IMPROVENEMT_ANIMATION, self.H_IMPROVENEMT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_IMPROVENEMT_ANIMATION, self.Z_ROTATION_IMPROVENEMT_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeSpecial()
		self.placeBonusYield()
		self.placeYield()
		self.placeRequires()



	def placeYield(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, True, self.X_IMPROVEMENTS_PANE, self.Y_IMPROVEMENTS_PANE, self.W_IMPROVEMENTS_PANE, self.H_IMPROVEMENTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)
		info = gc.getImprovementInfo(self.iImprovement)

		# PAE: Baukosten
		for k in xrange(gc.getNumBuildInfos()):
			if (gc.getBuildInfo(k).getImprovement() == self.iImprovement):
				szYield = (u"%s: -%i%c\n" % (gc.getBuildInfo(k).getText(), gc.getBuildInfo(k).getCost(),gc.getCommerceInfo(0).getChar() ))
				screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getYieldChange(k)
			if (iYieldChange != 0):
				szYield = u""
				if (iYieldChange > 0):
					sign = "+"
				else:
					sign = ""
				szYield += (u"%s: %s%i%c" % (gc.getYieldInfo(k).getDescription(), sign, iYieldChange, gc.getYieldInfo(k).getChar()))
				screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getIrrigatedYieldChange(k)
			if (iYieldChange != 0):
				szYield = localText.getText("TXT_KEY_PEDIA_IRRIGATED_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar()))
				screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getHillsYieldChange(k)
			if (iYieldChange != 0):
				szYield = localText.getText("TXT_KEY_PEDIA_HILLS_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar()))
				screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			szYield = u""
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getRiverSideYieldChange(k)
			if (iYieldChange != 0):
				szYield = localText.getText("TXT_KEY_PEDIA_RIVER_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar()))
				screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for iTech in xrange(gc.getNumTechInfos()):
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				szYield = u""
				iYieldChange = gc.getImprovementInfo(self.iImprovement).getTechYieldChanges(iTech, k)
				if (iYieldChange != 0):
					szYield = localText.getText("TXT_KEY_PEDIA_TECH_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getTechInfo(iTech).getDescription()))
					screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for iCivic in xrange(gc.getNumCivicInfos()):
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				szYield = u""
				iYieldChange = gc.getCivicInfo(iCivic).getImprovementYieldChanges(self.iImprovement, k)
				if (iYieldChange != 0):
					szYield = localText.getText("TXT_KEY_PEDIA_TECH_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getCivicInfo(iCivic).getDescription()))
					screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		for iRoute in xrange(gc.getNumRouteInfos()):
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(self.iImprovement).getRouteYieldChanges(iRoute, k)
				if (iYieldChange != 0):										
					szYield += localText.getText("TXT_KEY_PEDIA_ROUTE_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getRouteInfo(iRoute).getTextKey())) + u"\n"
					screen.appendListBoxString( listName, szYield, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )



	def placeBonusYield(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BONUS_YIELDS", ()), "", True, True, self.X_BONUS_YIELDS_PANE, self.Y_BONUS_YIELDS_PANE, self.W_BONUS_YIELDS_PANE, self.H_BONUS_YIELDS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		info = gc.getImprovementInfo(self.iImprovement)
		for j in xrange(gc.getNumBonusInfos()):
			bFirst = True
			szYield = u""
			bEffect = False
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = info.getImprovementBonusYield(j, k)
				if (iYieldChange != 0):
					bEffect = True
					# Uncomment for 3.13 behavior. Note that Uranium shows incorrect hammer yield (should be +2)
					#iYieldChange += info.getYieldChange(k)
					if (bFirst):
						bFirst = False
					else:
						szYield += u", "
					if (iYieldChange > 0):
						sign = u"+"
					else:
						sign = u""
					szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar()))
			if (bEffect):
				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childPanelName, "", "  ")
				screen.attachImageButton( childPanelName, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, j, 1, False )
				screen.attachLabel(childPanelName, "", u"<font=4>" + szYield + u"</font>")



	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		for iBuild in xrange(gc.getNumBuildInfos()):
			if (gc.getBuildInfo(iBuild).getImprovement() == self.iImprovement):
				iTech = gc.getBuildInfo(iBuild).getTechPrereq()
				if (iTech > -1):
					screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

		# PAE Units that can build that
		if self.iImprovement in Latifundien:
			if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1"):
				iUnit = gc.getInfoTypeForString("UNIT_PRAETORIAN")
				screen.attachImageButton( panelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )
			else:
				iImp = gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1")
				screen.attachImageButton( panelName, "", gc.getImprovementInfo(iImp).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImp, 1, False )

				iUnit = gc.getInfoTypeForString("UNIT_SLAVE")

				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
				screen.attachImageButton( childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )

				if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM3") or self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4") or self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5"):
					screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
					screen.attachImageButton( childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )

				if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4") or self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5"):
					screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
					screen.attachImageButton( childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )

				if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5"):
					screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
					screen.attachImageButton( childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )


		elif self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"):
			iUnit = gc.getInfoTypeForString("UNIT_TRADE_MERCHANT")
			screen.attachImageButton( panelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )
			iUnit = gc.getInfoTypeForString("UNIT_CARAVAN")
			screen.attachImageButton( panelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )

		# PAE: Units that can build the improvement
		# Sevopedia funkt damit nicht richtig
		#bFirst = True
		#for iUnit in xrange(gc.getNumUnitInfos()):
		#	if gc.getUnitInfo(iUnit).getBuilds(self.iImprovement):
		#		#if not bFirst:
		#		#	screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
		#		#else:
		#		#	bFirst = False
		#		# PAE: ethnic unit button
		#		szButton = gc.getUnitInfo(iUnit).getButton()
		#		if self.top.iActivePlayer != -1:
		#			szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iUnit)
		#		screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		szSpecialText = CyGameTextMgr().getImprovementHelp(self.iImprovement, True)

		# PAE: isFreshWaterValid
		if gc.getImprovementInfo(self.iImprovement).isFreshWaterMakesValid():
			szSpecialText += u"\n" + localText.getText("TXT_KEY_INFO_FRESHWATERMAKESVALID", ())
		# PAE: Latifundien (Prätis bauen es, Sklaven beschleunigen es)
		if self.iImprovement in Latifundien:
			szSpecialText += u"\n" + localText.getText("TXT_KEY_INFO_IMPROVEMENT_LATIFUNDIEN", ())
		if self.iImprovement in LImprFortSentry:
			szSpecialText += u"\n" + localText.getText("TXT_KEY_INFO_IMPROVEMENT_SENTRY", ())

		# Text wird hier ausgegeben
		screen.addMultilineText(listName, szSpecialText, self.X_EFFECTS+5, self.Y_EFFECTS+5, self.W_EFFECTS-10, self.H_EFFECTS-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
