## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Scrolling aspect by johny smith in http://forums.civfanatics.com/showthread.php?t=260697&highlight=scrolling+religion
## Inspiration from zappara to handle new religions, extended to handle new types of buildings and units

from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
                                CyGInterfaceScreen, PopupStates, FontTypes,
                                WidgetTypes, CyGame, PanelStyles, ButtonStyles,
                                ActivationTypes, NotifyCode, CyGameTextMgr,
                                FontSymbols, CyInterface)
import PyHelpers
import CvUtil
# import ScreenInput
import CvScreenEnums

# Mod BUG - start
# import BugUtil
import BugCore
# import PlayerUtil
# import ReligionUtil
AdvisorOpt = BugCore.game.Advisors
# Mod BUG - end

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

##johny smith start##
class CvReligionScreen:
    "Religion Advisor Screen"

    def __init__(self):

        self.SCREEN_NAME = "ReligionScreen"
        self.BUTTON_NAME = "ReligionScreenButton"
        self.TITLE_TOP_PANEL = "ReligionsTopPanel"
        self.TITLE_BOTTOM_PANEL = "ReligionsBottomPanel"
        self.AREA_NAME = "ReligionsScreenArea"
        self.HELP_IMAGE_NAME = "CivicsScreenCivicOptionImage"
        self.RELIGION_NAME = "ReligionText"
        self.CONVERT_NAME = "ReligionConvertButton"
        self.CANCEL_NAME = "ReligionCancelButton"
        self.CITY_NAME = "ReligionCity"
        self.HEADER_NAME = "ReligionScreenHeader"
        self.DEBUG_DROPDOWN_ID =  "ReligionDropdownWidget"
        self.TABLE_ID =  "ReligionTableWidget"
        self.AREA1_ID =  "ReligionAreaWidget1"
        self.AREA2_ID =  "ReligionAreaWidget2"
        self.BACKGROUND_ID = "ReligionBackground"
        self.RELIGION_PANEL_ID = "ReligionPanel"
        self.RELIGION_ANARCHY_WIDGET = "ReligionAnarchyWidget"

        self.HEADINGS_TOP = 0
        self.HEADINGS_BOTTOM = 220
        self.HEADINGS_LEFT = 0
        self.HEADINGS_RIGHT = 320
        self.HELP_TOP = 20
        self.HELP_BOTTOM = 610
        self.HELP_LEFT = 350
        self.HELP_RIGHT = 950
        self.BUTTON_SIZE = 48
        self.BIG_BUTTON_SIZE = 64
        self.BOTTOM_LINE_TOP = 630
        self.BOTTOM_LINE_HEIGHT = 60
        self.TEXT_MARGIN = 13

        self.BORDER_WIDTH = 2
        self.HIGHLIGHT_EXTRA_SIZE = 4

        self.Z_SCREEN = -6.1

        self.Y_TITLE = 8
        self.Z_TEXT = 0 # self.Z_SCREEN - 0.2
        self.DZ = -0.2
        self.Z_CONTROLS = self.Z_TEXT

    def setValues(self):
        # screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        resolutionWidth = 1024 # screen.getXResolution()
        resolutionHeigth = 768 # screen.getYResolution()

