## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvScreensInterface
import PAE_Lists as L

PIXEL_INCREMENT = 7
BOX_INCREMENT_WIDTH = 33 # Used to be 33 #Should be a multiple of 3...
BOX_INCREMENT_HEIGHT = 9 #Should be a multiple of 3...
BOX_INCREMENT_Y_SPACING = 6 #Should be a multiple of 3...
BOX_INCREMENT_X_SPACING = 9 #Should be a multiple of 3...

TECH_BUTTON_SIZE = 49  # PAE: 49 bigger Techbutton  40 unten: y=12 statt 8 ?
TEXTURE_SIZE = 24
# PAE
X_START = 6 + TECH_BUTTON_SIZE
#X_START = 6
X_INCREMENT = 27
Y_ROW = 32

CIV_HAS_TECH = 0
CIV_IS_RESEARCHING = 1
CIV_NO_RESEARCH = 2
CIV_TECH_AVAILABLE = 3

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# BUG - GP Tech Prefs - start
import TechPrefs
import BugCore
BugOpt = BugCore.game.Advisors
ClockOpt = BugCore.game.NJAGC

import BugUtil

PREF_ICON_SIZE = 24
PREF_ICON_TOP = 168
PREF_ICON_LEFT = 10

FLAVORS = [ TechPrefs.FLAVOR_PRODUCTION, TechPrefs.FLAVOR_GOLD, TechPrefs.FLAVOR_SCIENCE,
            TechPrefs.FLAVOR_CULTURE, TechPrefs.FLAVOR_RELIGION ]
UNIT_CLASSES = [ "UNITCLASS_ENGINEER", "UNITCLASS_MERCHANT", "UNITCLASS_SCIENTIST",
                 "UNITCLASS_ARTIST", "UNITCLASS_PROPHET" ]
# BUG - GP Tech Prefs - end

# BUG - 3.19 No Espionage - start
import GameUtil
# BUG - 3.19 No Espionage - end

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# BUG - Tech Era Colors - start
def getEraDescription(eWidgetType, iData1, iData2, bOption):
    return gc.getEraInfo(iData1).getDescription()
# BUG - Tech Era Colors - end

# BUG - GP Tech Prefs - start
def resetTechPrefs(args=[]):
    CvScreensInterface.techChooser.resetTechPrefs()

def getAllTechPrefsHover(widgetType, iData1, iData2, bOption):
    #return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_ALL", CvScreensInterface.techChooser.pPrefs.getAllFlavorTechs(iData1))
    return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_ALL", CvScreensInterface.techChooser.pPrefs.getRemainingFlavorTechs(iData1)) # K-Mod

def getCurrentTechPrefsHover(widgetType, iData1, iData2, bOption):
    return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_CURRENT", CvScreensInterface.techChooser.pPrefs.getCurrentFlavorTechs(iData1))

def getFutureTechPrefsHover(widgetType, iData1, iData2, bOption):
    pPlayer = gc.getPlayer(CvScreensInterface.techChooser.iCivSelected)
    sTechs = set()
    for i in range(gc.getNumTechInfos()):
        if (pPlayer.isResearchingTech(i)):
            sTechs.add(CvScreensInterface.techChooser.pPrefs.getTech(i))
    return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_FUTURE", CvScreensInterface.techChooser.pPrefs.getCurrentWithFlavorTechs(iData1, sTechs))

def buildTechPrefsHover(key, lTechs):
    szText = BugUtil.getPlainText(key) + "\n"
    for pTech in lTechs:
        szText += "<img=%s size=24></img>" % pTech.getInfo().getButton().replace(" ", "_")
    return szText
# BUG - GP Tech Prefs - end

class CvTechChooser:
    "Tech Chooser Screen"

    def __init__(self):
        self.nWidgetCount = 0
        self.iCivSelected = 0
        self.aiCurrentState = []
        self.sWidgets = []

        # Advanced Start
        self.m_iSelectedTech = -1
        self.m_bSelectedTechDirty = false
        self.m_bTechRecordsDirty = false

# BUG - GP Tech Prefs - start
        self.bPrefsShowing = False
        self.resetTechPrefs()
# BUG - GP Tech Prefs - end

        
        self.sTechSelectTab = self.getNextWidgetName("TechSelectTab")
        self.sTechTradeTab = self.getNextWidgetName("TechTradeTab")
        self.sTechTabID = self.sTechSelectTab
        
        self.PIXEL_INCREMENT = 7
        self.BOX_INCREMENT_WIDTH = 30 # Used to be 33 #Should be a multiple of 3...
        self.BOX_INCREMENT_HEIGHT = 9 #Should be a multiple of 3...
        self.BOX_INCREMENT_Y_SPACING = 6 #Should be a multiple of 3...
        self.BOX_INCREMENT_X_SPACING = 9 #Should be a multiple of 3...

    def getScreen(self):
        return CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

    def hideScreen (self):
        # Get the screen
        screen = self.getScreen()

        # Hide the screen
        screen.hideScreen()

    # Screen construction function
    def interfaceScreen(self):
#       BugUtil.debug("CvTechChooser: interfacescreen")
#       self.timer = BugUtil.Timer("CvTechChooser")

        if CyGame().isPitbossHost():
            return

        # Create a new screen, called TechChooser, using the file CvTechChooser.py for input
        screen = self.getScreen()
        screen.setRenderInterfaceOnly(True)
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

        screen.hide("AddTechButton")
        screen.hide("ASPointsLabel")
        screen.hide("SelectedTechLabel")

# BUG - GP Tech Prefs - start
        self.NO_TECH_ART = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
