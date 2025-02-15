## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
                                FontTypes, GenericButtonSizes,
                                WidgetTypes, PanelStyles, TableStyles,
                                CyGameTextMgr, CivilopediaPageTypes)
import CvUtil
# import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaReligion:
  "Civilopedia Screen for Religions"

  def __init__(self, main):
    self.iReligion = -1
    self.top = main

    #self.X_MAIN_PANE = 30
    #self.Y_MAIN_PANE = 90
    #self.W_MAIN_PANE = 250
    #self.H_MAIN_PANE = 210

    self.X_ICON = 30 #113
    self.Y_ICON = 90 #148
    self.W_ICON = 120
    self.H_ICON = 120
    self.ICON_SIZE = 64

    self.X_REQUIRES = 160 #330
    self.Y_REQUIRES = 70
    self.W_REQUIRES = 85 #440
    self.H_REQUIRES = 140

    self.X_SPECIAL = 270 #330
    self.Y_SPECIAL = 70 #190
    self.W_SPECIAL = 500 #440
    self.H_SPECIAL = 140

    self.X_TEXT = 30
    self.Y_TEXT = 340 #230
    self.W_TEXT = 743
    self.H_TEXT = 362 #472

    # PAE: buildings pane
    self.X_BUILDING_PANE = 30
    self.Y_BUILDING_PANE = 230
    self.W_BUILDING_PANE = 743
    self.H_BUILDING_PANE = 110

  # Screen construction function
  def interfaceScreen(self, iReligion):

    self.iReligion = iReligion

    self.top.deleteAllWidgets()

    screen = self.top.getScreen()

    bNotActive = (not screen.isActive())
    if bNotActive:
      self.top.setPediaCommonWidgets()

    # Header...
    szHeader = u"<font=4b>" + gc.getReligionInfo(self.iReligion).getDescription().upper() + u"</font>"
    szHeaderId = self.top.getNextWidgetName()
    screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

    # Top
    screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION, -1)

    if self.top.iLastScreen  != CvScreenEnums.PEDIA_RELIGION or bNotActive:
      self.placeLinks(True)
      self.top.iLastScreen = CvScreenEnums.PEDIA_RELIGION
    else:
      self.placeLinks(False)

    # Icon
    #screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
    #    self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
    screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
        self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
    screen.addDDSGFC(self.top.getNextWidgetName(), gc.getReligionInfo(self.iReligion).getButton(),
        self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

    self.placeSpecial()
    self.placeRequires()
    self.placeText()
    self.placeAllows()

  def placeRequires(self):

    screen = self.top.getScreen()

    panelName = self.top.getNextWidgetName()
    screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True,
         self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
    screen.attachLabel(panelName, "", "  ")

    iTech = gc.getReligionInfo(self.iReligion).getTechPrereq()
    if (iTech > -1):
      screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

  def placeSpecial(self):

    screen = self.top.getScreen()

    panelName = self.top.getNextWidgetName()
    screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False,
         self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )

    listName = self.top.getNextWidgetName()
    screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
    screen.enableSelect(listName, False)

    szSpecialText = CyGameTextMgr().parseReligionInfo(self.iReligion, True)
    splitText = string.split( szSpecialText, "\n" )
    for special in splitText:
      if len( special ) != 0:
        screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

    # Special Units
    if self.iReligion == gc.getInfoTypeForString("RELIGION_JUDAISM"):
      iUnit = gc.getInfoTypeForString("UNIT_STADTWACHE_ISRAEL")
      special = localText.getText("TXT_KEY_PEDIA_REL_UNIT", ()) + " " + gc.getUnitInfo(iUnit).getDescription()
      screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, CvUtil.FONT_LEFT_JUSTIFY )

  # PAE: Place buildings, units, promotions
  def placeAllows(self):

    screen = self.top.getScreen()

    panelName = self.top.getNextWidgetName()
    screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_ALLOWS", ()), "", False, True, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

    screen.attachLabel(panelName, "", "  ")

    # Buildings
    for eLoop in xrange(gc.getNumBuildingInfos()):
      if (eLoop != -1):
        if (gc.getBuildingInfo(eLoop).getPrereqReligion() == self.iReligion or gc.getBuildingInfo(eLoop).getHolyCity() == self.iReligion):
          screen.attachImageButton( panelName, "", gc.getBuildingInfo(eLoop).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoop, 1, False )

    # Units
    for eLoop in xrange(gc.getNumUnitInfos()):
      if (eLoop != -1):
        if (gc.getUnitInfo(eLoop).getPrereqReligion() == self.iReligion):
          screen.attachImageButton( panelName, "", gc.getUnitInfo(eLoop).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoop, 1, False )

    # Promotions
    for eLoop in xrange(gc.getNumPromotionInfos()):
      if (eLoop != -1):
        if (gc.getPromotionInfo(eLoop).getStateReligionPrereq() == self.iReligion):
          screen.attachImageButton( panelName, "", gc.getPromotionInfo(eLoop).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, eLoop, 1, False )

  def placeText(self):

    screen = self.top.getScreen()

    panelName = self.top.getNextWidgetName()
    screen.addPanel( panelName, "", "", True, True,
         self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )

    szText = gc.getReligionInfo(self.iReligion).getCivilopedia()
    screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

  def placeLinks(self, bRedraw):

    screen = self.top.getScreen()

    if bRedraw:
      screen.clearListBoxGFC(self.top.LIST_ID)

    # sort Improvements alphabetically
    listSorted=[(0,0)]*gc.getNumReligionInfos()
    for j in xrange(gc.getNumReligionInfos()):
      listSorted[j] = (gc.getReligionInfo(j).getDescription(), j)
    listSorted.sort()

    iSelected = 0
    i = 0
    for iI in xrange(gc.getNumReligionInfos()):
      if (not gc.getReligionInfo(iI).isGraphicalOnly()):
        if bRedraw:
          screen.appendListBoxString( self.top.LIST_ID, listSorted[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, listSorted[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY )
        if listSorted[iI][1] == self.iReligion:
          iSelected = i
        i += 1

    screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

  # Will handle the input for this screen...
  def handleInput (self, inputClass):
    return 0