## johny smith
## this sets the resoultion below
        self.W_SCREEN = resolutionWidth
        self.H_SCREEN = resolutionHeigth

        self.X_POSITION = 0 # screen.centerX(0)
        self.Y_POSITION = 0 # screen.centerY(0)


        self.PANEL_HEIGHT = 55
        self.PANEL_WIDTH = 0
        self.INITIAL_SPACING = 30
        self.HEADINGS_WIDTH = 340
        self.HEADINGS_HEIGHT = 64
        self.BOTTOM_LINE_HEIGHT = 60
        self.RIGHT_LINE_WIDTH = 0
        self.SCROLL_BAR_SPACING = 40
        self.BOTTOM_LINE_TEXT_SPACING = 150

        self.X_EXIT = self.W_SCREEN - 30
        self.Y_EXIT = self.H_SCREEN - 40

        self.X_CANCEL = 552
        self.X_SCREEN = self.W_SCREEN / 2
        self.Y_SCREEN = 396
        self.Y_CANCEL = self.H_SCREEN - 40 # PAE self.H_SCREEN - 40# kmod: 726
        self.HELP_BOTTOM = self.H_SCREEN - 2 * self.PANEL_HEIGHT - self.BOTTOM_LINE_HEIGHT

        self.BOTTOM_LINE_WIDTH = self.W_SCREEN
        self.BOTTOM_LINE_TOP = self.H_SCREEN - self.PANEL_HEIGHT - 70
        self.X_ANARCHY = 21
        self.Y_ANARCHY = 726

        self.LEFT_EDGE_TEXT = 10
        self.X_RELIGION_START = 154 # PAE 154 # kmod 180
        self.Y_RELIGION_START = 154
        self.DX_RELIGION = 116 # PAE 116 # kmod 98
        self.DY_RELIGION = 116
        self.DX_RELIGION_OFFSET = self.DX_RELIGION
        self.X_RELIGION = 0
        self.Y_RELIGION = 35
        self.Y_FOUNDED = 90
        self.Y_HOLY_CITY = 115
        self.Y_INFLUENCE = 140
        self.Y_RELIGION_NAME = 70 # PAE 70 # kmod 58

        self.X_RELIGION_DIFF = self.X_RELIGION_START - self.X_RELIGION
        self.X_RELIGION_AREA = 0 # PAE 0 # kmod 45
        self.Y_RELIGION_AREA = 0 # PAE 0 # kmod 84
        self.W_RELIGION_AREA = 1008 + self.BUTTON_SIZE # PAE 1008 + self.BUTTON_SIZE # kmod 934
        self.H_RELIGION_AREA = 180 # PAE 180 # kmod 175

        self.X_CITY1_AREA = 45
        self.X_CITY2_AREA = 522
        self.Y_CITY_AREA = 250 # PAE 250 # kmod 282
        self.W_CITY_AREA = 457
        self.H_CITY_AREA = 460 # PAE 460 # kmod 395

        self.X_CITY = 10
        self.DY_CITY = 38

# Mod BUG - start
        # self.NUM_RELIGIONS = -1
        # self.COL_ZOOM_CITY = 0
        # self.COL_CITY_NAME = 1
        # self.COL_FIRST_RELIGION = 2
        # self.COL_FIRST_UNIT = 9
        # self.COL_FIRST_BUILDING = 10
        # self.COL_EFFECTS = 14
        # self.TABLE_COLUMNS = 15
# Mod BUG - end

        self.iReligionExamined = -1
        self.iReligionSelected = -1
        self.iReligionOriginal = -1
        self.iActivePlayer = -1

        self.bScreenUp = False

        self.ReligionScreenInputMap = {
            self.RELIGION_NAME      : self.ReligionScreenButton,
            self.BUTTON_NAME        : self.ReligionScreenButton,
            self.CONVERT_NAME       : self.ReligionConvert,
            self.CANCEL_NAME        : self.ReligionCancel,
            }

        # Mod BUG Constants
        self.bBUGConstants = False

    def getScreen(self):
        return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.RELIGION_SCREEN)

    def setActivePlayer(self, iPlayer):

        self.iActivePlayer = iPlayer
        activePlayer = gc.getPlayer(iPlayer)

        self.m_paeCurrentReligions = []
        self.m_paeDisplayReligions = []
        self.m_paeOriginalReligions = []
        for i in xrange (gc.getNumReligionInfos()):
            self.m_paeCurrentReligions.append(activePlayer.getReligions(i));
            self.m_paeDisplayReligions.append(activePlayer.getReligions(i));
            self.m_paeOriginalReligions.append(activePlayer.getReligions(i));

    def interfaceScreen (self):

        # johny smith ScreenTweaks LINE:
        self.setValues()
        self.SCREEN_ART = ArtFileMgr.getInterfaceArtInfo("TECH_BG").getPath()
        self.NO_STATE_BUTTON_ART = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
        self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
        self.CONVERT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_RELIGION_CONVERT", ()).upper() + "</font>"
        self.CANCEL_TEXT = u"<font=4>" + localText.getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>"

        self.iActivePlayer = gc.getGame().getActivePlayer()