# BUG - GP Tech Prefs - end

        if CyGame().isDebugMode():
            screen.addDropDownBoxGFC( "CivDropDown", 22, 12, 192, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
            screen.setActivation( "CivDropDown", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
            for j in range(gc.getMAX_PLAYERS()):
                if (gc.getPlayer(j).isAlive()):
                    screen.addPullDownString( "CivDropDown", gc.getPlayer(j).getName(), j, j, False )
        else:
            screen.hide( "CivDropDown" )

        if screen.isPersistent() and self.iCivSelected == gc.getGame().getActivePlayer():
            self.updateTechRecords(false)
            return

        self.nWidgetCount = 0
        self.sWidgets = []

        self.iCivSelected = gc.getGame().getActivePlayer()
        self.aiCurrentState = []
        screen.setPersistent( True )

        # Advanced Start
        if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() >= 0):

            self.m_bSelectedTechDirty = true

            self.X_ADD_TECH_BUTTON = 10
            self.Y_ADD_TECH_BUTTON = 731
            self.W_ADD_TECH_BUTTON = 150
            self.H_ADD_TECH_BUTTON = 30
            self.X_ADVANCED_START_TEXT = self.X_ADD_TECH_BUTTON + self.W_ADD_TECH_BUTTON + 20

            szText = localText.getText("TXT_KEY_WB_AS_ADD_TECH", ())
            screen.setButtonGFC( "AddTechButton", szText, "", self.X_ADD_TECH_BUTTON, self.Y_ADD_TECH_BUTTON, self.W_ADD_TECH_BUTTON, self.H_ADD_TECH_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
            screen.hide("AddTechButton")

# BUG - Tech Screen Resolution - start
        if BugOpt.isWideTechScreen() and screen.getXResolution() > 1024:
            xPanelWidth = screen.getXResolution() - 60
        else:
            xPanelWidth = 1024
        yPanelHeight = 768

        screen.showWindowBackground(False)
        screen.setDimensions((screen.getXResolution() - xPanelWidth) / 2, screen.centerY(0), xPanelWidth, yPanelHeight)
        # PAE
        # screen.setDimensions(screen.centerX(0), screen.centerY(0), xPanelWidth, yPanelHeight)
# BUG - Tech Screen Resolution - end

        screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, xPanelWidth, 55, PanelStyles.PANEL_STYLE_TOPBAR )
        # PAE
        # screen.addDDSGFC("TechBG", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 48, xPanelWidth, 672, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        # screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, xPanelWidth, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
        # screen.setText( "TechChooserExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xPanelWidth - 30, 726, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
        screen.addDDSGFC("TechBG", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 51, xPanelWidth, yPanelHeight - 96, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, yPanelHeight - 55, xPanelWidth, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
        screen.setText( "TechChooserExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xPanelWidth - 30, yPanelHeight - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
        screen.setActivation( "TechChooserExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

        # Header...
        szText = u"<font=4>"
        szText = szText + localText.getText("TXT_KEY_TECH_CHOOSER_TITLE", ()).upper()
        szText = szText + u"</font>"
        # PAE
        # screen.setLabel( "TechTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, (xPanelWidth / 2) - 10, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setLabel( "TechTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xPanelWidth / 2, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        # Make the scrollable area for the city list...
        if BugOpt.isShowGPTechPrefs():
            iX = 80
            iW = xPanelWidth - 80
        else:
            iX = 0
            iW = xPanelWidth

        self.TabPanels = ["TechList", "TechTrade"]

        # screen.addScrollPanel(self.TabPanels[0], u"", iX, 64, iW, yPanelHeight - 142, PanelStyles.PANEL_STYLE_EXTERNAL)
        # PAE
        # screen.addScrollPanel(self.TabPanels[0], u"", 0, 64, xPanelWidth, 626, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.addScrollPanel(self.TabPanels[0], u"", iX, 56, iW, yPanelHeight - 134, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.setActivation(self.TabPanels[0], ActivationTypes.ACTIVATE_NORMAL)

        # PAE
        # screen.hide(self.TabPanels[0])
        
        screen.addScrollPanel(self.TabPanels[1], u"", 80, 64, xPanelWidth - 80, yPanelHeight - 142, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.setActivation(self.TabPanels[1], ActivationTypes.ACTIVATE_NORMAL)

# BUG - GP Tech Prefs - start
        if BugOpt.isShowGPTechPrefs():
            screen.addPanel("GPTechPref", u"", u"", True, False, 0, 51, 80, yPanelHeight - 95, PanelStyles.PANEL_STYLE_MAIN_WHITE)
# BUG - GP Tech Prefs - end

        # Add the Highlight
        #screen.addDDSGFC( "TechHighlight", ArtFileMgr.getInterfaceArtInfo("TECH_HIGHLIGHT").getPath(), 0, 0, self.getXStart() + 6, 12 + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ), WidgetTypes.WIDGET_GENERAL, -1, -1 )
        #screen.hide( "TechHighlight" )

        self.X_SELECT_TAB = 30
        self.X_TRADE_TAB = 165
        self.Y_TABS = 730

        # reset widget array so that the above never get deleted
        self.nWidgetCount = 0
        self.sWidgets = []

        self.ConstructTabs()

        self.ShowTab()

        return

    def ConstructTabs(self):
#       BugUtil.debug("cvTechChooser: ConstructTabs")

        screen = self.getScreen()

        self.BOX_INCREMENT_WIDTH = 30 # Used to be 33 #Should be a multiple of 3...
        self.DrawTechChooser(screen, self.TabPanels[0], True, True, True, True, True, True)

        self.BOX_INCREMENT_WIDTH = 12 # Used to be 33 #Should be a multiple of 3...
        self.DrawTechChooser(screen, self.TabPanels[1], True, False, True, False, False, True)
        self.BOX_INCREMENT_WIDTH = 30 # Used to be 33 #Should be a multiple of 3...

    def ShowTab(self):
#       BugUtil.debug("cvTechChooser: ShowTab")

        screen = self.getScreen()

        for tp in self.TabPanels:
            screen.hide(tp)

        # remove these 2 lines when we return to multi-tab screen and uncomment out the 10 below.
        screen.show(self.TabPanels[0])
        screen.setFocus(self.TabPanels[0])

#       if(self.sTechTabID == self.sTechSelectTab):
#           screen.setText(self.sTechSelectTab, "", "Tech Select", CvUtil.FONT_LEFT_JUSTIFY, self.X_SELECT_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#           screen.setText(self.sTechTradeTab, "", "Tech Trade - under development", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRADE_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#           screen.show(self.TabPanels[0])
#           screen.setFocus(self.TabPanels[0])

#       elif(self.sTechTabID == self.sTechTradeTab):
#           screen.setText(self.sTechSelectTab, "", "Tech Select", CvUtil.FONT_LEFT_JUSTIFY, self.X_SELECT_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#           screen.setText(self.sTechTradeTab, "", "Tech Trade - under development", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRADE_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#           screen.show(self.TabPanels[1])
#           screen.setFocus(self.TabPanels[1])


    def DrawTechChooser(self, screen, sPanel, bTechPanel, bTechName, bTechIcon, bTechDetails, bANDPreReq, bORPreReq):
#       BugUtil.debug("cvTechChooser: DrawTechChooser (%s)", sPanel)
#       self.timer.reset()
#       self.timer.start()

        # Place the tech blocks
        self.placeTechs(screen, sPanel, bTechPanel, bTechName, bTechIcon, bTechDetails)

        # Draw the arrows
        self.drawArrows(screen, sPanel, bANDPreReq, bORPreReq)

        self.updateTechPrefs()

        screen.moveToFront( "CivDropDown" )

        screen.moveToFront( "AddTechButton" )

#       self.timer.logSpan("total")

    def placeTechs(self, screen, sPanel, bTechPanel, bTechName, bTechIcon, bTechDetails):
#       BugUtil.debug("cvTechChooser: placeTechs")
        global L

        iMaxX = 0
        iMaxY = 0

        if sPanel == self.TabPanels[0]:
            sPanelWidget = ""
        else:
            sPanelWidget = sPanel

        # If we are the Pitboss, we don't want to put up an interface at all
        if ( CyGame().isPitbossHost() ):
            return

        # Go through all the techs
        for i in range(gc.getNumTechInfos()):

            # Create and place a tech in its proper location
            iX = 30 + ((gc.getTechInfo(i).getGridX() - 1) * ((self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH) * self.PIXEL_INCREMENT))
            iY = (gc.getTechInfo(i).getGridY() - 1) * (self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT) + 5
            szTechRecord = sPanelWidget + "TechRecord" + str(i)

            if iMaxX < iX + self.getXStart():
                iMaxX = iX + self.getXStart()
            if iMaxY < iY + (self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT):
                iMaxY = iY + (self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT)

# BUG - Tech Era Colors - start
            szTechRecordShadow = sPanelWidget + "TechRecordShadow" + str(i)
            iShadowOffset = 9
            screen.attachPanelAt( sPanel, szTechRecordShadow, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6 + iShadowOffset, iY - 6 + iShadowOffset, self.getXStart() + 6, 12 + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ), WidgetTypes.WIDGET_TECH_CHOOSER_ERA, gc.getTechInfo(i).getEra(), -1 )
            self.setTechPanelShadowColor(screen, szTechRecordShadow, gc.getTechInfo(i).getEra())
            screen.hide(szTechRecordShadow)
# BUG - Tech Era Colors - end

            screen.attachPanelAt(sPanel, szTechRecord, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6, iY - 6, self.getXStart() + 6, 12 + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ), WidgetTypes.WIDGET_TECH_TREE, i, -1 )
            screen.setActivation( szTechRecord, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
            screen.hide( szTechRecord )

            #reset so that it offsets from the tech record's panel
            iX = 6
            iY = 6

            if gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i):
                screen.setPanelColor(szTechRecord, 85, 150, 87)
                self.aiCurrentState.append(CIV_HAS_TECH)
            elif gc.getPlayer(self.iCivSelected).getCurrentResearch() == i:
                screen.setPanelColor(szTechRecord, 104, 158, 165)
                self.aiCurrentState.append(CIV_IS_RESEARCHING)
            elif gc.getPlayer(self.iCivSelected).isResearchingTech(i):
                screen.setPanelColor(szTechRecord, 104, 158, 165)
                self.aiCurrentState.append(CIV_IS_RESEARCHING)
            elif gc.getPlayer(self.iCivSelected).canEverResearch(i):
                # Dieses Farbschema ist 2x in dieser Datei enthalten !!!
                # This file contains two copies of this colour scheme
                iEra = gc.getTechInfo(i).getEra()
                if iEra == 4: 
                    screen.setPanelColor(szTechRecord, 130, 70, 0) #braun
                elif iEra == 3: 
                    screen.setPanelColor(szTechRecord, 165, 30, 185) #purpur
                elif iEra == 2: 
                    screen.setPanelColor(szTechRecord, 100, 104, 160) #blau
                elif iEra == 1: 
                    screen.setPanelColor(szTechRecord, 255, 170, 0) #orange
                else: 
                    screen.setPanelColor(szTechRecord, 140, 140, 140) #grau
                self.aiCurrentState.append(CIV_NO_RESEARCH)
            else:
                screen.setPanelColor(szTechRecord, 206, 65, 69)
                self.aiCurrentState.append(CIV_TECH_AVAILABLE)

            if bTechName:
                szTechID = sPanelWidget + "TechID" + str(i)
                szTechString = "<font=1>"
                if gc.getPlayer(self.iCivSelected).isResearchingTech(i):
                    szTechString = szTechString + str(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "
                szTechString += gc.getTechInfo(i).getDescription()
                szTechString = szTechString + "</font>"
                # PAE
                screen.setTextAt(szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + TECH_BUTTON_SIZE, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1)
                # BUG
                # screen.setTextAt( szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + X_INCREMENT, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )

                screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

            if bTechIcon:
                szTechButtonID = sPanelWidget + "TechButtonID" + str(i)
                # PAE
                screen.addDDSGFCAt(szTechButtonID, szTechRecord, gc.getTechInfo(i).getButton(), iX + 6, iY + 8, TECH_BUTTON_SIZE, TECH_BUTTON_SIZE, WidgetTypes.WIDGET_TECH_TREE, i, -1, False)
                # BUG
                # screen.addDDSGFCAt(szTechButtonID, szTechRecord, gc.getTechInfo(i).getButton(), iX + 6, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_TECH_TREE, i, -1, False)

            if bTechDetails:
                self.addIconsToTechPanel(screen, i, X_START, iX, iY, szTechRecord)

            if bTechPanel:
                if BugOpt.isShowTechEra():
                    screen.show(szTechRecordShadow)
                else:
                    screen.hide(szTechRecordShadow)
                screen.show(szTechRecord)
            else:
                screen.hide(szTechRecordShadow)
                screen.hide(szTechRecord)

        screen.setViewMin(sPanel, iMaxX + 20, iMaxY + 20)

        return

    def addIconsToTechPanel(self, screen, i, fX, iX, iY, szTechRecord):
#       BugUtil.debug("cvTechChooser: addIconsToTechPanel")

        j = 0
        k = 0
        # PAE - rank units, not buildable
        LDontShowTheseUnits = [
          gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"),
          gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"),
          gc.getInfoTypeForString("UNIT_HOPLIT_2"),
          gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"),
          gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS"),
          gc.getInfoTypeForString("UNIT_SPARTA_3"),
          gc.getInfoTypeForString("UNIT_HYPASPIST2"),
          gc.getInfoTypeForString("UNIT_HYPASPIST3"),
          gc.getInfoTypeForString("UNIT_PEZHETAIROI2"),
          gc.getInfoTypeForString("UNIT_PEZHETAIROI3"),
          gc.getInfoTypeForString("UNIT_PEZHETAIROI4"),
          gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"),
          gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"),
          gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2")
        ]
    
        # Unlockable units...
        for j in range(gc.getNumUnitClassInfos()):
            eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(j)
            if eLoopUnit != -1 and eLoopUnit not in LDontShowTheseUnits:
                if gc.getUnitInfo(eLoopUnit).getPrereqAndTech() == i:
                    szUnitButton = self.getNextWidgetName("Unit")
                    screen.addDDSGFCAt( szUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, True )
                    fX += X_INCREMENT

        # Unlockable Buildings...
        for j in range(gc.getNumBuildingClassInfos()):
            bTechFound = 0
            eLoopBuilding = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationBuildings(j)

            if eLoopBuilding != -1:
                if gc.getBuildingInfo(eLoopBuilding).getPrereqAndTech() == i:
                    if eLoopBuilding == gc.getInfoTypeForString("BUILDING_AQUEDUCT"):
                        if gc.getGame().getActiveCivilizationType() in L.LCivsWithAqueduct:
                            szBuildingButton = self.getNextWidgetName("Building")
                            screen.addDDSGFCAt( szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True )
                            fX += X_INCREMENT
                    else:
                        szBuildingButton = self.getNextWidgetName("Building")
                        screen.addDDSGFCAt( szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True )
                        fX += X_INCREMENT

        # Obsolete Buildings...
        for j in range(gc.getNumBuildingClassInfos()):
            eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(self.iCivSelected).getCivilizationType()).getCivilizationBuildings(j)

            if eLoopBuilding != -1:
                if gc.getBuildingInfo(eLoopBuilding).getObsoleteTech() == i:
                    # Add obsolete picture here...
                    szObsoleteButton = self.getNextWidgetName("Obsolete")
                    szObsoleteX = self.getNextWidgetName("ObsoleteX")
                    screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
                    screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
                    fX += X_INCREMENT

        # Obsolete Bonuses...
        for j in range(gc.getNumBonusInfos()):
            if gc.getBonusInfo(j).getTechObsolete() == i:
                # Add obsolete picture here...
                szObsoleteButton = self.getNextWidgetName("ObsoleteBonus")
                szObsoleteX = self.getNextWidgetName("ObsoleteXBonus")
                screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
                screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
                fX += X_INCREMENT

        # Obsolete Monastaries...
        for j in range (gc.getNumSpecialBuildingInfos()):
            if gc.getSpecialBuildingInfo(j).getObsoleteTech() == i:
                    # Add obsolete picture here...
                    szObsoleteSpecialButton = self.getNextWidgetName("ObsoleteSpecial")
                    szObsoleteSpecialX = self.getNextWidgetName("ObsoleteSpecialX")
                    screen.addDDSGFCAt( szObsoleteSpecialButton, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
                    screen.addDDSGFCAt( szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
                    fX += X_INCREMENT

        # Route movement change
        for j in range(gc.getNumRouteInfos()):
            if ( gc.getRouteInfo(j).getTechMovementChange(i) != 0 ):
                szMoveButton = self.getNextWidgetName("Move")
                screen.addDDSGFCAt( szMoveButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, i, -1, False )
                fX += X_INCREMENT

        # Promotion Info
        for j in range(gc.getNumPromotionInfos()):
            if gc.getPromotionInfo(j).getTechPrereq() == i:
                szPromotionButton = self.getNextWidgetName("Promotion")
                screen.addDDSGFCAt( szPromotionButton, szTechRecord, gc.getPromotionInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, -1, False )
                fX += X_INCREMENT

        # Free unit
        if gc.getTechInfo(i).getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS:
            szFreeUnitButton = self.getNextWidgetName("FreeUnit")
            eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(gc.getTechInfo(i).getFirstFreeUnitClass())
            if eLoopUnit != -1:
# BUG - 3.19 No Espionage - start
                # CvUnitInfo.getEspionagePoints() was added in 319
                if GameUtil.getVersion() < 319 or gc.getUnitInfo(eLoopUnit).getEspionagePoints() == 0 or not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE):
# BUG - 3.19 No Espionage - end
                    screen.addDDSGFCAt( szFreeUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, eLoopUnit, i, False )
                    fX += X_INCREMENT

        # Feature production modifier
        if gc.getTechInfo(i).getFeatureProductionModifier() != 0:
            szFeatureProductionButton = self.getNextWidgetName("FeatureProduction")
            screen.addDDSGFCAt( szFeatureProductionButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, i, -1, False )
            fX += X_INCREMENT

        # Worker speed
        if gc.getTechInfo(i).getWorkerSpeedModifier() != 0:
            szWorkerModifierButton = self.getNextWidgetName("Worker")
            screen.addDDSGFCAt( szWorkerModifierButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, i, -1, False )
            fX += X_INCREMENT

        # Trade Routes per City change
        if gc.getTechInfo(i).getTradeRoutes() != 0:
            szTradeRouteButton = self.getNextWidgetName("TradeRoutes")
            screen.addDDSGFCAt( szTradeRouteButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, i, -1, False )
            fX += X_INCREMENT

        # Health Rate bonus from this tech...
        if ( gc.getTechInfo(i).getHealth() != 0 ):
            szHealthRateButton = self.getNextWidgetName("HealthRate")
            screen.addDDSGFCAt( szHealthRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, i, -1, False )
            fX += X_INCREMENT

        # Happiness Rate bonus from this tech...
        if gc.getTechInfo(i).getHappiness() != 0:
            szHappinessRateButton = self.getNextWidgetName("HappinessRate")
            screen.addDDSGFCAt( szHappinessRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, i, -1, False )
            fX += X_INCREMENT

        # Free Techs
        if gc.getTechInfo(i).getFirstFreeTechs() > 0:
            szFreeTechButton = self.getNextWidgetName("FreeTech")
            screen.addDDSGFCAt( szFreeTechButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, i, -1, False )
            fX += X_INCREMENT

        # Line of Sight bonus...
        if gc.getTechInfo(i).isExtraWaterSeeFrom():
            szLOSButton = self.getNextWidgetName("LOS")
            screen.addDDSGFCAt( szLOSButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, i, -1, False )
            fX += X_INCREMENT

        # Map Center Bonus...
        if gc.getTechInfo(i).isMapCentering():
            szMapCenterButton = self.getNextWidgetName("MapCenter")
            screen.addDDSGFCAt( szMapCenterButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, i, -1, False )
            fX += X_INCREMENT

        # Map Reveal...
        if gc.getTechInfo(i).isMapVisible():
            szMapRevealButton = self.getNextWidgetName("MapReveal")
            screen.addDDSGFCAt( szMapRevealButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, i, -1, False )
            fX += X_INCREMENT

        # Map Trading
        if gc.getTechInfo(i).isMapTrading():
            szMapTradeButton = self.getNextWidgetName("MapTrade")
            screen.addDDSGFCAt( szMapTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, i, -1, False )
            fX += X_INCREMENT

        # Tech Trading
        if gc.getTechInfo(i).isTechTrading():
            szTechTradeButton = self.getNextWidgetName("TechTrade")
            screen.addDDSGFCAt( szTechTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, i, -1, False )
            fX += X_INCREMENT

        # Gold Trading
        if gc.getTechInfo(i).isGoldTrading():
            szGoldTradeButton = self.getNextWidgetName("GoldTrade")
            screen.addDDSGFCAt( szGoldTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, i, -1, False )
            fX += X_INCREMENT

        # Open Borders
        if gc.getTechInfo(i).isOpenBordersTrading():
            szOpenBordersButton = self.getNextWidgetName("OpenBorders")
            screen.addDDSGFCAt( szOpenBordersButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, i, -1, False )
            fX += X_INCREMENT

        # Defensive Pact
        if ( gc.getTechInfo(i).isDefensivePactTrading() ):
            szDefensivePactButton = self.getNextWidgetName("DefensivePact")
            screen.addDDSGFCAt( szDefensivePactButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, i, -1, False )
            fX += X_INCREMENT

        # Permanent Alliance
        if ( gc.getTechInfo(i).isPermanentAllianceTrading() ):
            szPermanentAllianceButton = self.getNextWidgetName("PermanentAlliance")
            screen.addDDSGFCAt( szPermanentAllianceButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, i, -1, False )
            fX += X_INCREMENT

        # Vassal States
        if ( gc.getTechInfo(i).isVassalStateTrading() ):
            szVassalStateButton = self.getNextWidgetName("VassalState")
            screen.addDDSGFCAt( szVassalStateButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, i, -1, False )
            fX += X_INCREMENT

        # Bridge Building
        if ( gc.getTechInfo(i).isBridgeBuilding() ):
            szBuildBridgeButton = self.getNextWidgetName("BuildBridge")
            screen.addDDSGFCAt( szBuildBridgeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, i, -1, False )
            fX += X_INCREMENT

        # Irrigation unlocked...
        if ( gc.getTechInfo(i).isIrrigation() ):
            szIrrigationButton = self.getNextWidgetName("Irrigation")
            screen.addDDSGFCAt( szIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, i, -1, False )
            fX += X_INCREMENT

        # Ignore Irrigation unlocked...
        if ( gc.getTechInfo(i).isIgnoreIrrigation() ):
            szIgnoreIrrigationButton = self.getNextWidgetName("IgnoreIrrigation")
            screen.addDDSGFCAt( szIgnoreIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, i, -1, False )
            fX += X_INCREMENT

        # Coastal Work unlocked...
        if ( gc.getTechInfo(i).isWaterWork() ):
            szWaterWorkButton = self.getNextWidgetName("WaterWork")
            screen.addDDSGFCAt( szWaterWorkButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, i, -1, False )
            fX += X_INCREMENT

        # Improvements
        # Limes
        lBuildInfos = []
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES1"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES3"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES4"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES5"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES6"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES7"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES8"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES9"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_1"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_2"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_3"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_4"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_5"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_6"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_7"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_8"))
        lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_9"))
            
        for j in range(gc.getNumBuildInfos()):
            if j in lBuildInfos:
                continue
            bTechFound = False

            if gc.getBuildInfo(j).getTechPrereq() == -1:
                bTechFound = False
                for k in range(gc.getNumFeatureInfos()):
                    if gc.getBuildInfo(j).getFeatureTech(k) == i:
                        bTechFound = True
            elif gc.getBuildInfo(j).getTechPrereq() == i:
                bTechFound = True

            if bTechFound:
                szImprovementButton = self.getNextWidgetName("Improvement")
                screen.addDDSGFCAt( szImprovementButton, szTechRecord, gc.getBuildInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, j, False )
                fX += X_INCREMENT

        # Domain Extra Moves
        for j in range( DomainTypes.NUM_DOMAIN_TYPES ):
            if (gc.getTechInfo(i).getDomainExtraMoves(j) != 0):
                szDomainExtraMovesButton = self.getNextWidgetName("DomainExtraMoves")
                screen.addDDSGFCAt( szDomainExtraMovesButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, i, j, False )
                fX += X_INCREMENT

        # K-Mod. Commerce modifiers
        for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
            if (gc.getTechInfo(i).getCommerceModifier(j) > 0):
                szCommerceModifierButton = self.getNextWidgetName("CommerceModifierButton")
                screen.addDDSGFCAt( szCommerceModifierButton, szTechRecord, gc.getCommerceInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GLOBAL_COMMERCE_MODIFIER, i, j, False )
                fX += X_INCREMENT

        # K-Mod. Extra specialist commerce
        for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
            if (gc.getTechInfo(i).getSpecialistExtraCommerce(j) > 0):
                if (gc.getDefineINT("DEFAULT_SPECIALIST") != SpecialistTypes.NO_SPECIALIST):
                    szSpecialistCommerceButtonButton = self.getNextWidgetName("SpecialistCommerceButton")
                    screen.addDDSGFCAt( szSpecialistCommerceButtonButton, szTechRecord, gc.getSpecialistInfo(gc.getDefineINT("DEFAULT_SPECIALIST")).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_EXTRA_SPECIALIST_COMMERCE, i, j, False )
                    fX += X_INCREMENT
                break

        # K-Mod end.

        # Adjustments
        for j in range( CommerceTypes.NUM_COMMERCE_TYPES ):
            if (gc.getTechInfo(i).isCommerceFlexible(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isCommerceFlexible(j))):
                szAdjustButton = self.getNextWidgetName("AdjustButton")
                if ( j == CommerceTypes.COMMERCE_CULTURE ):
                    szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_CULTURE").getPath()
                elif ( j == CommerceTypes.COMMERCE_ESPIONAGE ):
                    szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
                else:
                    szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
                screen.addDDSGFCAt( szAdjustButton, szTechRecord, szFileName, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, i, j, False )
                fX += X_INCREMENT

        # Terrain opens up as a trade route
        for j in range( gc.getNumTerrainInfos() ):
            if (gc.getTechInfo(i).isTerrainTrade(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isTerrainTrade(j))):
                szTerrainTradeButton = self.getNextWidgetName("TerrainTradeButton")
                screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
                fX += X_INCREMENT

        j = gc.getNumTerrainInfos()
        if (gc.getTechInfo(i).isRiverTrade() and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isRiverTrade())):
            szTerrainTradeButton = self.getNextWidgetName("TerrainTradeButton")
            screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
            fX += X_INCREMENT

        # Special buildings like monestaries...
        for j in range( gc.getNumSpecialBuildingInfos() ):
            if (gc.getSpecialBuildingInfo(j).getTechPrereq() == i):
                szSpecialBuilding = self.getNextWidgetName("SpecialBuildingButton")
                screen.addDDSGFCAt( szSpecialBuilding, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, i, j, False )
                fX += X_INCREMENT

        # Yield change
        for j in range( gc.getNumImprovementInfos() ):
            bFound = False
            for k in range( YieldTypes.NUM_YIELD_TYPES ):
                if (gc.getImprovementInfo(j).getTechYieldChanges(i, k)):
                    if not bFound:
                        szYieldChange = self.getNextWidgetName("YieldChangeButton")
                        screen.addDDSGFCAt( szYieldChange, szTechRecord, gc.getImprovementInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, j, False )
                        fX += X_INCREMENT
                        bFound = True

        # Bonuses revealed
        for j in range( gc.getNumBonusInfos() ):
            if (gc.getBonusInfo(j).getTechReveal() == i):
                szBonusReveal = self.getNextWidgetName("BonusRevealButton")
                screen.addDDSGFCAt( szBonusReveal, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, i, j, False )
                fX += X_INCREMENT

        # Civic options
        for j in range( gc.getNumCivicInfos() ):
            if (gc.getCivicInfo(j).getTechPrereq() == i):
                szCivicReveal = self.getNextWidgetName("CivicRevealButton")
                screen.addDDSGFCAt( szCivicReveal, szTechRecord, gc.getCivicInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, j, False )
                fX += X_INCREMENT

        # Projects possible
        for j in range( gc.getNumProjectInfos() ):
            if (gc.getProjectInfo(j).getTechPrereq() == i):
                szProjectInfo = self.getNextWidgetName("ProjectInfoButton")
                screen.addDDSGFCAt( szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
                fX += X_INCREMENT

        # Processes possible
        for j in range( gc.getNumProcessInfos() ):
            if (gc.getProcessInfo(j).getTechPrereq() == i):
                szProcessInfo = self.getNextWidgetName("ProcessInfoButton")
                screen.addDDSGFCAt( szProcessInfo, szTechRecord, gc.getProcessInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, i, j, False )
                fX += X_INCREMENT

        # Religions unlocked
        for j in range(gc.getNumReligionInfos()):
            if gc.getReligionInfo(j).getTechPrereq() == i:
                szFoundReligion = self.getNextWidgetName("FoundReligionButton")
                if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
                    szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
                else:
                    szButton = gc.getReligionInfo(j).getButton()
                screen.addDDSGFCAt( szFoundReligion, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, i, j, False )
                fX += X_INCREMENT

        # PAE: Kulte/Cults
        for j in range(gc.getNumCorporationInfos()):
            if gc.getCorporationInfo(j).getTechPrereq() == i:
                szFoundCorporation = self.getNextWidgetName("FoundCorporationButton")
                screen.addDDSGFCAt( szFoundCorporation, szTechRecord, gc.getCorporationInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, i, j, False )
                fX += X_INCREMENT

        ### Techs - PAE Special features made possible via python (eg. free units, unit formations, obsolete units, reservists)
        if i == gc.getInfoTypeForString("TECH_RELIGION_NORDIC"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_nordic.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_CELTIC"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_celtic.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_SUMER"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_sumer.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_EGYPT"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_egypt.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_PHOEN"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_phoen.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_GREEK"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_greek.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_HINDU"):
            screen.addDDSGFCAt( "", szTechRecord, ",Art/Interface/Buttons/Units/Missionary_Hindu.dds,Art/Interface/Buttons/Unit_Resource_Atlas.dds,4,3", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_RELIGION_ROME"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_rome.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_DUALISMUS"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_zoro.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 698, 698, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_FRUCHTBARKEIT"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Corporations/button_unit_corp2.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 676, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_SENSE"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Corporations/button_unit_corp3.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 676, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_GLADIATOR"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Corporations/button_unit_corp5.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 676, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_BUCHSTABEN"):
            screen.addDDSGFCAt( "", szTechRecord, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEGESSTELE")).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 2, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_CONSTRUCTION"):
            screen.addDDSGFCAt( "", szTechRecord, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL")).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 3, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_KRIEGERETHOS"):
            screen.addDDSGFCAt( "", szTechRecord, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL")).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 4, False )
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 4, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_GER_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 5, False )
            fX += X_INCREMENT
        ### Unit Formations und Rang/Rank
        elif i == gc.getInfoTypeForString("TECH_BEWAFFNUNG3"):
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 6, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_BUERGERSOLDATEN"):
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_SUMER_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 7, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 8, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_BRANDSCHATZEN"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FOURAGE")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_ARMOR"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_SCHILDWALL")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_CLOSED_FORM"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_CLOSED_FORM")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_PHALANX"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PHALANX")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 9, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_PHALANX2"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_SCHIEF")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PHALANX2")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 10, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_SKIRMISH_TACTICS"):
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 11, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_BANKWESEN"):
            # Comission elite mercenaries
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARIES_CITYBUTTON").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 15, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_MANIPEL"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_MANIPEL")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_TREFFEN"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_TREFFEN")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_KETTENPANZER"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KEIL")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_MILIT_STRAT"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_ZANGENANGRIFF")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_LINOTHORAX"):
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_GREEK_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 12, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 13, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_MARIAN_REFORM"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KOHORTE")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ROM_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 14, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 15, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_STAUROGRAMM"):
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 16, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_TESTUDO"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_TESTUDO")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_PARTHERSCHUSS"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PARTHER")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_KANTAKREIS"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_GEOMETRIE2"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_GASSE")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_LOGIK"):
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_KEIL")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_ZANGE")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False )
            fX += X_INCREMENT
        # Actions und Rang/Rank
        elif i == gc.getInfoTypeForString("TECH_HORSEBACK_RIDING"):
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_HUN")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 17, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_HORSEBACK_RIDING_2"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HORSE_DOWN").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 666, 666, False )
            fX += X_INCREMENT
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HORSE_UP").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 667, 667, False )
            fX += X_INCREMENT
            iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_1")
            screen.addDDSGFCAt( "", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 18, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_SYNKRETISMUS"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2BORDELL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 668, 668, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_GLADIATOR"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GLADIATOR").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 669, 669, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_DRAMA"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2THEATRE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 670, 670, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_KUNST"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2SCHOOL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 679, 679, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_MANUFAKTUREN"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2MANUFAKTUR_FOOD").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 680, 680, False )
            fX += X_INCREMENT
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2MANUFAKTUR_PROD").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 681, 681, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_ENSLAVEMENT"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_PALACE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 692, 692, False )
            fX += X_INCREMENT
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_TEMPLE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 693, 693, False )
            fX += X_INCREMENT
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SELL_SLAVES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 694, 694, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_SOELDNERTUM"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SELL_UNITS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 695, 100, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_FEUERWEHR"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_FEUERWEHR").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 696, 696, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_ARMOR"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EDLE_RUESTUNG").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 699, -1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_KUESTE"):
            screen.addDDSGFCAt( "", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_PROMO_OIL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 701, -1, False )
            fX += X_INCREMENT
        # Reservisten
        elif i == gc.getInfoTypeForString("TECH_RESERVISTEN"):
            screen.addDDSGFCAt( "", szTechRecord, ",Art/Interface/MainScreen/CityScreen/Great_Engineer.dds,Art/Interface/Buttons/Warlords_Atlas_2.dds,7,6", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 724, -1, False )
            fX += X_INCREMENT
            #if gc.getGame().getActiveCivilizationType() in L.LGreeks or gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
            #    j = gc.getInfoTypeForString("UNIT_KLERUCHOI")
            #    screen.addDDSGFCAt( "", szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, -1, False )
            #    fX += X_INCREMENT
        #elif i == gc.getInfoTypeForString("TECH_BEWAFFNUNG5"):
        #    if gc.getGame().getActiveCivilizationType() in L.LNorthern or gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_IBERER"):
        #        j = gc.getInfoTypeForString("UNIT_SOLDURII")
        #        screen.addDDSGFCAt( "", szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, -1, False )
        #        fX += X_INCREMENT
        #elif i == gc.getInfoTypeForString("TECH_BERUFSSOLDATEN"):
        #    if gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ROME") or gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
        #        j = gc.getInfoTypeForString("UNIT_LEGION_EVOCAT")
        #        screen.addDDSGFCAt( "", szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, -1, False )
        #        fX += X_INCREMENT

        # Sterberate von Sklaven
        elif i == gc.getInfoTypeForString("TECH_PATRONAT"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 16, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_MECHANIK"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 17, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_EISENPFLUG"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 18, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_MEDICINE3") or i == gc.getInfoTypeForString("TECH_ANATOMIE"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 19, False )
            fX += X_INCREMENT

        # Limes
        elif i == gc.getInfoTypeForString("TECH_LIMES"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Buildings/button_building_limes.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 733, 0, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_DEFENCES_2"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Buildings/button_building_hadrianswall.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 733, 1, False )
            fX += X_INCREMENT
        # Salae/Sold oder Dezimierung
        elif i == gc.getInfoTypeForString("TECH_CURRENCY"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Actions/button_action_salae.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 735, 1, False )
            fX += X_INCREMENT
        elif i == gc.getInfoTypeForString("TECH_DEZIMATION"):
            screen.addDDSGFCAt( "", szTechRecord, "Art/Interface/Buttons/Actions/button_action_dezimierung.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 735, 2, False )
            fX += X_INCREMENT
        # Obsolete units (Praetorianer)
        elif i == gc.getInfoTypeForString("TECH_GRENZHEER"):
            j = gc.getInfoTypeForString("UNIT_PRAETORIAN")
            szObsoleteSpecialButton = "ObsoleteUnit" + str(j)
            szObsoleteSpecialX = "ObsoleteUnitX" + str(j)
            screen.addDDSGFCAt( szObsoleteSpecialButton, szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, True )
            screen.addDDSGFCAt( szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, True )
            fX += X_INCREMENT
        # Obsolet Olympic Games
        elif i == gc.getInfoTypeForString("TECH_PAPSTTUM"):
            j = gc.getInfoTypeForString("PROJECT_OLYMPIC_GAMES")
            szObsoleteButton = "ObsoleteProject" + str(j)
            szObsoleteX = "ObsoleteProjectX" + str(j)
            screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getProjectInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, False )
            screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, False )
            fX += X_INCREMENT
        ### End -----------

        # PAE: Espionage Missions
        for j in range( gc.getNumEspionageMissionInfos() ):
            if ( gc.getEspionageMissionInfo(j).getTechPrereq() == i ):
                szFoundEspionage = "FoundEspionageButton" + str( ( i * 1000 ) + j )
                szButton = ArtFileMgr.getInterfaceArtInfo("ESPIONAGE_BUTTON2").getPath()
                screen.addDDSGFCAt( szFoundEspionage, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 723, j, False )
                fX += X_INCREMENT
        j = 0

        # ------------------------

        #screen.show( szTechRecord )

        #screen.setViewMin( "TechList", iMaxX + 20, iMaxY + 20 )
        #screen.show( "TechList" )
        #screen.setFocus( "TechList" )


    # Will update the tech records based on color, researching, researched, queued, etc.
    def updateTechRecords (self, bForce):
#       BugUtil.debug("cvTechChooser: updateTechRecords")

        # If we are the Pitboss, we don't want to put up an interface at all
        if ( CyGame().isPitbossHost() ):
            return

        if (self.sTechTabID == self.sTechSelectTab):
            bTechName = True
            sPanel = self.TabPanels[0]
            self.BOX_INCREMENT_WIDTH = 30 # Used to be 33 #Should be a multiple of 3...
        else:
            bTechName = False
            sPanel = self.TabPanels[1]
            self.BOX_INCREMENT_WIDTH = 12 # Used to be 33 #Should be a multiple of 3...

        # Get the screen
        screen = self.getScreen()

        abChanged = []
        bAnyChanged = 0

        # Go through all the techs
        for i in range(gc.getNumTechInfos()):

            abChanged.append(0)

            if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
                if ( self.aiCurrentState[i] != CIV_HAS_TECH ):
                    self.aiCurrentState[i] = CIV_HAS_TECH
                    abChanged[i] = 1
                    bAnyChanged = 1
            elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
                if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
                    self.aiCurrentState[i] = CIV_IS_RESEARCHING
                    abChanged[i] = 1
                    bAnyChanged = 1
            elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
                if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
                    self.aiCurrentState[i] = CIV_IS_RESEARCHING
                    abChanged[i] = 1
                    bAnyChanged = 1
            elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
                if ( self.aiCurrentState[i] != CIV_NO_RESEARCH ):
                    self.aiCurrentState[i] = CIV_NO_RESEARCH
                    abChanged[i] = 1
                    bAnyChanged = 1
            else:
                if ( self.aiCurrentState[i] != CIV_TECH_AVAILABLE ):
                    self.aiCurrentState[i] = CIV_TECH_AVAILABLE
                    abChanged[i] = 1
                    bAnyChanged = 1

        for i in range(gc.getNumTechInfos()):
            if (abChanged[i] or bForce or (bAnyChanged and gc.getPlayer(self.iCivSelected).isResearchingTech(i))):
                # Create and place a tech in its proper location
                szTechRecord = "TechRecord" + str(i)
                szTechID = "TechID" + str(i)
                szTechString = "<font=1>"

                if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
                    szTechString = szTechString + unicode(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "

                iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
                iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + 5

                if bTechName:
                    szTechString += gc.getTechInfo(i).getDescription()
                    if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
                        szTechString += " ("
                        szTechString += str(gc.getPlayer(self.iCivSelected).getResearchTurnsLeft(i, ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i )))
                        szTechString += ")"
                    szTechString = szTechString + "</font>"
                    # PAE
                    screen.setTextAt( szTechID, sPanel, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + TECH_BUTTON_SIZE, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
                    screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

                if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
                    screen.setPanelColor(szTechRecord, 85, 150, 87)
                elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
                    screen.setPanelColor(szTechRecord, 104, 158, 165)
                elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
                    screen.setPanelColor(szTechRecord, 104, 158, 165)
                elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
                    # TODO use setTechPanelShadowColor(self, screen, sPanel, iEra)
                    iEra = gc.getTechInfo(i).getEra()
                    if iEra == 4: 
                        screen.setPanelColor(szTechRecord, 130, 70, 0) #braun
                    elif iEra == 3: 
                        screen.setPanelColor(szTechRecord, 165, 30, 185) #purpur
                    elif iEra == 2: 
                        screen.setPanelColor(szTechRecord, 100, 104, 160) #blau
                    elif iEra == 1: 
                        screen.setPanelColor(szTechRecord, 255, 170, 0) #orange
                    else: 
                        screen.setPanelColor(szTechRecord, 140, 140, 140) #grau
                else:
                    screen.setPanelColor(szTechRecord, 206, 65, 69)

# BUG - GP Tech Prefs - start
        self.updateTechPrefs()
# BUG - GP Tech Prefs - end

# BUG - Tech Era Colors - start
    def setTechPanelShadowColor(self, screen, sPanel, iEra):
        szEra = gc.getEraInfo(iEra).getType()
        iColor = ClockOpt.getEraColor(szEra)
        if iColor != -1:
            color = gc.getColorInfo(iColor)
            if color:
                rgb = color.getColor() # NiColorA object
                if rgb:
                    screen.setPanelColor(sPanel, int(100 * rgb.r), int(100 * rgb.g), int(100 * rgb.b))
# BUG - Tech Era Colors - end

    # Will draw the arrows
    def drawArrows(self, screen, sPanel, bANDPreReq, bORPreReq):
#       BugUtil.debug("cvTechChooser: drawArrows")

        iLoop = 0

        ARROW_X = ArtFileMgr.getInterfaceArtInfo("ARROW_X").getPath()
        ARROW_Y = ArtFileMgr.getInterfaceArtInfo("ARROW_Y").getPath()
        ARROW_MXMY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXMY").getPath()
        ARROW_XY = ArtFileMgr.getInterfaceArtInfo("ARROW_XY").getPath()
        ARROW_MXY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXY").getPath()
        ARROW_XMY = ArtFileMgr.getInterfaceArtInfo("ARROW_XMY").getPath()
        ARROW_HEAD = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD").getPath()

        for i in range(gc.getNumTechInfos()):
            bFirst = 1
            fX = (self.BOX_INCREMENT_WIDTH * self.PIXEL_INCREMENT) - 10  # - 8

            if bANDPreReq:
                for j in range(gc.getNUM_AND_TECH_PREREQS()):
                    eTech = gc.getTechInfo(i).getPrereqAndTechs(j)
                    if eTech > -1:
                        fX = fX - X_INCREMENT
                        iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
                        iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + 5

                        szTechPrereqID = "TechPrereqID" + str((i * 1000) + j)
                        screen.addDDSGFCAt( szTechPrereqID, sPanel, gc.getTechInfo(eTech).getButton(), iX + fX, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

                        #szTechPrereqBorderID = "TechPrereqBorderID" + str((i * 1000) + j)
                        #screen.addDDSGFCAt( szTechPrereqBorderID, sPanel, ArtFileMgr.getInterfaceArtInfo("TECH_TREE_BUTTON_BORDER").getPath(), iX + fX + 4, iY + 22, 32, 32, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

            if bORPreReq:
                for j in range(gc.getNUM_OR_TECH_PREREQS()):
                    eTech = gc.getTechInfo(i).getPrereqOrTechs(j)
                    if eTech > -1:
                        iX = 24 + ((gc.getTechInfo(eTech).getGridX() - 1) * ((self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH) * self.PIXEL_INCREMENT))
                        iY = (gc.getTechInfo(eTech).getGridY() - 1) * (self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT) + 5

                        # j is the pre-req, i is the tech...
                        xDiff = gc.getTechInfo(i).getGridX() - gc.getTechInfo(eTech).getGridX()
                        yDiff = gc.getTechInfo(i).getGridY() - gc.getTechInfo(eTech).getGridY()

                        if (yDiff == 0):
                            screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(3), self.getWidth(xDiff), 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                            screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                        elif (yDiff < 0):
                            if ( yDiff == -6 ):
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(1), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) + 8 - self.getHeight(yDiff, 0), 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                            elif ( yDiff == -2 and xDiff == 2 ):
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(2), self.getWidth(xDiff) * 5 / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                            else:
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(2), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                        elif (yDiff > 0):
                            if ( yDiff == 2 and xDiff == 2):
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(4), self.getWidth(xDiff) / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) * 5 / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                            elif ( yDiff == 4 and xDiff == 1):
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(5), self.getWidth(xDiff) / 3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), ( self.getWidth(xDiff) * 2 / 3 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                            else:
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(4), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
                                screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

        return

# BUG - GP Tech Prefs - start
    def resetTechPrefs (self):
        self.pPrefs = TechPrefs.TechPrefs()

    def updateTechPrefs (self):
#       BugUtil.debug("cvTechChooser: updateTechPrefs")

        # If we are the Pitboss, we don't want to put up an interface at all
        if ( CyGame().isPitbossHost() ):
            return

        # These don't seem to be setup when screen is first opened
        if (gc.getNumTechInfos() <= 0 or gc.getNumFlavorTypes() <= 0):
            return

        # Get the screen and player
        screen = self.getScreen()
        pPlayer = gc.getPlayer(self.iCivSelected)

        # Don't show tech prefs during advanced start setup
        if (pPlayer.getAdvancedStartPoints() >= 0):
            return

        # Check to see if option is disabled
        if (not BugOpt.isShowGPTechPrefs()):
            if (self.bPrefsShowing):
                # ... and if so, remove icons if they are currently showing
                screen.hide( "GreatPersonHeading")
                for i, f in enumerate(FLAVORS):
                    screen.hide( "GreatPerson" + str(f) )
                    screen.hide( "GreatPersonTech" + str(f) )
                    screen.hide( "GreatPersonTechNext" + str(f) )
                self.bPrefsShowing = False
            return
        # Always redraw the GP icons because otherwise they are prone to disappearing
        # discover icon heading
        iIconSize = 48
        iX = PREF_ICON_LEFT + 5 * PREF_ICON_SIZE / 4 - iIconSize / 2
        iY = PREF_ICON_TOP - iIconSize - 40
        screen.addDDSGFC( "GreatPersonHeading", ArtFileMgr.getInterfaceArtInfo("DISCOVER_TECHNOLOGY_BUTTON").getPath(), iX, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        for i, f in enumerate(FLAVORS):
            # GP icon
            iUnitClass = gc.getInfoTypeForString(UNIT_CLASSES[i])
            iUnitType = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
            pUnitInfo = gc.getUnitInfo(iUnitType)
            iX = PREF_ICON_LEFT
            iY = PREF_ICON_TOP + 4 * i * PREF_ICON_SIZE
            screen.addDDSGFC( "GreatPerson" + str(f), pUnitInfo.getButton(), iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_ALL, f, -1 )
        self.bPrefsShowing = True

        # Remove any techs researched since last call, creating tree if necessary
        if (not self.pPrefs):
            self.resetTechPrefs()
        self.pPrefs.removeKnownTechs()

        # Add all techs in research queue to set of soon-to-be-known techs
        sTechs = set()
        for i in range(gc.getNumTechInfos()):
            if (pPlayer.isResearchingTech(i)):
                sTechs.add(self.pPrefs.getTech(i))

        # Update the buttons to reflect the new tech prefs
        for i, f in enumerate(FLAVORS):
            # GP button
            screen.show( "GreatPerson" + str(f) )

            # Current tech GP will pop
            szButtonName = "GreatPersonTech" + str(f)
            pTech = self.pPrefs.getNextResearchableFlavorTech(f)
            iX = PREF_ICON_LEFT + 3 * PREF_ICON_SIZE / 2
            iY = PREF_ICON_TOP + 4 * i * PREF_ICON_SIZE
            if (pTech):
                screen.addDDSGFC( szButtonName, pTech.getInfo().getButton(), iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_CURRENT, f, -1 )
            else:
                screen.addDDSGFC( szButtonName, self.NO_TECH_ART, iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_CURRENT, f, -1 )
            screen.show( szButtonName )

            # Tech GP will pop once selected techs are researched
            szButtonName = "GreatPersonTechNext" + str(f)
            pTech = self.pPrefs.getNextResearchableWithFlavorTech(f, sTechs)
            iX = PREF_ICON_LEFT + 3 * PREF_ICON_SIZE / 2
            iY = PREF_ICON_TOP + 4 * i * PREF_ICON_SIZE + 3 * PREF_ICON_SIZE / 2
            if (pTech):
                screen.addDDSGFC( szButtonName, pTech.getInfo().getButton(), iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_FUTURE, f, -1 )
            else:
                screen.addDDSGFC( szButtonName, self.NO_TECH_ART, iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_FUTURE, f, -1 )
            screen.show( szButtonName )
# BUG - GP Tech Prefs - end

    def TechRecord (self, inputClass):
        return 0

    # Clicked the parent?
    def ParentClick (self, inputClass):
        return 0

    def CivDropDown( self, inputClass ):
        if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
            screen = self.getScreen()
            iIndex = screen.getSelectedPullDownID("CivDropDown")
            self.iCivSelected = screen.getPullDownData("CivDropDown", iIndex)
            self.updateTechRecords(false)

    # Will handle the input for this screen...
    def handleInput (self, inputClass):
#       BugUtil.debug("cvTechChooser: handleInput")
#       BugUtil.debugInput(inputClass)

        # Get the screen
        screen = self.getScreen()

        szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())

        # Advanced Start Stuff
        pPlayer = gc.getPlayer(self.iCivSelected)
        if (pPlayer.getAdvancedStartPoints() >= 0):
#           BugUtil.debug("cvTechChooser: handleInput - advancedstart")
            # Add tech button
            if inputClass.getFunctionName() == "AddTechButton":
                if pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1:
                    CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_TECH, self.iCivSelected, -1, -1, self.m_iSelectedTech, true)    #Action, Player, X, Y, Data, bAdd
                    self.m_bTechRecordsDirty = true
                    self.m_bSelectedTechDirty = true

            # Tech clicked on
            elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
                if inputClass.getButtonType() == WidgetTypes.WIDGET_TECH_TREE:
                    self.m_iSelectedTech = inputClass.getData1()
                    self.updateSelectedTech()

        ' Calls function mapped in TechChooserInputMap'
        # only get from the map if it has the key
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
#           BugUtil.debug("cvTechChooser: handleInput - dropdown")
            self.CivDropDown( inputClass )
            return 1

        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            if szWidgetName == self.sTechSelectTab:
                self.sTechTabID = self.sTechSelectTab
                self.ShowTab()

            elif szWidgetName == self.sTechTradeTab:
                self.sTechTabID = self.sTechTradeTab
                self.ShowTab()

        return 0

    def getNextWidgetName(self, sName):
#       BugUtil.debug("cvTechChooser: getNextWidgetName %i %i", self.nWidgetCount, len(self.sWidgets))
        szName = sName + str(self.nWidgetCount)
        self.nWidgetCount += 1
        self.sWidgets.append(szName)
        return szName

    def deleteWidgets(self):
#       BugUtil.debug("cvTechChooser: deleteWidgets %i %i", self.nWidgetCount, len(self.sWidgets))
        screen = self.getScreen()
        for w in self.sWidgets:
#           BugUtil.debug("cvTechChooser: deleteWidgets '%s'", w)
            screen.deleteWidget(w)

        self.nWidgetCount = 0
        self.sWidgets = []
        return

    def getXStart(self):
        return self.BOX_INCREMENT_WIDTH * self.PIXEL_INCREMENT

    def getXSpacing(self):
        return self.BOX_INCREMENT_X_SPACING * self.PIXEL_INCREMENT

    def getYStart(self, iY):
        return int((((self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ) / 6.0) * iY) - self.PIXEL_INCREMENT )

    def getWidth(self, xDiff):
        return ( xDiff * self.getXSpacing() ) + ( ( xDiff - 1 ) * self.getXStart() )

    def getHeight(self, yDiff, nFactor):
        return ( nFactor + ( ( abs( yDiff ) - 1 ) * 6 ) ) * self.PIXEL_INCREMENT

    def update(self, fDelta):
        if (CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT)):
            CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, false)

            if (self.m_bSelectedTechDirty):
                self.m_bSelectedTechDirty = false
                self.updateSelectedTech()

            if (self.m_bTechRecordsDirty):
                self.m_bTechRecordsDirty = false
                self.updateTechRecords(true)

            if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() < 0):
                # hide the screen
                screen = self.getScreen()
                screen.hide("AddTechButton")
                screen.hide("ASPointsLabel")
                screen.hide("SelectedTechLabel")

        return

    def updateSelectedTech(self):
        pPlayer = gc.getPlayer(CyGame().getActivePlayer())

        # Get the screen
        screen = self.getScreen()

        szName = ""
        iCost = 0

        if (self.m_iSelectedTech != -1):
            szName = gc.getTechInfo(self.m_iSelectedTech).getDescription()
            iCost = gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartTechCost(self.m_iSelectedTech, true)

        if iCost > 0:
            szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_SELECTED_TECH_COST", (iCost, pPlayer.getAdvancedStartPoints())) + u"</font>"
            screen.setLabel( "ASPointsLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        else:
            screen.hide("ASPointsLabel")

        szText = u"<font=4>"
        szText += localText.getText("TXT_KEY_WB_AS_SELECTED_TECH", (szName,))
        szText += u"</font>"
        screen.setLabel( "SelectedTechLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT + 250, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        # Want to add
        if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1):
            screen.show("AddTechButton")
        else:
            screen.hide("AddTechButton")

    def onClose(self):
        pPlayer = gc.getPlayer(self.iCivSelected)
        if (pPlayer.getAdvancedStartPoints() >= 0):
            CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, true)
        return 0