# Mod BUG - start
        # if self.NUM_RELIGIONS == -1:
            # self.NUM_RELIGIONS = gc.getNumReligionInfos()
            # self.COL_FIRST_UNIT = self.COL_FIRST_RELIGION + self.NUM_RELIGIONS
            # self.COL_FIRST_BUILDING = self.COL_FIRST_UNIT + ReligionUtil.getNumUnitTypes()
            # self.COL_EFFECTS = self.COL_FIRST_BUILDING + ReligionUtil.getNumBuildingTypes()
            # self.TABLE_COLUMNS = self.COL_EFFECTS + 1
# Mod BUG - end

        self.bScreenUp = True

        screen = self.getScreen()
        if screen.isActive():
            return
        screen.setRenderInterfaceOnly(True);
        screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

        # Set the background and exit button, and show the screen
        screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

        screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
        ## Panels on the Top(name of screen) and bottom(Cancel, Exit, Revolution buttons)
        screen.addPanel(self.TITLE_TOP_PANEL, u"", u"", True, False, 0, 0, self.W_SCREEN, self.PANEL_HEIGHT, PanelStyles.PANEL_STYLE_TOPBAR)
        screen.addPanel(self.TITLE_BOTTOM_PANEL, u"", u"", True, False, 0, self.H_SCREEN - self.PANEL_HEIGHT, self.W_SCREEN, self.PANEL_HEIGHT, PanelStyles.PANEL_STYLE_BOTTOMBAR)
        screen.addPanel(self.RELIGION_PANEL_ID, "", "", False, True, -10, 50, self.W_SCREEN + 20, self.H_RELIGION_AREA, PanelStyles.PANEL_STYLE_MAIN)
        screen.setText(self.CANCEL_NAME, "Background", self.CANCEL_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_CANCEL, self.Y_CANCEL, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)

        screen.showWindowBackground(False)

        # Header...
        # screen.setLabel(self.HEADER_NAME, "Background", u"<font=4b>" + localText.getText("TXT_KEY_RELIGION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # Make the scrollable areas for the city list...

        if CyGame().isDebugMode():
            self.szDropdownName = self.DEBUG_DROPDOWN_ID
            screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
            for j in xrange(gc.getMAX_PLAYERS()):
                if gc.getPlayer(j).isAlive():
                    screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

        # self.X_RELIGION_AREA = self.PANEL_WIDTH/8 * 7 # PAE self.PANEL_WIDTH/8 * 7 # kmod 45
        # self.Y_RELIGION_AREA = self.PANEL_HEIGHT/8 * 7 # PAE self.PANEL_HEIGHT/8 * 7 # kmod 84
        # self.W_RELIGION_AREA = self.W_SCREEN # PAE self.W_SCREEN # kmod 934
        # self.H_RELIGION_AREA = self.Y_RELIGION_AREA + 180 + 5 # PAE self.Y_RELIGION_AREA + 180 + 5 # kmod 175
        # self.RELIGIONS = range(gc.getNumReligionInfos()) # K-Mod. (the original BUG code simply doesn't run.)

        # Make the scrollable area for the religion list...
        # screen.addPanel(self.RELIGION_PANEL_ID, "", "", False, True, self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA+5, PanelStyles.PANEL_STYLE_MAIN)
        screen.addScrollPanel("ReligionList", u"", self.PANEL_WIDTH/8 * 7, self.PANEL_HEIGHT/8 * 7, self.W_SCREEN, self.Y_RELIGION_AREA + self.H_RELIGION_AREA + 5, PanelStyles.PANEL_STYLE_EXTERNAL )
        # screen.addScrollPanel("ReligionList", u"", self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.setActivation("ReligionList", ActivationTypes.ACTIVATE_NORMAL)

        # Draw Religion info
        self.drawReligionInfo()

        self.drawHelpInfo()

        self.drawCityInfo(self.iReligionSelected)

    # Draws the religion buttons and information
    def drawReligionInfo(self):

        screen = self.getScreen()

        # Put everything on a scrollable area
        szArea = "ReligionList"

        # Religion buttons at the top
        ## johny smith
        ## This draws the symbols
        ## Puts the symbols in a loop
        ## Attachs the symbols so they will scroll
        xLoop = self.X_RELIGION_START
        for iRel in xrange(gc.getNumReligionInfos()):
            szButtonName = self.getReligionButtonName(iRel)
            if gc.getGame().getReligionGameTurnFounded(iRel) >= 0:
                screen.addCheckBoxGFCAt(szArea, szButtonName,
                                        gc.getReligionInfo(iRel).getButton(),
                                        ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                                        self.X_RELIGION_AREA + xLoop - 25,
                                        self.Y_RELIGION_AREA + 10, self.BUTTON_SIZE, # kmod + 5
                                        self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL,
                                        -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)
            else:
                screen.setImageButtonAt(szButtonName, szArea, gc.getReligionInfo(iRel).getButtonDisabled(), self.X_RELIGION_AREA + xLoop - 25, self.Y_RELIGION_AREA + 10, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
            szName = self.getReligionTextName(iRel)
            szLabel = gc.getReligionInfo(iRel).getDescription()
            screen.setLabelAt(szName, szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, self.X_RELIGION_AREA + xLoop, self.Y_RELIGION_NAME, self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
            xLoop += self.DX_RELIGION

        screen.addCheckBoxGFCAt(szArea, szButtonName, self.NO_STATE_BUTTON_ART,
                                ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                                self.X_RELIGION_AREA + xLoop - 25,
                                self.Y_RELIGION_AREA + 10, self.BUTTON_SIZE,
                                self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL,
                                -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)

        szName = self.getReligionTextName(gc.getNumReligionInfos())
        szLabel = localText.getText("TXT_KEY_RELIGION_SCREEN_NO_STATE", ())

        screen.setLabelAt(szName, szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY,  self.X_RELIGION_AREA + xLoop, self.Y_RELIGION_NAME, self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()
        if self.iReligionSelected == -1:
            self.iReligionSelected = gc.getNumReligionInfos()
        self.iReligionExamined = self.iReligionSelected
        self.iReligionOriginal = self.iReligionSelected


    def drawHelpInfo(self):

        screen = self.getScreen()
        szArea = "ReligionList"

        ## johny smith
        ## This attaches the text to the panel
        ## This is for every line of font
        # Founded...
        screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_DATE_FOUNDED", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # Date Founded:
        xLoop = self.X_RELIGION_START
        for iRel in xrange(gc.getNumReligionInfos()):
            if gc.getGame().getReligionGameTurnFounded(iRel) >= 0:
                szFounded = CyGameTextMgr().getTimeStr(gc.getGame().getReligionGameTurnFounded(iRel), False)
                screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, self.X_RELIGION_AREA + xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1) # kmod: xLoop,
                xLoop += self.DX_RELIGION

        # Holy City...
        screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_HOLY_CITY", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        xLoop = self.X_RELIGION_START
        for iRel in xrange(gc.getNumReligionInfos()):
            if gc.getGame().getReligionGameTurnFounded(iRel) >= 0:
                pHolyCity = gc.getGame().getHolyCity(iRel)
                if pHolyCity.isNone():
                    szFounded = localText.getText("TXT_KEY_NONE", ())
                    screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                elif not pHolyCity.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False):
                    szFounded = localText.getText("TXT_KEY_UNKNOWN", ())
                    screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                else:
                    szFounded = pHolyCity.getName()
                    screen.setLabelAt("", szArea, u"(%s)" % gc.getPlayer(pHolyCity.getOwner()).getCivilizationAdjective(0), CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY+8, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                    screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY-8, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

            xLoop += self.DX_RELIGION

        # Influence...
        screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_INFLUENCE", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        xLoop = self.X_RELIGION_START
        for iRel in xrange(gc.getNumReligionInfos()):
            if gc.getGame().getReligionGameTurnFounded(iRel) >= 0:
                szFounded = str(gc.getGame().calculateReligionPercent(iRel)) + "%"
                screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
            xLoop += self.DX_RELIGION

        self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()
        if self.iReligionSelected == -1:
            self.iReligionSelected = gc.getNumReligionInfos()
        self.iReligionExamined = self.iReligionSelected
        self.iReligionOriginal = self.iReligionSelected

##johny smith end##

    # Draws the city list
    def drawCityInfo(self, iReligion):

        if not self.bScreenUp:
            return

        screen = self.getScreen()

        if iReligion == gc.getNumReligionInfos():
            iLinkReligion = -1
        else:
            iLinkReligion = iReligion

        screen.addPanel(self.AREA1_ID, "", "", True, True, self.X_CITY1_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)
        screen.addPanel(self.AREA2_ID, "", "", True, True, self.X_CITY2_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)

        # szArea = self.RELIGION_PANEL_ID
        for iRel in xrange(gc.getNumReligionInfos()):
            if self.iReligionSelected == iRel:
                screen.setState(self.getReligionButtonName(iRel), True)
            else:
                screen.setState(self.getReligionButtonName(iRel), False)

        if self.iReligionSelected == gc.getNumReligionInfos():
            screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), True)
        else:
            screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), False)

        iPlayer = PyPlayer(self.iActivePlayer)
        cityList = iPlayer.getCityList()