class TechChooserMaps:

    TechChooserInputMap = {
        'TechRecord'            : CvTechChooser().TechRecord,
        'TechID'                : CvTechChooser().ParentClick,
        'TechPane'              : CvTechChooser().ParentClick,
        'TechButtonID'          : CvTechChooser().ParentClick,
        'TechButtonBorder'      : CvTechChooser().ParentClick,
        'Unit'                  : CvTechChooser().ParentClick,
        'Building'              : CvTechChooser().ParentClick,
        'Obsolete'              : CvTechChooser().ParentClick,
        'ObsoleteX'             : CvTechChooser().ParentClick,
        'Move'                  : CvTechChooser().ParentClick,
        'FreeUnit'              : CvTechChooser().ParentClick,
        'FeatureProduction'         : CvTechChooser().ParentClick,
        'Worker'                : CvTechChooser().ParentClick,
        'TradeRoutes'           : CvTechChooser().ParentClick,
        'HealthRate'            : CvTechChooser().ParentClick,
        'HappinessRate'         : CvTechChooser().ParentClick,
        'FreeTech'              : CvTechChooser().ParentClick,
        'LOS'                   : CvTechChooser().ParentClick,
        'MapCenter'             : CvTechChooser().ParentClick,
        'MapReveal'             : CvTechChooser().ParentClick,
        'MapTrade'              : CvTechChooser().ParentClick,
        'TechTrade'             : CvTechChooser().ParentClick,
        'OpenBorders'       : CvTechChooser().ParentClick,
        'BuildBridge'           : CvTechChooser().ParentClick,
        'Irrigation'            : CvTechChooser().ParentClick,
        'Improvement'           : CvTechChooser().ParentClick,
        'DomainExtraMoves'          : CvTechChooser().ParentClick,
        'AdjustButton'          : CvTechChooser().ParentClick,
        'TerrainTradeButton'    : CvTechChooser().ParentClick,
        'SpecialBuildingButton' : CvTechChooser().ParentClick,
        'YieldChangeButton'     : CvTechChooser().ParentClick,
        'BonusRevealButton'     : CvTechChooser().ParentClick,
        'CivicRevealButton'     : CvTechChooser().ParentClick,
        'ProjectInfoButton'     : CvTechChooser().ParentClick,
        'ProcessInfoButton'     : CvTechChooser().ParentClick,
        'FoundReligionButton'   : CvTechChooser().ParentClick,
        'CivDropDown'           : CvTechChooser().CivDropDown,
        }