# start of BUG indent for new code
        # Loop through the cities
        szLeftCities = u""
        szRightCities = u""
        for i in xrange(len(cityList)):

                bFirstColumn = (i % 2 == 0)

                pLoopCity = cityList[i]

                # Constructing the City name...
                szCityName = u""
                if pLoopCity.isCapital():
                    szCityName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)

                lHolyCity = pLoopCity.getHolyCity()
                if lHolyCity:
                    for iI in xrange(len(lHolyCity)):
                        szCityName += u"%c" %(gc.getReligionInfo(lHolyCity[iI]).getHolyCityChar())

                lReligions = pLoopCity.getReligions()
                if lReligions:
                    for iI in xrange(len(lReligions)):
                        if lReligions[iI] not in lHolyCity:
                            szCityName += u"%c" %(gc.getReligionInfo(lReligions[iI]).getChar())

                szCityName += pLoopCity.getName()[0:17] + "  "

                if iLinkReligion == -1:
                    bFirst = True
                    for iI in xrange(len(lReligions)):
                        szTempBuffer = CyGameTextMgr().getReligionHelpCity(lReligions[iI], pLoopCity.GetCy(), False, False, False, True)
                        if szTempBuffer:
                            if not bFirst:
                                szCityName += u", "
                            szCityName += szTempBuffer
                            bFirst = False
                else:
                    szCityName += CyGameTextMgr().getReligionHelpCity(iLinkReligion, pLoopCity.GetCy(), False, False, True, False)

                if bFirstColumn:
                    szLeftCities += u"<font=3>" + szCityName + u"</font>\n"
                else:
                    szRightCities += u"<font=3>" + szCityName + u"</font>\n"

        screen.addMultilineText("Child" + self.AREA1_ID, szLeftCities, self.X_CITY1_AREA+5, self.Y_CITY_AREA+5, self.W_CITY_AREA-10, self.H_CITY_AREA-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
        screen.addMultilineText("Child" + self.AREA2_ID, szRightCities, self.X_CITY2_AREA+5, self.Y_CITY_AREA+5, self.W_CITY_AREA-10, self.H_CITY_AREA-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# end of BUG indent of original code

        # Convert Button....
        # iLink = 0
        # if gc.getPlayer(self.iActivePlayer).canChangeReligion():
            # iLink = 1

        if not self.canConvert(iLinkReligion) or iLinkReligion == self.iReligionOriginal:
            screen.setText(self.CONVERT_NAME, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
            screen.hide(self.CANCEL_NAME)
            szAnarchyTime = CyGameTextMgr().setConvertHelp(self.iActivePlayer, iLinkReligion)
        else:
            screen.setText(self.CONVERT_NAME, "Background", self.CONVERT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CONVERT, iLinkReligion, 1)
            screen.show(self.CANCEL_NAME)
            szAnarchyTime = localText.getText("TXT_KEY_ANARCHY_TURNS", (gc.getPlayer(self.iActivePlayer).getReligionAnarchyLength(), ))

        # Turns of Anarchy Text...
        screen.setLabel(self.RELIGION_ANARCHY_WIDGET, "Background", u"<font=3>" + szAnarchyTime + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ANARCHY, self.Y_ANARCHY, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

    def getReligionButtonName(self, iReligion):
        szName = self.BUTTON_NAME + str(iReligion)
        return szName

    def getReligionTextName(self, iReligion):
        szName = self.RELIGION_NAME + str(iReligion)
        return szName

    def canConvert(self, iReligion):
        iCurrentReligion = gc.getPlayer(self.iActivePlayer).getStateReligion()
        if iReligion == gc.getNumReligionInfos():
            iConvertReligion = -1
        else:
            iConvertReligion = iReligion

        return (iConvertReligion != iCurrentReligion and gc.getPlayer(self.iActivePlayer).canConvert(iConvertReligion))

    # Will handle the input for this screen...
    def handleInput (self, inputClass):

        screen = self.getScreen()
        szWidgetName = inputClass.getFunctionName()
        # szFullWidgetName = szWidgetName + str(inputClass.getID())
        # code = inputClass.getNotifyCode()

        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED and szWidgetName != self.TABLE_ID:

            iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
            self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
            self.drawReligionInfo()
            self.drawCityInfo(self.iReligionSelected)
            return 1
        # Mod BUG Zoom to City
        elif szWidgetName == self.TABLE_ID:
            if inputClass.getMouseX() == 0:
                screen.hideScreen()
                pPlayer = gc.getPlayer(inputClass.getData1())
                pCity = pPlayer.getCity(inputClass.getData2())
#               CyCamera().JustLookAtPlot(pCity.plot())

                CyInterface().selectCity(pCity, True);

        elif self.ReligionScreenInputMap.has_key(inputClass.getFunctionName()):
            'Calls function mapped in ReligionScreenInputMap'
            # only get from the map if it has the key

            # get bound function from map and call it
            self.ReligionScreenInputMap.get(inputClass.getFunctionName())(inputClass)
            return 1
        return 0

    def update(self, fDelta):
        return

    # Religion Button
    def ReligionScreenButton( self, inputClass ):
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            if inputClass.getID() == gc.getNumReligionInfos() or gc.getGame().getReligionGameTurnFounded(inputClass.getID()) >= 0:
                self.iReligionSelected = inputClass.getID()
                self.iReligionExamined = self.iReligionSelected
                self.drawCityInfo(self.iReligionSelected)
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON:
            if inputClass.getID() == gc.getNumReligionInfos() or gc.getGame().getReligionGameTurnFounded(inputClass.getID()) >= 0:
                self.iReligionExamined = inputClass.getID()
                self.drawCityInfo(self.iReligionExamined)
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF:
            self.iReligionExamined = self.iReligionSelected
            self.drawCityInfo(self.iReligionSelected)
        return 0

    def ReligionConvert(self, inputClass):
        screen = self.getScreen()
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            screen.hideScreen()

    def ReligionCancel(self, inputClass):
        # screen = self.getScreen()
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            self.iReligionSelected = self.iReligionOriginal
            if self.iReligionSelected == -1:
                self.iReligionSelected = gc.getNumReligionInfos()
            self.drawCityInfo(self.iReligionSelected)

    def calculateBuilding (self, city, bldg):
        if city.getNumBuilding(bldg) > 0:
            return self.objectHave
        elif city.GetCy().getFirstBuildingOrder(bldg) != -1:
            return self.objectUnderConstruction
        elif city.GetCy().canConstruct(bldg, False, False, False):
            return self.objectPossible
        elif city.GetCy().canConstruct(bldg, True, False, False):
            return self.objectPossibleConcurrent
        else:
            return self.objectNotPossible
