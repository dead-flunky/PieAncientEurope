# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Edited by Pie, Austria

# import time

# from CvPythonExtensions import *
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
    CyUserProfile, PlayerOptionTypes, WidgetTypes, ControlTypes, DomainTypes,
    CommerceTypes, CyInterface, CyGInterfaceScreen, ButtonStyles, InterfaceVisibility,
    CyMessageControl, CyGame, TableStyles, CyEngine, CyAudioGame, HitTestTypes,
    InterfaceModeTypes, MissionTypes, isLimitedWonderClass, InfoBarTypes,
    ActivityTypes, PanelStyles, FontTypes, GameOptionTypes, PopupStates,
    CyGameTextMgr, FontSymbols, OrderTypes, MultiplayerOptionTypes,
    InterfaceDirtyBits, NotifyCode, CyGlobeLayerManager, YieldTypes,
    EndTurnButtonStates, getClockText, CultureLevelTypes, CityTabTypes)
import CvUtil
# import ScreenInput
import CvScreenEnums
import CvEventInterface
import PyHelpers

import PAE_Trade
import PAE_Cultivation
import PAE_Unit
# import PAE_Mercenaries
import PAE_City
import PAE_Lists as L
import PAE_Vassal

# Mod BUG - DLL - start
# import BugDll
# Mod BUG - DLL - end

# Mod BUG - Options - start
import BugCore
import BugOptions
# import BugOptionsScreen
# import BugPath
import BugUtil
import CityUtil
# Mod BUG - Options - end

# Mod BUG - PLE - start
# PleOpt = BugCore.game.PLE
# Mod BUG - PLE - end

# Mod BUG - Align Icons - start
# import Scoreboard
import PlayerUtil
# Mod BUG - Align Icons - end

# Mod BUG - Worst Enemy - start
import AttitudeUtil
# Mod BUG - Refuses to Talk - end

# Mod BUG - Fractional Trade - start
import TradeUtil
# Mod BUG - Fractional Trade - end

# import BugUnitPlot

# Mod BUG - 3.17 No Espionage - start
import GameUtil
# Mod BUG - 3.17 No Espionage - end

# Mod BUG - Reminders - start
# import ReminderEventManager
# Mod BUG - Reminders - end

# Mod BUG - Great General Bar - start
# import GGUtil
# Mod BUG - Great General Bar - end

# Mod BUG - Great Person Bar - start
import GPUtil
# Mod BUG - Great Person Bar - end

# Mod BUG - Progress Bar - Tick Marks - start
import ProgressBarUtil
# Mod BUG - Progress Bar - Tick Marks - end

# PLE Code
# import PLE
import MonkeyTools as mt


# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
PyInfo = PyHelpers.PyInfo

ClockOpt = BugCore.game.NJAGC
ScoreOpt = BugCore.game.Scores
MainOpt = BugCore.game.MainInterface
CityScreenOpt = BugCore.game.CityScreen
PleOpt = BugCore.game.PLE

g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

MAX_SELECTED_TEXT = 5
MAX_DISPLAYABLE_BUILDINGS = 15
MAX_DISPLAYABLE_TRADE_ROUTES = 4
MAX_BONUS_ROWS = 10

# Mod BUG - field of view slider - start
DEFAULT_FIELD_OF_VIEW = 44
# PAE (False for better ingame python programming)
bFieldOfView = CyUserProfile().getPlayerOption(PlayerOptionTypes.PLAYEROPTION_MODDER_2)
# Mod BUG - field of view slider - end

# SPECIALIST STACKER        05/02/07      JOHNY
MAX_CITIZEN_BUTTONS = 20 # kmod 8

# <STACKER START>
# Modify this if you want to change the distance between the stacked specialists.
# Default value is 9
SPECIALIST_STACK_WIDTH = 9

# Set this to False if you don't want to have the yellow highlight displayed when
# citizens are forced to be specialized. Default value is True
g_bHighlightForcedSpecialists = True

# Set this to True if you want to stack the super specialists. Default value is False
g_bStackSuperSpecialists = True

# Change this if you want to display a different number of super specialists when
# g_bStackSuperSpecialists is set to False. Default value is 6
MAX_SUPER_SPECIALIST_BUTTONS = 6

# Modify this if you want to change the distance between the stacked super specialists
# Default value is 15
SUPER_SPECIALIST_STACK_WIDTH = 15

# Set this to False if you want to show every super specialist in the city. This
# feature will only work if g_bStackSuperSpecialists is set to True and works best of
# you have set g_bDynamicSuperSpecialistsSpacing to True. Default value is True.
g_bDisplayUniqueSuperSpecialistsOnly = False

# If this is set to True then the SUPER_SPECIALIST_STACK_WIDTH set value will not
# be used. Default value is True
g_bDynamicSuperSpecialistsSpacing = True

# Set this to True if you want to stack the angry citizens. Default value is False
g_bStackAngryCitizens = False

# Change this if you want to display a different number of angry citizens when
# g_bStackAngryCitizens is set to False. Default value is 6
MAX_ANGRY_CITIZEN_BUTTONS = 6

# Modify this if you want to change the distance between the stacked angry citizens.
# Default value is 15
ANGRY_CITIZEN_STACK_WIDTH = 15

# If this is set to True then the ANGRY_CITIZEN_STACK_WIDTH set value will not
# be used. Default value is True
g_bDynamicAngryCitizensSpacing = True

# Do not edit g_SuperSpecialistCount or g_iAngryCitizensCount, otherwise really bad
# things could happen.
g_iSuperSpecialistCount = 0
g_iAngryCitizensCount = 0

# SPECIALIST STACKER        END

SELECTION_BUTTON_COLUMNS = 8
SELECTION_BUTTON_ROWS = 2
NUM_SELECTION_BUTTONS = SELECTION_BUTTON_ROWS * SELECTION_BUTTON_COLUMNS

g_iNumBuildingWidgets = MAX_DISPLAYABLE_BUILDINGS
g_iNumTradeRouteWidgets = MAX_DISPLAYABLE_TRADE_ROUTES

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 32
iEndOfTurnPosX = 296  # distance from right
iEndOfTurnPosY = 147  # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsExtent = 228
iMinimapButtonsX = 227
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32
iMinimapButtonWidth = 24
iMinimapButtonHeight = 24

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsX = 235
iGlobeLayerOptionsY_Regular = 170  # distance from bottom edge
iGlobeLayerOptionsY_Minimal = 38  # distance from bottom edge
iGlobeLayerOptionsWidth = 400
iGlobeLayerOptionHeight = 24

# STACK BAR
#####################
iStackBarHeight = 27


# MULTI LIST
#####################
iMultiListXL = 318
iMultiListXR = 332


# TOP CENTER TITLE
#####################
iCityCenterRow1X = 398
iCityCenterRow1Y = 78
iCityCenterRow2X = 398
iCityCenterRow2Y = 104

iCityCenterRow1Xa = 347
iCityCenterRow2Xa = 482


g_iNumTradeRoutes = 0
g_iNumBuildings = 0
g_iNumLeftBonus = 0
g_iNumCenterBonus = 0
g_iNumRightBonus = 0

g_szTimeText = ""

# Mod BUG - NJAGC - start
g_bShowTimeTextAlt = False
g_iTimeTextCounter = -1

g_pSelectedUnit = 0
# Mod BUG - NJAGC - end

# Mod BUG - Raw Yields - start
import RawYields
g_bRawShowing = False
g_bYieldView, g_iYieldType = RawYields.getViewAndType(0)
g_iYieldTiles = RawYields.WORKED_TILES
RAW_YIELD_HELP = ("TXT_KEY_RAW_YIELD_VIEW_TRADE",
                  "TXT_KEY_RAW_YIELD_VIEW_FOOD",
                  "TXT_KEY_RAW_YIELD_VIEW_PRODUCTION",
                  "TXT_KEY_RAW_YIELD_VIEW_COMMERCE",
                  "TXT_KEY_RAW_YIELD_TILES_WORKED",
                  "TXT_KEY_RAW_YIELD_TILES_CITY",
                  "TXT_KEY_RAW_YIELD_TILES_OWNED",
                  "TXT_KEY_RAW_YIELD_TILES_ALL" )
# Mod BUG - Raw Yields - end

m_iNumPlotListButtons = 0

HELP_TEXT_MINIMUM_WIDTH = 300


# Mod BUG - start
g_mainInterface = None
def onSwitchHotSeatPlayer(argsList):
    if g_mainInterface:
        g_mainInterface.resetEndTurnObjects()
# Mod BUG - end

class CvMainInterface:
    "Main Interface Screen"

    def __init__(self):
# Mod BUG - start
        global g_mainInterface
        g_mainInterface = self
# Mod BUG - end

# Platy ScoreBoard adapted and changed by Pie
        self.iScoreRows = 0
        self.iScoreWidth = 150
        self.iScoreHidePoints = False  # PAE
# Platy ScoreBoard end

# Mod BUG - PLE - start
        self.iMaxPlotListIcons      = 0
        self.xResolution = 0
        self.yResolution = 0

        self.tLastMousePos          = (0,0)
        self.bInfoPaneActive        = False
        self.iInfoPaneCnt           = 0
        self.iLastInfoPaneCnt       = -1

        self.UNIT_INFO_PANE         = "PLE_UNIT_INFO_PANE_ID"
        self.UNIT_INFO_TEXT         = "PLE_UNIT_INFO_TEXT_ID"
        self.UNIT_INFO_TEXT_SHADOW  = "PLE_UNIT_INFO_TEXT_SHADOW_ID"
# Mod BUG - PLE - end

# Mod BUG - field of view slider - start
        self.szSliderTextId = "FieldOfViewSliderText"
        self.sFieldOfView_Text = ""
        self.szSliderId = "FieldOfViewSlider"
        self.iField_View_Prev = -1
# Mod BUG - field of view slider - end

        # Ramk - City Widgets
        self.buildWidgets = [
            WidgetTypes.WIDGET_TRAIN,
            WidgetTypes.WIDGET_CONSTRUCT,
            WidgetTypes.WIDGET_CREATE,
            WidgetTypes.WIDGET_MAINTAIN
        ]

        # PAE Taxes Bar
        self.bHideTaxes = False

############## Basic operational functions ###################

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################

    def numPlotListButtons(self):
        return self.m_iNumPlotListButtons

    def initState(self, screen=None):
        """
        Initialize screen instance (self.foo) and global variables.

        This function is called before drawing the screen (from interfaceScreen() below)
        and anytime the Python modules are reloaded (from CvEventInterface).

        THIS FUNCTION MUST NOT ALTER THE SCREEN -- screen.foo()
        """
        if screen is None:
            screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        self.xResolution = screen.getXResolution()
        self.yResolution = screen.getYResolution()

# Mod BUG - Raw Yields - begin
        global g_bYieldView
        global g_iYieldType
        g_bYieldView, g_iYieldType = RawYields.getViewAndType(CityScreenOpt.getRawYieldsDefaultView())
# Mod BUG - Raw Yields - end

        # Global variables being set here
        global g_NumEmphasizeInfos
        global g_NumCityTabTypes
        global g_NumHurryInfos
        global g_NumUnitClassInfos
        global g_NumBuildingClassInfos
        global g_NumProjectInfos
        global g_NumProcessInfos
        global g_NumActionInfos

        g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
        g_NumCityTabTypes = CityTabTypes.NUM_CITYTAB_TYPES
        g_NumHurryInfos = gc.getNumHurryInfos()
        g_NumUnitClassInfos = gc.getNumUnitClassInfos()
        g_NumBuildingClassInfos = gc.getNumBuildingClassInfos()
        g_NumProjectInfos = gc.getNumProjectInfos()
        g_NumProcessInfos = gc.getNumProcessInfos()
        g_NumActionInfos = gc.getNumActionInfos()

# Mod BUG - field of view slider - start
        iBtnY = 27
        self.iX_FoVSlider = self.xResolution - 120
        self.iY_FoVSlider = iBtnY + 30
        self.sFieldOfView_Text = localText.getText("TXT_KEY_MAININTERFACE_FIELDOFVIEW_TEXT", ())
        self.DEFAULT_FIELD_OF_VIEW = max(40, min(80, self.xResolution / 30)) # K-Mod (bigger FoW for bigger monitors. They'll appreciate it. Trust me.)

        self.iField_View = int(MainOpt.getFieldOfView())

        # K-Mod
        if self.iField_View < 0:
            self.iField_View = self.DEFAULT_FIELD_OF_VIEW
# Mod BUG - field of view slider - end

# Mod BUG - Progress Bar - Tick Marks - start
        xCoord = 268 + (self.xResolution - 1024) / 2
        self.pBarResearchBar_n = ProgressBarUtil.ProgressBar("ResearchBar-Canvas", xCoord, 2, 487, iStackBarHeight, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"), ProgressBarUtil.TICK_MARKS, True)
        self.pBarResearchBar_n.addBarItem("ResearchBar")
        self.pBarResearchBar_n.addBarItem("ResearchText")
# Mod BUG - Progress Bar - Tick Marks - end

# Mod BUG - Progress Bar - Tick Marks - start
        xCoord = 268 + (self.xResolution - 1440) / 2
        xCoord += 6 + 84
        self.pBarResearchBar_w = ProgressBarUtil.ProgressBar("ResearchBar-w-Canvas", xCoord, 2, 487, iStackBarHeight, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"), ProgressBarUtil.TICK_MARKS, True)
        self.pBarResearchBar_w.addBarItem("ResearchBar-w")
        self.pBarResearchBar_w.addBarItem("ResearchText")
# Mod BUG - Progress Bar - Tick Marks - end

# Mod BUG - Progress Bar - Tick Marks - start
        self.pBarPopulationBar = ProgressBarUtil.ProgressBar("PopulationBar-Canvas", iCityCenterRow1X, iCityCenterRow1Y-4, self.xResolution - (iCityCenterRow1X*2), iStackBarHeight, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), ProgressBarUtil.SOLID_MARKS, True)
        self.pBarPopulationBar.addBarItem("PopulationBar")
        self.pBarPopulationBar.addBarItem("PopulationText")
        self.pBarProductionBar = ProgressBarUtil.ProgressBar("ProductionBar-Canvas", iCityCenterRow2X, iCityCenterRow2Y-4, self.xResolution - (iCityCenterRow2X*2), iStackBarHeight, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), ProgressBarUtil.TICK_MARKS, True)
        self.pBarProductionBar.addBarItem("ProductionBar")
        self.pBarProductionBar.addBarItem("ProductionText")
        self.pBarProductionBar_Whip = ProgressBarUtil.ProgressBar("ProductionBar-Whip-Canvas", iCityCenterRow2X, iCityCenterRow2Y-4, self.xResolution - (iCityCenterRow2X*2), iStackBarHeight, gc.getInfoTypeForString("COLOR_YELLOW"), ProgressBarUtil.CENTER_MARKS, False)
        self.pBarProductionBar_Whip.addBarItem("ProductionBar")
        self.pBarProductionBar_Whip.addBarItem("ProductionText")
# Mod BUG - Progress Bar - Tick Marks - end

        self.m_iNumPlotListButtons = (self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34

# Mod BUG - BUG unit plot draw method - start bug unit panel
        # self.BupPanel = BugUnitPlot.BupPanel(screen, screen.getXResolution(), screen.getYResolution(), iMultiListXL+iMultiListXR, self.numPlotListButtons(), gc.getMAX_PLOT_LIST_ROWS())
# Mod BUG - BUG unit plot draw method - end

    def interfaceScreen(self):
        """
        Draw all of the screen elements.

        This function is called once after starting or loading a game.

        THIS FUNCTION MUST NOT CREATE ANY INSTANCE OR GLOBAL VARIABLES.
        It may alter existing ones created in __init__() or initState(), however.
        """
        if CyGame().isPitbossHost():
            return 0

        global MAX_SELECTED_TEXT
        global MAX_DISPLAYABLE_BUILDINGS
        global MAX_DISPLAYABLE_TRADE_ROUTES
        global MAX_BONUS_ROWS
        global MAX_CITIZEN_BUTTONS

        # SPECIALIST STACKER        05/02/07      JOHNY
        global g_iSuperSpecialistCount
        global g_iAngryCitizensCount

        global SPECIALIST_STACK_WIDTH
        global g_bHighlightForcedSpecialists
        global g_bStackSuperSpecialists
        global MAX_SUPER_SPECIALIST_BUTTONS
        global SUPER_SPECIALIST_STACK_WIDTH
        global g_bDisplayUniqueSuperSpecialistsOnly
        global g_bDynamicSuperSpecialistsSpacing
        global g_bStackAngryCitizens
        global MAX_ANGRY_CITIZEN_BUTTONS
        global ANGRY_CITIZEN_STACK_WIDTH
        global g_bDynamicAngryCitizensSpacing

        # SPECIALIST STACKER        END

        # Mod BUG - field of view
        # This is the main interface screen, create it as such
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        self.initState(screen)
        screen.setForcedRedraw(True)
        screen.setDimensions(0, 0, self.xResolution, self.yResolution)

        # to avoid changing all the code below
        xResolution = self.xResolution
        yResolution = self.yResolution
        # Mod BUG - field of view end

        # Find out our resolution
        self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
        self.m_iNumMenuButtons = (xResolution - (iMultiListXL+iMultiListXR) - 18) / 50  # PAE, Ramk 34=>50

        # To decide if mouse clicked on first or second row of the menu.
        self.secondRowBorder = yResolution-113+50
        self.ySecondRow = 0

        screen.setDimensions(0, 0, xResolution, yResolution)

        # Help Text Area
        screen.setHelpTextArea(350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150)

        # Center Left
        screen.addPanel("InterfaceCenterLeftBackgroundWidget", u"", u"", True, False, 0, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceCenterLeftBackgroundWidget", "Panel_City_Left_Style")
        screen.hide("InterfaceCenterLeftBackgroundWidget")

        # Top Left
        screen.addPanel("InterfaceTopLeftBackgroundWidget", u"", u"", True, False, 258, 0, xResolution - 516, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceTopLeftBackgroundWidget", "Panel_City_Top_Style")
        screen.hide("InterfaceTopLeftBackgroundWidget")

        # Center Right
        screen.addPanel("InterfaceCenterRightBackgroundWidget", u"", u"", True, False, xResolution - 258, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceCenterRightBackgroundWidget", "Panel_City_Right_Style")
        screen.hide("InterfaceCenterRightBackgroundWidget")

        screen.addPanel("CityScreenAdjustPanel", u"", u"", True, False, 10, 44, 238, 105, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("CityScreenAdjustPanel", "Panel_City_Info_Style")
        screen.hide("CityScreenAdjustPanel")

        screen.addPanel("TopCityPanelLeft", u"", u"", True, False, 260, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("TopCityPanelLeft", "Panel_City_TanTL_Style")
        screen.hide("TopCityPanelLeft")

        screen.addPanel("TopCityPanelRight", u"", u"", True, False, xResolution/2, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("TopCityPanelRight", "Panel_City_TanTR_Style")
        screen.hide("TopCityPanelRight")

        # Top Bar

        # SF CHANGE
        screen.addPanel("CityScreenTopWidget", u"", u"", True, False, 0, -2, xResolution, 41, PanelStyles.PANEL_STYLE_STANDARD)

        screen.setStyle("CityScreenTopWidget", "Panel_TopBar_Style")
        screen.hide("CityScreenTopWidget")

        # Top Center Title
        screen.addPanel("CityNameBackground", u"", u"", True, False, 260, 31, xResolution - (260*2), 38, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("CityNameBackground", "Panel_City_Title_Style")
        screen.hide("CityNameBackground")

        # Left Background Widget
        screen.addDDSGFC("InterfaceLeftBackgroundWidget", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOTTOM_LEFT").getPath(), 0, yResolution - 184, 304, 184, WidgetTypes.WIDGET_GENERAL, -1, -1) #0, -164,304,164
        screen.hide("InterfaceLeftBackgroundWidget")

        # Center Background Widget
        screen.addPanel("InterfaceCenterBackgroundWidget", u"", u"", True, False, 296, yResolution - 133, xResolution - (296*2), 133, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceCenterBackgroundWidget", "Panel_Game_HudBC_Style")
        screen.hide("InterfaceCenterBackgroundWidget")

        # Left Background Widget
        screen.addPanel("InterfaceLeftBackgroundWidget", u"", u"", True, False, 0, yResolution - 188, 304, 188, PanelStyles.PANEL_STYLE_STANDARD) #0, -168,304,168
        screen.setStyle("InterfaceLeftBackgroundWidget", "Panel_Game_HudBL_Style")
        screen.hide("InterfaceLeftBackgroundWidget")

        # Right Background Widget
        screen.addPanel("InterfaceRightBackgroundWidget", u"", u"", True, False, xResolution - 304, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceRightBackgroundWidget", "Panel_Game_HudBR_Style")
        screen.hide("InterfaceRightBackgroundWidget")

        # Top Center Background
        screen.addPanel("InterfaceTopCenter", u"", u"", True, False, 257, -2, xResolution-(257*2), 48, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceTopCenter", "Panel_Game_HudTC_Style")
        screen.hide("InterfaceTopCenter")

        # Top Left Background
        screen.addPanel("InterfaceTopLeft", u"", u"", True, False, 0, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceTopLeft", "Panel_Game_HudTL_Style")
        screen.hide("InterfaceTopLeft")

        # Top Right Background
        screen.addPanel("InterfaceTopRight", u"", u"", True, False, xResolution - 267, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("InterfaceTopRight", "Panel_Game_HudTR_Style")
        screen.hide("InterfaceTopRight")

        iBtnWidth = 28
        iBtnAdvance = 28
        iBtnY = 27
        iBtnX = 65

        # Turn log Button
        screen.setImageButton("TurnLogButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1)
        screen.setStyle("TurnLogButton", "Button_HUDLog_Style")
        screen.hide("TurnLogButton")

        iBtnX += iBtnAdvance + 10
        screen.setImageButton("VictoryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style")
        screen.hide("VictoryAdvisorButton")

        iBtnX += iBtnAdvance + 3
        screen.setImageButton("InfoAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1)
        screen.setStyle("InfoAdvisorButton", "Button_HUDAdvisorRecord_Style")
        screen.hide("InfoAdvisorButton")

# Mod BUG - 3.17 No Espionage - start
        if GameUtil.isEspionage():
            iBtnX += iBtnAdvance + 3
            screen.setImageButton("EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1)
            screen.setStyle("EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style")
            screen.hide("EspionageAdvisorButton")
# Mod BUG - 3.17 No Espionage - end

        # PAE TradeRouteAdvisor
        iBtnX += iBtnAdvance + 3
        screen.setImageButton("TradeRouteAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_GENERAL, 10000, 1)
        # screen.setImageButton( "TradeRouteAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, -1, 1 )
        screen.setStyle("TradeRouteAdvisorButton", "Button_HUDAdvisorTradeRoute_Style")
        screen.hide("TradeRouteAdvisorButton")
        iBtnX += iBtnAdvance + 3
        screen.setImageButton("TradeRouteAdvisorButton2", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_GENERAL, 10000, 2)
        # screen.setImageButton( "TradeRouteAdvisorButton2", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, -1, 2 )
        screen.setStyle("TradeRouteAdvisorButton2", "Button_HUDAdvisorTradeRoute2_Style")
        screen.hide("TradeRouteAdvisorButton2")

        iBtnX = xResolution - 247

        # Advisor Buttons...
        screen.setImageButton("DomesticAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style")
        screen.hide("DomesticAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("FinanceAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style")
        screen.hide("FinanceAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("CivicsAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style")
        screen.hide("CivicsAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("ForeignAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style")
        screen.hide("ForeignAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("MilitaryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style")
        screen.hide("MilitaryAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("TechAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)
        screen.setStyle("TechAdvisorButton", "Button_HUDAdvisorTechnology_Style")
        screen.hide("TechAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("ReligiousAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style")
        screen.hide("ReligiousAdvisorButton")

        iBtnX += iBtnAdvance
        screen.setImageButton("CorporationAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1)
        screen.setStyle("CorporationAdvisorButton", "Button_HUDAdvisorCorporation_Style")
        screen.hide("CorporationAdvisorButton")

        # Field of View slider
        if bFieldOfView:
            self.setFieldofView_Text(screen)
            iW = 100
            iH = 15
            screen.addSlider(self.szSliderId, self.iX_FoVSlider + 5, self.iY_FoVSlider, iW, iH, self.iField_View - 1, 0, 99, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
            screen.hide(self.szSliderTextId)
            screen.hide(self.szSliderId)

        # City Tabs
        self.cityTabsJumpmarks = [0, 1, 2]
        self.updateCityTabs(screen)
        screen.hide("CityTab0")
        screen.hide("CityTab1")
        screen.hide("CityTab2")

        # Minimap initialization
        screen.setMainInterface(True)

        screen.addPanel("MiniMapPanel", u"", u"", True, False, xResolution - 214, yResolution - 151, 208, 151, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("MiniMapPanel", "Panel_Game_HudMap_Style")
        screen.hide("MiniMapPanel")

        screen.initMinimap(xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1)
        gc.getMap().updateMinimapColor()

        self.createMinimapButtons()

        # Help button (always visible)
        screen.setImageButton("InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1)
        screen.hide("InterfaceHelpButton")

        screen.setImageButton("MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 54, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1)
        screen.hide("MainMenuButton")

        # Globeview buttons
        self.createGlobeviewButtons()

        screen.addMultiListControlGFC("BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD)
        screen.hide("BottomButtonContainer")

        # *********************************************************************************
        # PLOT LIST BUTTONS
        # *********************************************************************************

        for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
            yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
            yPixel = yResolution - 169 + yRow - 3
            xPixel = 315 - 3
            xWidth = self.numPlotListButtons() * 34 + 3
            yHeight = 32 + 3

            szStringPanel = "PlotListPanel" + str(j)
            screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

            for i in xrange(self.numPlotListButtons()):
                k = j * self.numPlotListButtons() + i

                xOffset = i * 34

                szString = "PlotListButton" + str(k)

# Mod BUG - plot list - start
                # szFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
                # szStringPromoFrame  = szString + "PromoFrame"
                # screen.addDDSGFCAt(szStringPromoFrame , szStringPanel, szFileNamePromo, xOffset +  2,  2, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False)
                # screen.hide( szStringPromoFrame  )
# Mod BUG - plot list - end

                screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True)
                screen.hide(szString)

                szStringHealth = szString + "Health"
                screen.addStackedBarGFCAt(szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1)
                screen.hide(szStringHealth)

                szStringIcon = szString + "Icon"
                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
                screen.addDDSGFCAt(szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False)
                screen.hide(szStringIcon)

                # PAE Extra Overlay for Leaders, Heroes and PromotionReadyUnits
                szStringIcon = szString + "Icon2"
                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
                screen.addDDSGFCAt(szStringIcon, szStringPanel, szFileName, xOffset + 22, 0, 14, 14, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False)
                screen.hide(szStringIcon)
                szStringIcon = szString + "Icon3"
                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
                screen.addDDSGFCAt(szStringIcon, szStringPanel, szFileName, xOffset + 4, 16, 14, 14, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False)
                screen.hide(szStringIcon)
                # ------------------

        # End Turn Text
        screen.setLabel("EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.setHitTest("EndTurnText", HitTestTypes.HITTEST_NOHIT)

        # Three states for end turn button...
        screen.setImageButton("EndTurnButton", "", xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1)
        screen.setStyle("EndTurnButton", "Button_HUDEndTurn_Style")
        screen.setEndTurnState("EndTurnButton", "Red")
        screen.hide("EndTurnButton")

        # *********************************************************************************
        # RESEARCH BUTTONS
        # *********************************************************************************

        i = 0
        for i in xrange(gc.getNumTechInfos()):
            szName = "ResearchButton" + str(i)
            screen.setImageButton(szName, gc.getTechInfo(i).getButton(), 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, i, -1)
            screen.hide(szName)

        i = 0
        for i in xrange(gc.getNumReligionInfos()):
            szName = "ReligionButton" + str(i)
            if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
                szButton = gc.getReligionInfo(i).getGenericTechButton()
            else:
                szButton = gc.getReligionInfo(i).getTechButton()
            screen.setImageButton(szName, szButton, 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, gc.getReligionInfo(i).getTechPrereq(), -1)
            screen.hide(szName)

        # *********************************************************************************
        # CITIZEN BUTTONS
        # *********************************************************************************

        # SPECIALIST STACKER        05/02/07      JOHNY
        # szHideCitizenList = []

        # Angry Citizens
        i = 0
        for i in xrange(MAX_ANGRY_CITIZEN_BUTTONS):
            szName = "AngryCitizen" + str(i)
            screen.setImageButton(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (34 * i), yResolution - 241, 30, 30, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1)
            screen.hide(szName)
        g_iAngryCitizensCount = MAX_ANGRY_CITIZEN_BUTTONS

        iCount = 0

        # Increase Specialists...
        i = 0
        iXShiftVal = 0
        iYShiftVal = 0

        for i in xrange(gc.getNumSpecialistInfos()):
            if i > 5:
                iXShiftVal = 110
                iYShiftVal = (i % 5)-1
            else:
                iYShiftVal = i
            if gc.getSpecialistInfo(i).isVisible():
                szName = "IncreaseSpecialist" + str(i)
                screen.setButtonGFC(szName, u"", "", xResolution - (38+iXShiftVal), (yResolution - 258 - (30 * iYShiftVal)), 19, 19, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
                screen.hide(szName)

                iCount = iCount + 1

        iCount = 0

        # Decrease specialists
        i = 0
        iXShiftVal = 0
        iYShiftVal = 0

        for i in xrange(gc.getNumSpecialistInfos()):
            if i > 5:
                iXShiftVal = 110
                iYShiftVal = (i % 5)-1
            else:
                iYShiftVal = i

            if gc.getSpecialistInfo(i).isVisible():
                szName = "DecreaseSpecialist" + str(i)
                screen.setButtonGFC(szName, u"", "", xResolution - (38+iXShiftVal), (yResolution - 243 - (30 * iYShiftVal)), 19, 19, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
                screen.hide(szName)

                iCount = iCount + 1

        iCount = 0

        # Citizen Buttons
        i = 0
        iXShiftVal = 0
        iYShiftVal = 0
        iCount = 0

        for i in xrange(gc.getNumSpecialistInfos()):
            if iCount > 5:
                iXShiftVal = 110
                iYShiftVal = (iCount % 5) - 1
            else:
                iYShiftVal = iCount
            if gc.getSpecialistInfo(i).isVisible():
                szName = "CitizenDisabledButton" + str(i)
                screen.setImageButton(szName, gc.getSpecialistInfo(i).getTexture(), xResolution + 5 - (74+iXShiftVal), (yResolution - 253 - (30 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1)
                screen.enable(szName, False)
                screen.hide(szName)
                for j in xrange(MAX_CITIZEN_BUTTONS):
                    szName = "CitizenButton" + str((i * 100) + j)
                    screen.addCheckBoxGFC(szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution + 5 - (74+iXShiftVal) - (SPECIALIST_STACK_WIDTH * j), (yResolution - 253 - (30 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL)
                    screen.hide(szName)
                iCount = iCount + 1

        screen.addPanel("SpecialistBackground", u"", u"", True, False, xResolution - 243, yResolution-455, 230, 30, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("SpecialistBackground", "Panel_City_Header_Style")
        screen.hide("SpecialistBackground")
        screen.setLabel("SpecialistLabel", "Background", localText.getText("TXT_KEY_LABEL_SPECIALISTS", ()), CvUtil.FONT_CENTER_JUSTIFY, xResolution - 128, yResolution-447, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("SpecialistLabel")

        # SPECIALIST STACKER        END

        # **********************************************************
        # GAME DATA STRINGS
        # **********************************************************

        # szGameDataList = []

        # Original:
        # xCoord = 268 + ((xResolution - 1024) / 2)
        # width = 487
        if xResolution >= 1280:
            xCoord = 405  # 268 + 137 (Left Side + GG Bar)
            RBwidth = xResolution - 880  # (268 * 2) - 137 - 200 / Both Sides - GG Bar - GP Bar
        else:
            xCoord = 268
            RBwidth = xResolution - 538  # (Both Sides: 268 * 2)

        screen.addStackedBarGFC("ResearchBar", xCoord, 2, RBwidth, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1)
        screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED"))
        screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"))
        screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("ResearchBar")

        # PAE (meets BUG) - Great General Bar - start
        if xResolution >= 1280:
            xCoord = 268
            yCoord = 2
        else:
            xCoord = 308
            yCoord = 27
        screen.addStackedBarGFC("GreatGeneralBar", xCoord, yCoord, 130, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
        screen.setStackedBarColors("GreatGeneralBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE"))
        screen.setStackedBarColors("GreatGeneralBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("GreatGeneralBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("GreatGeneralBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("GreatGeneralBar")
# PAE - Great General Bar - end

# PAE (meets BUG) - Great Person Bar - start // >=1440
        if xResolution >= 1280:
            xCoord = xResolution - 470
            yCoord = 2
        else:
            xCoord = xResolution - 510
            yCoord = 27
        screen.addStackedBarGFC("GreatPersonBar", xCoord, yCoord, 200, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1)
        screen.setStackedBarColors("GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
        screen.setStackedBarColors("GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
        screen.setStackedBarColors("GreatPersonBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("GreatPersonBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("GreatPersonBar")
# PAE - Great Person Bar - end

# PAE - Unit Info Bar (Unit ScriptData) Bar
        xCoord = xResolution - 250
        yCoord = 90
        screen.addStackedBarGFC("UnitInfoBar", xCoord, yCoord, 230, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.setStackedBarColors("UnitInfoBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_EMPTY"))
        #screen.setStackedBarColors( "UnitInfoBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
        #screen.setStackedBarColors( "UnitInfoBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
        screen.setStackedBarColors("UnitInfoBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("UnitInfoBar")
        screen.addStackedBarGFC("UnitInfoBar2", xCoord, yCoord + 30, 230, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.setStackedBarColors("UnitInfoBar2", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("UnitInfoBar2")
        # PAE - UnitInfoBar - end
        # PAE Taxes Bar
        screen.addStackedBarGFC("TaxesBar", 5, 25, 55, 25, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.setStackedBarColors("TaxesBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("TaxesBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("TaxesBar")
# ----- BUG - Bars on single line for higher resolution screens - start
        xCoord = 268 + (xResolution - 1440) / 2
        screen.addStackedBarGFC("GreatGeneralBar-w", xCoord, 2, 84, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
        screen.setStackedBarColors("GreatGeneralBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE")) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
        screen.setStackedBarColors("GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("GreatGeneralBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("GreatGeneralBar-w" )

        xCoord += 6 + 84
        screen.addStackedBarGFC("ResearchBar-w", xCoord, 2, 487, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
        screen.setStackedBarColors("ResearchBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
        screen.setStackedBarColors("ResearchBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
        screen.setStackedBarColors("ResearchBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
        screen.setStackedBarColors("ResearchBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
        screen.hide("ResearchBar-w" )

        xCoord += 6 + 487
        screen.addStackedBarGFC("GreatPersonBar-w", xCoord, 2, 320, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
        screen.setStackedBarColors("GreatPersonBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
        screen.setStackedBarColors("GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
        screen.setStackedBarColors("GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
        screen.setStackedBarColors("GreatPersonBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
        screen.hide("GreatPersonBar-w" )
# Mod BUG - Bars on single line for higher resolution screens - end

        # *********************************************************************************
        # SELECTION DATA BUTTONS/STRINGS
        # *********************************************************************************

        # szHideSelectionDataList = []

        screen.addStackedBarGFC("PopulationBar", iCityCenterRow1X, iCityCenterRow1Y-4, xResolution - (iCityCenterRow1X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1)
        screen.setStackedBarColors("PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType())
        screen.setStackedBarColorsAlpha("PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8)
        screen.setStackedBarColors("PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE"))
        screen.setStackedBarColors("PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("PopulationBar")

        screen.addStackedBarGFC("ProductionBar", iCityCenterRow2X, iCityCenterRow2Y-4, xResolution - (iCityCenterRow2X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1)
        screen.setStackedBarColors("ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType())
        screen.setStackedBarColorsAlpha("ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8)
        screen.setStackedBarColors("ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType())
        screen.setStackedBarColors("ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("ProductionBar")

        screen.addStackedBarGFC("GreatPeopleBar", xResolution - 246, yResolution - 180, 194, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1)
        screen.setStackedBarColors("GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
        screen.setStackedBarColors("GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
        screen.setStackedBarColors("GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("GreatPeopleBar")

        screen.addStackedBarGFC("CultureBar", 16, yResolution - 186, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1)
        screen.setStackedBarColors("CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED"))
        screen.setStackedBarColors("CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE"))
        screen.setStackedBarColors("CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.setStackedBarColors("CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
        screen.hide("CultureBar")

        screen.addStackedBarGFC("PAE_RevoltBar", 16, yResolution - 332, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("PAE_RevoltBar")
        screen.addStackedBarGFC("PAE_EmigrationBar", 16, yResolution - 308, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("PAE_EmigrationBar")
        screen.addStackedBarGFC("PAE_SupplyBar", 16, yResolution - 284, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("PAE_SupplyBar")
        screen.addStackedBarGFC("PAE_SlavesBar", 16, yResolution - 260, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("PAE_SlavesBar")
        screen.addStackedBarGFC("PAE_Rebellion2Bar", 16, yResolution - 236, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("PAE_Rebellion2Bar")

        screen.addStackedBarGFC("NationalityBar", 16, yResolution - 210, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1)
        screen.hide("NationalityBar")

        screen.setButtonGFC("CityScrollMinus", u"", "", 274, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
        screen.hide("CityScrollMinus")

        screen.setButtonGFC("CityScrollPlus", u"", "", 288, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
        screen.hide("CityScrollPlus")

        screen.setButtonGFC("PlotListMinus", u"", "", 315 + (xResolution - (iMultiListXL+iMultiListXR) - 68), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
        screen.hide("PlotListMinus")

        screen.setButtonGFC("PlotListPlus", u"", "", 298 + (xResolution - (iMultiListXL+iMultiListXR) - 34), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
        screen.hide("PlotListPlus")

        screen.addPanel("TradeRouteListBackground", u"", u"", True, False, 10, 157, 238, 30, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("TradeRouteListBackground", "Panel_City_Header_Style")
        screen.hide("TradeRouteListBackground")

        screen.setLabel("TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 165, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("TradeRouteListLabel")

# Mod BUG - Raw Yields - start
        nX = 10 + 24
        nY = 157 + 5
        nSize = 24
        nDist = 24
        nGap = 10
        szHighlightButton = ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_HIGHLIGHT").getPath()

        # Trade
        screen.addCheckBoxGFC( "RawYieldsTrade0", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_TRADE").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 0, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsTrade0")

        # Yields
        nX += nDist + nGap
        screen.addCheckBoxGFC( "RawYieldsFood1", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_FOOD").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsFood1")
        nX += nDist
        screen.addCheckBoxGFC( "RawYieldsProduction2", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_PRODUCTION").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 2, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsProduction2")
        nX += nDist
        screen.addCheckBoxGFC( "RawYieldsCommerce3", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_COMMERCE").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 3, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsCommerce3")

        # Tile Selection
        nX += nDist + nGap
        screen.addCheckBoxGFC( "RawYieldsWorkedTiles4", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_WORKED_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 4, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsWorkedTiles4")
        nX += nDist
        screen.addCheckBoxGFC( "RawYieldsCityTiles5", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_CITY_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 5, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsCityTiles5")
        nX += nDist
        screen.addCheckBoxGFC( "RawYieldsOwnedTiles6", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_OWNED_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 6, -1, ButtonStyles.BUTTON_STYLE_LABEL )
        screen.hide("RawYieldsOwnedTiles6")
# Mod BUG - Raw Yields - end

        screen.addPanel("BuildingListBackground", u"", u"", True, False, 10, 287, 238, 30, PanelStyles.PANEL_STYLE_STANDARD)
        screen.setStyle("BuildingListBackground", "Panel_City_Header_Style")
        screen.hide("BuildingListBackground")

        screen.setLabel("BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 295, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        screen.hide("BuildingListLabel")

        # *********************************************************************************
        # UNIT INFO ELEMENTS
        # *********************************************************************************

        i = 0

        szCircleArt = ArtFileMgr.getInterfaceArtInfo("WHITE_CIRCLE_40").getPath()
        for i in xrange(gc.getNumPromotionInfos()):
            szName = "PromotionButton" + str(i)
            # PAE: Widget changed to HELP Promotion, was: PEDIA_JUMP_TO
            screen.addDDSGFC(szName, gc.getPromotionInfo(i).getButton(), 180, yResolution - 18, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, i, -1)
            screen.hide(szName)
# Mod BUG - Stack Promotions - start
            szName = "PromotionButtonCircle" + str(i)
            x, y = self.calculatePromotionButtonPosition(screen, i)
            screen.addDDSGFC(szName, szCircleArt, x + 11, y + 9, 16, 16, WidgetTypes.WIDGET_HELP_PROMOTION, i, -1)
            screen.hide(szName)
# Mod BUG - Stack Promotions - end

        # *********************************************************************************
        # SCORES
        # *********************************************************************************

        screen.addPanel("ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP)
        screen.hide("ScoreBackground")

        for i in xrange(gc.getMAX_PLAYERS()):
            szName = "ScoreText" + str(i)
            screen.setText(szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1)
            screen.hide(szName)

        # This should be a forced redraw screen
        screen.setForcedRedraw(True)

        # This should show the screen immidiately and pass input to the game
        screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

        szHideList = []

        szHideList.append("CreateGroup")
        szHideList.append("DeleteGroup")

        # City Tabs
        for i in xrange(g_NumCityTabTypes):
            szButtonID = "CityTab" + str(i)
            szHideList.append(szButtonID)

        for i in xrange(g_NumHurryInfos):
            szButtonID = "Hurry" + str(i)
            szHideList.append(szButtonID)

        szHideList.append("Hurry0")
        szHideList.append("Hurry1")

        screen.registerHideList(szHideList, len(szHideList), 0)

        return 0

    # Will update the screen (every 250 MS)
    def updateScreen(self):
        global g_szTimeText
        global g_iTimeTextCounter

# Mod BUG - Options - start
        BugOptions.write()
# Mod BUG - Options - end

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        # Find out our resolution
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()
        self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
        self.m_iNumMenuButtons = (xResolution - (iMultiListXL+iMultiListXR) - 18) / 50  # PAE, Ramk 34=>50

        # This should recreate the minimap on load games and returns if already exists -JW
        screen.initMinimap(xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1)

        messageControl = CyMessageControl()

        bShow = False

        # Hide all interface widgets
        #screen.hide( "EndTurnText" )

        if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY:
            if gc.getGame().isPaused():
                # Pause overrides other messages
                acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
                #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                screen.setEndTurnState("EndTurnText", acOutput)
                bShow = True
            elif messageControl.GetFirstBadConnection() != -1:
                # Waiting on a bad connection to resolve
                if messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1:
                    if gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS):
                        acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
                    else:
                        acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
                    #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                    screen.setEndTurnState("EndTurnText", acOutput)
                    bShow = True
                elif messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2:
                    if gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS):
                        acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
                    else:
                        acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
                    #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                    screen.setEndTurnState("EndTurnText", acOutput)
                    bShow = True
            else:
                # Flash select messages if no popups are present
                if CyInterface().shouldDisplayReturn():
                    acOutput = localText.getText("SYSTEM_RETURN", ())
                    #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                    screen.setEndTurnState("EndTurnText", acOutput)
                    bShow = True
                elif CyInterface().shouldDisplayWaitingOthers():
                    acOutput = localText.getText("SYSTEM_WAITING", ())
                    #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                    screen.setEndTurnState("EndTurnText", acOutput)
                    bShow = True
                elif CyInterface().shouldDisplayEndTurn():
                    acOutput = localText.getText("SYSTEM_END_TURN", ())
                    #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                    screen.setEndTurnState("EndTurnText", acOutput)
                    bShow = True
                elif CyInterface().shouldDisplayWaitingYou():
                    acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
                    #screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
                    screen.setEndTurnState("EndTurnText", acOutput)
                    bShow = True

        if bShow:
            screen.showEndTurn("EndTurnText")
            if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isCityScreenUp():
                screen.moveItem("EndTurnText", 0, yResolution - 194, -0.1)
            else:
                screen.moveItem("EndTurnText", 0, yResolution - 86, -0.1)
        else:
            screen.hideEndTurn("EndTurnText")

        self.updateEndTurnButton()

# Mod BUG - NJAGC - start
        global g_bShowTimeTextAlt
        if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL \
           and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START:
           # and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY \
            screen.show("EraText")
            if ClockOpt.isEnabled():
                if ClockOpt.isAlternateTimeText():
                    #global g_iTimeTextCounter (already done above)
                    if CyUserProfile().wasClockJustTurnedOn() or g_iTimeTextCounter <= 0:
                        # reset timer, display primary
                        g_bShowTimeTextAlt = False
                        g_iTimeTextCounter = ClockOpt.getAlternatePeriod() * 1000
                        CyUserProfile().setClockJustTurnedOn(False)
                    else:
                        # countdown timer
                        g_iTimeTextCounter -= 250
                        if g_iTimeTextCounter <= 0:
                            # timer elapsed, toggle between primary and alternate
                            g_iTimeTextCounter = ClockOpt.getAlternatePeriod() * 1000
                            g_bShowTimeTextAlt = not g_bShowTimeTextAlt
                else:
                    g_bShowTimeTextAlt = False

                self.updateTimeText()
                screen.setLabel("TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("TimeText")
            else:
                # screen.hide("EraText")
                self.updateTimeText()
                screen.setLabel("TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("TimeText")
        else:
            screen.hide("TimeText")
            screen.hide("EraText")
# Mod BUG - NJAGC - end
        return 0

    # Will redraw the interface
    def redraw(self):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
# Mod BUG - Field of View - start
        if bFieldOfView:
            #self.setFieldofView(screen, CyInterface().isCityScreenUp())
            self.setFieldofView(screen, False) # K-Mod. (using the default for the city screen is an ok idea, but it doesn't work properly because the screen is drawn before the value is changed.)
# Mod BUG - Field of View - end
        # Check Dirty Bits, see what we need to redraw...
        if CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT):
            # Percent Buttons
            self.updatePercentButtons()
            CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT):
            # Percent Buttons
            self.updateFlag()
            CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT):
            # Miscellaneous buttons (civics screen, etc)
            self.updateMiscButtons()
            CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT):
            # Info Pane Dirty Bit
            # This must come before updatePlotListButtons so that the entity widget appears in front of the stats
            self.updateInfoPaneStrings()
            CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT):
#           BugUtil.debug("dirty PlotListButtons end - %s %s %s", self.bVanCurrentlyShowing, self.bPLECurrentlyShowing, self.bBUGCurrentlyShowing)
            # Plot List Buttons Dirty
            self.updatePlotListButtons()
            CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
#           BugUtil.debug("dirty PlotListButtons start - %s %s %s", self.bVanCurrentlyShowing, self.bPLECurrentlyShowing, self.bBUGCurrentlyShowing)
        if CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT):
            # Selection Buttons Dirty
            self.updateSelectionButtons()
            CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT):
            # Research Buttons Dirty
            self.updateResearchButtons()
            CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT):
            # Citizen Buttons Dirty
            self.updateCitizenButtons()
            CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT):
            # Game Data Strings Dirty
            self.updateGameDataStrings()
            CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT):
            # Help Dirty bit
            self.updateHelpStrings()
            CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT):
            # Selection Data Dirty Bit
            self.updateCityScreen()
            CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
            CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) or CyInterface().checkFlashUpdate():
            # Scores!
            self.updateScoreStrings()
            CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
        if CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT):
            # Globeview and Globelayer buttons
            CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
            self.updateGlobeviewButtons()

        # PAE - River tiles
        if CvEventInterface.getEventManager().bRiverTiles_WaitOnMainInterface:
            CvEventInterface.getEventManager().bRiverTiles_WaitOnMainInterface = False
            CvEventInterface.getEventManager().bRiverTiles_NeedUpdate = True
            # Force update call. (The update event would not be propagated into
            # python as default.)
            CvEventInterface.getEventManager().onUpdate((0.0,))
        # PAE - River tiles end

        return 0

    # K-Mod. There are some special rules for which buttons should be shown and when. I'd rather have all those rules in one place. ie. here.
    def showCommercePercent(self, eCommerce, ePlayer):
        player = gc.getPlayer(ePlayer)
        if not player.isFoundedFirstCity():
            return False

        # Flunky PAE - do show COMMERCE_GOLD except if bHideTaxes
        if self.bHideTaxes and eCommerce == CommerceTypes.COMMERCE_GOLD and not CyInterface().isCityScreenUp():
            return False

        if player.getCommercePercent(eCommerce) > 0:
            return True

        if eCommerce == CommerceTypes.COMMERCE_ESPIONAGE and (gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE) or gc.getTeam(player.getTeam()).getHasMetCivCount(True) == 0):
            return False

        if player.isCommerceFlexible(eCommerce):
            return True
        return False
    # K-Mod end

    # Will update the percent buttons
    def updatePercentButtons(self):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
            szString = "IncreasePercent" + str(iI)
            screen.hide(szString)
            szString = "DecreasePercent" + str(iI)
            screen.hide(szString)
            # Min/Max Sliders - start
            szString = "MaxPercent" + str(iI)
            screen.hide(szString)
            szString = "MinPercent" + str(iI)
            screen.hide(szString)
            # Min/Max Sliders - end

        pHeadSelectedCity = CyInterface().getHeadSelectedCity()

        #if not CyInterface().isCityScreenUp() or pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode():
        if not CyInterface().isCityScreenUp() or pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer(): # K-Mod. (debug mode still doesn't allow us to use the buttons.)
            iCount = 0

            # Taxes
            if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL \
               and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY \
               and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START \
               and (not self.bHideTaxes or CyInterface().isCityScreenUp()):
                for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
                    # Intentional offset...
                    eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES

                    #if gc.getActivePlayer().isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and eCommerce == CommerceTypes.COMMERCE_GOLD):
                    if self.showCommercePercent(eCommerce, gc.getGame().getActivePlayer()): # K-Mod
# Mod BUG - Min/Max Sliders - start
                        bEnable = gc.getActivePlayer().isCommerceFlexible(eCommerce)
                        if MainOpt.isShowMinMaxCommerceButtons() and not CyInterface().isCityScreenUp():
                            iMinMaxAdjustX = 20
                            szString = "MaxPercent" + str(eCommerce)
                            screen.setButtonGFC(szString, u"", "", 70,
                                                52 + (19 * iCount), 20, 20,
                                                WidgetTypes.WIDGET_CHANGE_PERCENT,
                                                eCommerce, 50,
                                                ButtonStyles.BUTTON_STYLE_CITY_PLUS)
                            screen.show(szString)
                            screen.enable(szString, bEnable)
                            szString = "MinPercent" + str(eCommerce)
                            screen.setButtonGFC(szString, u"", "", 130,
                                                52 + (19 * iCount), 20, 20,
                                                WidgetTypes.WIDGET_CHANGE_PERCENT,
                                                eCommerce, -50,
                                                ButtonStyles.BUTTON_STYLE_CITY_MINUS)
                            screen.show(szString)
                            screen.enable(szString, bEnable)
                        else:
                            iMinMaxAdjustX = 0

                        szString = "IncreasePercent" + str(eCommerce)
                        screen.setButtonGFC(szString, u"", "", 70 + iMinMaxAdjustX,
                                            52 + (19 * iCount), 20, 20,
                                            WidgetTypes.WIDGET_CHANGE_PERCENT,
                                            eCommerce,
                                            gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"),
                                            ButtonStyles.BUTTON_STYLE_CITY_PLUS)
                        screen.show(szString)
                        screen.enable(szString, bEnable)
                        szString = "DecreasePercent" + str(eCommerce)
                        screen.setButtonGFC(szString, u"", "",
                                            90 + iMinMaxAdjustX, 52 + (19 * iCount),
                                            20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT,
                                            eCommerce,
                                            -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"),
                                            ButtonStyles.BUTTON_STYLE_CITY_MINUS)
                        screen.show(szString)
                        screen.enable(szString, bEnable)

                        iCount = iCount + 1
                        # moved enabling above
# Mod BUG - Min/Max Sliders - end

        return 0

# Mod BUG - start
    def resetEndTurnObjects(self):
        'Clears the end turn text and hides it and the button.'
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        screen.setEndTurnState("EndTurnText", u"")
        screen.hideEndTurn("EndTurnText")
        screen.hideEndTurn("EndTurnButton")
# Mod BUG - end

    # Will update the end Turn Button
    def updateEndTurnButton(self):
        global g_eEndTurnButtonState
        bShow = False
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        if CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
            g_eEndTurnButtonState = CyInterface().getEndTurnState()
            if g_eEndTurnButtonState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT:
                screen.setEndTurnState("EndTurnButton", u"Red")
                bShow = True
            elif g_eEndTurnButtonState == EndTurnButtonStates.END_TURN_OVER_DARK:
                screen.setEndTurnState("EndTurnButton", u"Red")
                bShow = True
            elif g_eEndTurnButtonState == EndTurnButtonStates.END_TURN_GO:
                screen.setEndTurnState("EndTurnButton", u"Green")
                bShow = True
        if bShow:
            screen.showEndTurn("EndTurnButton")
        else:
            screen.hideEndTurn("EndTurnButton")
        return 0

    # Update the miscellaneous buttons
    def updateMiscButtons(self):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        # xResolution = screen.getXResolution()

# Mod BUG - Great Person Bar - start
        if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL \
            and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY \
            and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START:
            self.updateGreatPersonBar(screen)
# Mod BUG - Great Person Bar - end

        if CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
            screen.show("CivilizationFlag")
            screen.show("InterfaceHelpButton")
            screen.show("MainMenuButton")
        else:
            screen.hide("CivilizationFlag")
            screen.hide("InterfaceHelpButton")
            screen.hide("MainMenuButton")

        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL \
            or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY:
            screen.hide("InterfaceLeftBackgroundWidget")
            screen.hide("InterfaceTopBackgroundWidget")
            screen.hide("InterfaceCenterBackgroundWidget")
            screen.hide("InterfaceRightBackgroundWidget")
            screen.hide("MiniMapPanel")
            screen.hide("InterfaceTopLeft")
            screen.hide("InterfaceTopCenter")
            screen.hide("InterfaceTopRight")
            screen.hide("TurnLogButton")
            screen.hide("EspionageAdvisorButton")
            screen.hide("DomesticAdvisorButton")
            screen.hide("ForeignAdvisorButton")
            screen.hide("TechAdvisorButton")
            screen.hide("CivicsAdvisorButton")
            screen.hide("ReligiousAdvisorButton")
            screen.hide("CorporationAdvisorButton")
            screen.hide("FinanceAdvisorButton")
            screen.hide("MilitaryAdvisorButton")
            screen.hide("VictoryAdvisorButton")
            screen.hide("InfoAdvisorButton")

            # Field of View slider
            screen.hide(self.szSliderTextId)
            screen.hide(self.szSliderId)

            screen.hide("TradeRouteAdvisorButton")
            screen.hide("TradeRouteAdvisorButton2")

        elif CyInterface().isCityScreenUp():
            screen.show("InterfaceLeftBackgroundWidget")
            screen.show("InterfaceTopBackgroundWidget")
            screen.show("InterfaceCenterBackgroundWidget")
            screen.show("InterfaceRightBackgroundWidget")
            screen.show("MiniMapPanel")
            screen.hide("InterfaceTopLeft")
            screen.hide("InterfaceTopCenter")
            screen.hide("InterfaceTopRight")
            screen.hide("TurnLogButton")
            screen.hide("EspionageAdvisorButton")
            screen.hide("DomesticAdvisorButton")
            screen.hide("ForeignAdvisorButton")
            screen.hide("TechAdvisorButton")
            screen.hide("CivicsAdvisorButton")
            screen.hide("ReligiousAdvisorButton")
            screen.hide("CorporationAdvisorButton")
            screen.hide("FinanceAdvisorButton")
            screen.hide("MilitaryAdvisorButton")
            screen.hide("VictoryAdvisorButton")
            screen.hide("InfoAdvisorButton")

            # Field of View slider
            screen.hide(self.szSliderTextId)
            screen.hide(self.szSliderId)

            screen.hide("TradeRouteAdvisorButton")
            screen.hide("TradeRouteAdvisorButton2")

        elif CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
            screen.hide("InterfaceLeftBackgroundWidget")
            screen.show("InterfaceTopBackgroundWidget")
            screen.hide("InterfaceCenterBackgroundWidget")
            screen.hide("InterfaceRightBackgroundWidget")
            screen.hide("MiniMapPanel")
            screen.show("InterfaceTopLeft")
            screen.show("InterfaceTopCenter")
            screen.show("InterfaceTopRight")
            screen.show("TurnLogButton")
            screen.show("EspionageAdvisorButton")
            screen.show("DomesticAdvisorButton")
            screen.show("ForeignAdvisorButton")
            screen.show("TechAdvisorButton")
            screen.show("CivicsAdvisorButton")
            screen.show("ReligiousAdvisorButton")
            screen.show("CorporationAdvisorButton")
            screen.show("FinanceAdvisorButton")
            screen.show("MilitaryAdvisorButton")
            screen.show("VictoryAdvisorButton")
            screen.show("InfoAdvisorButton")
            screen.moveToFront("TurnLogButton")
            screen.moveToFront("EspionageAdvisorButton")
            screen.moveToFront("DomesticAdvisorButton")
            screen.moveToFront("ForeignAdvisorButton")
            screen.moveToFront("TechAdvisorButton")
            screen.moveToFront("CivicsAdvisorButton")
            screen.moveToFront("ReligiousAdvisorButton")
            screen.moveToFront("CorporationAdvisorButton")
            screen.moveToFront("FinanceAdvisorButton")
            screen.moveToFront("MilitaryAdvisorButton")
            screen.moveToFront("VictoryAdvisorButton")
            screen.moveToFront("InfoAdvisorButton")

            # Field of View
            screen.hide(self.szSliderTextId)
            screen.hide(self.szSliderId)

            screen.show("TradeRouteAdvisorButton")
            screen.moveToFront("TradeRouteAdvisorButton")
            screen.show("TradeRouteAdvisorButton2")
            screen.moveToFront("TradeRouteAdvisorButton2")

        elif CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START:
            screen.hide("InterfaceLeftBackgroundWidget")
            screen.hide("InterfaceTopBackgroundWidget")
            screen.hide("InterfaceCenterBackgroundWidget")
            screen.hide("InterfaceRightBackgroundWidget")
            screen.show("MiniMapPanel")
            screen.hide("InterfaceTopLeft")
            screen.hide("InterfaceTopCenter")
            screen.hide("InterfaceTopRight")
            screen.hide("TurnLogButton")
            screen.hide("EspionageAdvisorButton")
            screen.hide("DomesticAdvisorButton")
            screen.hide("ForeignAdvisorButton")
            screen.hide("TechAdvisorButton")
            screen.hide("CivicsAdvisorButton")
            screen.hide("ReligiousAdvisorButton")
            screen.hide("CorporationAdvisorButton")
            screen.hide("FinanceAdvisorButton")
            screen.hide("MilitaryAdvisorButton")
            screen.hide("VictoryAdvisorButton")
            screen.hide("InfoAdvisorButton")

            screen.hide("TradeRouteAdvisorButton")
            screen.hide("TradeRouteAdvisorButton2")

        elif CyEngine().isGlobeviewUp():
            screen.hide("InterfaceLeftBackgroundWidget")
            screen.hide("InterfaceTopBackgroundWidget")
            screen.hide("InterfaceCenterBackgroundWidget")
            screen.show("InterfaceRightBackgroundWidget")
            screen.show("MiniMapPanel")
            screen.show("InterfaceTopLeft")
            screen.show("InterfaceTopCenter")
            screen.show("InterfaceTopRight")
            screen.show("TurnLogButton")
            screen.show("EspionageAdvisorButton")
            screen.show("DomesticAdvisorButton")
            screen.show("ForeignAdvisorButton")
            screen.show("TechAdvisorButton")
            screen.show("CivicsAdvisorButton")
            screen.show("ReligiousAdvisorButton")
            screen.show("CorporationAdvisorButton")
            screen.show("FinanceAdvisorButton")
            screen.show("MilitaryAdvisorButton")
            screen.show("VictoryAdvisorButton")
            screen.show("InfoAdvisorButton")
            screen.moveToFront("TurnLogButton")
            screen.moveToFront("EspionageAdvisorButton")
            screen.moveToFront("DomesticAdvisorButton")
            screen.moveToFront("ForeignAdvisorButton")
            screen.moveToFront("TechAdvisorButton")
            screen.moveToFront("CivicsAdvisorButton")
            screen.moveToFront("ReligiousAdvisorButton")
            screen.moveToFront("CorporationAdvisorButton")
            screen.moveToFront("FinanceAdvisorButton")
            screen.moveToFront("MilitaryAdvisorButton")
            screen.moveToFront("VictoryAdvisorButton")
            screen.moveToFront("InfoAdvisorButton")

            # Field of View slider
            screen.hide(self.szSliderTextId)
            screen.hide(self.szSliderId)

            screen.show("TradeRouteAdvisorButton")
            screen.moveToFront("TradeRouteAdvisorButton")
            screen.show("TradeRouteAdvisorButton2")
            screen.moveToFront("TradeRouteAdvisorButton2")

        else:
            screen.show("InterfaceLeftBackgroundWidget")
            screen.show("InterfaceTopBackgroundWidget")
            screen.show("InterfaceCenterBackgroundWidget")
            screen.show("InterfaceRightBackgroundWidget")
            screen.show("MiniMapPanel")
            screen.show("InterfaceTopLeft")
            screen.show("InterfaceTopCenter")
            screen.show("InterfaceTopRight")
            screen.show("TurnLogButton")
            screen.show("EspionageAdvisorButton")
            screen.show("DomesticAdvisorButton")
            screen.show("ForeignAdvisorButton")
            screen.show("TechAdvisorButton")
            screen.show("CivicsAdvisorButton")
            screen.show("ReligiousAdvisorButton")
            screen.show("CorporationAdvisorButton")
            screen.show("FinanceAdvisorButton")
            screen.show("MilitaryAdvisorButton")
            screen.show("VictoryAdvisorButton")
            screen.show("InfoAdvisorButton")
            screen.moveToFront("TurnLogButton")
            screen.moveToFront("EspionageAdvisorButton")
            screen.moveToFront("DomesticAdvisorButton")
            screen.moveToFront("ForeignAdvisorButton")
            screen.moveToFront("TechAdvisorButton")
            screen.moveToFront("CivicsAdvisorButton")
            screen.moveToFront("ReligiousAdvisorButton")
            screen.moveToFront("CorporationAdvisorButton")
            screen.moveToFront("FinanceAdvisorButton")
            screen.moveToFront("MilitaryAdvisorButton")
            screen.moveToFront("VictoryAdvisorButton")
            screen.moveToFront("InfoAdvisorButton")

            # Field of View slider
            screen.show(self.szSliderTextId)
            screen.show(self.szSliderId)

            screen.show("TradeRouteAdvisorButton")
            screen.moveToFront("TradeRouteAdvisorButton")
            screen.show("TradeRouteAdvisorButton2")
            screen.moveToFront("TradeRouteAdvisorButton2")

        screen.updateMinimapVisibility()

        return 0

    # Update plot List Buttons
    def updatePlotListButtons(self):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        # xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        bHandled = False
        if CyInterface().shouldDisplayUnitModel() \
            and not CyEngine().isGlobeviewUp() \
            and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
            if CyInterface().isCitySelection():
                iOrders = CyInterface().getNumOrdersQueued()

                for i in xrange(iOrders):
                    if not bHandled:
                        eOrderNodeType = CyInterface().getOrderNodeType(i)
                        if eOrderNodeType == OrderTypes.ORDER_TRAIN:
                            screen.addUnitGraphicGFC("InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False)
                            bHandled = True
                            break
                        elif eOrderNodeType == OrderTypes.ORDER_CONSTRUCT:
                            screen.addBuildingGraphicGFC("InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False)
                            bHandled = True
                            break
                        elif eOrderNodeType == OrderTypes.ORDER_CREATE:
                            if gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).isSpaceship():
                                modelType = 0
                                screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 175, yResolution - 138, 123, 132, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
                            else:
                                screen.hide("InterfaceUnitModel")
                            bHandled = True
                            break
                        elif eOrderNodeType == OrderTypes.ORDER_MAINTAIN:
                            screen.hide("InterfaceUnitModel")
                            bHandled = True
                            break

                if not bHandled:
                    screen.hide("InterfaceUnitModel")
                    bHandled = True

                screen.moveToFront("SelectedCityText")

            elif CyInterface().getHeadSelectedUnit():
                screen.addUnitGraphicGFC("InterfaceUnitModel", CyInterface().getHeadSelectedUnit().getUnitType(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False)
                # screen.moveToFront("SelectedUnitText")  # disabled for PAE Unit Detail Promo Icons
            else:
                screen.hide("InterfaceUnitModel")
        else:
            screen.hide("InterfaceUnitModel")

        pPlot = CyInterface().getSelectionPlot()

        for i in xrange(gc.getNumPromotionInfos()):
            szName = "PromotionButton" + str(i)
            screen.moveToFront(szName)

# Mod BUG - Stack Promotions - start
        for i in xrange(gc.getNumPromotionInfos()):
            szName = "PromotionButtonCircle" + str(i)
            screen.moveToFront(szName)
            szName = "PromotionButtonCount" + str(i)
            screen.moveToFront(szName)
# Mod BUG - Stack Promotions - end

        screen.hide("PlotListMinus")
        screen.hide("PlotListPlus")

        BugUtil.debug("updatePlotListButtons_Orig - column %i, offset %i", CyInterface().getPlotListColumn(), CyInterface().getPlotListOffset())

        for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
            #szStringPanel = "PlotListPanel" + str(j)
            # screen.hide(szStringPanel)

            for i in xrange(self.numPlotListButtons()):
                szString = "PlotListButton" + str(j*self.numPlotListButtons()+i)
                screen.hide(szString)

                szStringHealth = szString + "Health"
                screen.hide(szStringHealth)

                szStringIcon = szString + "Icon"
                screen.hide(szStringIcon)

                # PAE Extra Overlay for Leaders, Heroes and PromotionReadyUnits
                szStringIcon = szString + "Icon2"
                screen.hide(szStringIcon)
                szStringIcon = szString + "Icon3"
                screen.hide(szStringIcon)
                # -----------

        if pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and not CyEngine().isGlobeviewUp():
            iVisibleUnits = CyInterface().getNumVisibleUnits()
            iCount = -(CyInterface().getPlotListColumn())
            bLeftArrow = False
            bRightArrow = False
            if CyInterface().isCityScreenUp():
                iMaxRows = 1
                iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
                iCount += iSkipped
            else:
                iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
                iCount += CyInterface().getPlotListOffset()
                iSkipped = 0

            BugUtil.debug("updatePlotListButtons_Orig - iCount(%i), iSkipped(%i)", iCount, iSkipped)

            CyInterface().cacheInterfacePlotUnits(pPlot)
            for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
                pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
                if pLoopUnit:
                    if iCount == 0 and CyInterface().getPlotListColumn() > 0:
                        bLeftArrow = True
                    elif iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1) and (iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1:
                        bRightArrow = True

                    if iCount >= 0 and iCount < self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS():
                        if pLoopUnit.getTeam() != gc.getGame().getActiveTeam() or pLoopUnit.isWaiting():
                            if pLoopUnit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_SENTRY:
                                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_SENTRY").getPath()
                            else:
                                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
                        elif pLoopUnit.canMove():
                            if pLoopUnit.hasMoved():
                                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
                            else:
                                szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
                        else:
                            szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

                        # PAE Extra Overlay for Leaders, Heroes and PromotionReadyUnits
                        szPAELeaderHero = ""
                        szPAEPromotion = ""
                        if pLoopUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")) \
                            and pLoopUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")):
                            szPAELeaderHero = "Art/Interface/Buttons/Unitoverlay/PAE_unitoverlay_hero2.dds"
                        elif pLoopUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
                            szPAELeaderHero = "Art/Interface/Buttons/Unitoverlay/PAE_unitoverlay_star.dds"
                        elif pLoopUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")):
                            szPAELeaderHero = "Art/Interface/Buttons/Unitoverlay/PAE_unitoverlay_hero.dds"
                        if pLoopUnit.getOwner() == gc.getGame().getActivePlayer():
                            if pLoopUnit.isPromotionReady():
                                szPAEPromotion = "Art/Interface/Buttons/Unitoverlay/PAE_unitoverlay_promo.dds"
                            elif CvUtil.getScriptData(pLoopUnit, ["P", "t"]) == "RangPromoUp":
                                szPAEPromotion = "Art/Interface/Buttons/Rang/button_rang_up.dds"
                        # -------------

                        szString = "PlotListButton" + str(iCount)
                        screen.changeImageButton(szString, pLoopUnit.getButton())
                        bEnable = (pLoopUnit.getOwner() == gc.getGame().getActivePlayer())

                        screen.enable(szString, bEnable)

                        if pLoopUnit.IsSelected():
                            screen.setState(szString, True)
                        else:
                            screen.setState(szString, False)
                        screen.show(szString)

                        # place the health bar
                        if pLoopUnit.isFighting():
                            bShowHealth = False
                        elif pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR:
                            bShowHealth = pLoopUnit.canAirAttack()
                        else:
                            bShowHealth = pLoopUnit.canFight()

                        if bShowHealth:
                            szStringHealth = szString + "Health"
                            screen.setBarPercentage(szStringHealth, InfoBarTypes.INFOBAR_STORED, float(pLoopUnit.currHitPoints()) / float(pLoopUnit.maxHitPoints()))
                            if pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3):
                                screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
                            elif pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3):
                                screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
                            else:
                                screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
                            screen.show(szStringHealth)

                        # Adds the overlay first
                        szStringIcon = szString + "Icon"
                        screen.changeDDSGFC(szStringIcon, szFileName)
                        screen.show(szStringIcon)

                        # PAE Extra Overlay for Leaders, Heroes and PromotionReadyUnits
                        if szPAELeaderHero != "":
                            szStringIcon = szString + "Icon2"
                            screen.changeDDSGFC(szStringIcon, szPAELeaderHero)
                            screen.show(szStringIcon)
                        if szPAEPromotion != "":
                            szStringIcon = szString + "Icon3"
                            screen.changeDDSGFC(szStringIcon, szPAEPromotion)
                            screen.show(szStringIcon)
                        # ----------------------

                    iCount = iCount + 1

#           BugUtil.debug("updatePlotListButtons_Orig - vis units(%i), buttons per row(%i), max rows(%i)", iVisibleUnits, self.numPlotListButtons(), iMaxRows)
            if iVisibleUnits > self.numPlotListButtons() * iMaxRows:
#               BugUtil.debug("updatePlotListButtons_Orig - show arrows %s %s", bLeftArrow, bRightArrow)
                screen.enable("PlotListMinus", bLeftArrow)
                screen.show("PlotListMinus")

                screen.enable("PlotListPlus", bRightArrow)
                screen.show("PlotListPlus")

        return 0

    # This will update the flag widget for SP hotseat and dbeugging
    def updateFlag(self):

        if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START:
            screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
            xResolution = screen.getXResolution()
            yResolution = screen.getYResolution()
            screen.addFlagWidgetGFC("CivilizationFlag", xResolution - 288, yResolution - 138, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)

    # Will hide and show the selection buttons and their associated buttons
    def updateSelectionButtons(self):
        global SELECTION_BUTTON_COLUMNS
        global g_pSelectedUnit

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        pHeadSelectedCity = CyInterface().getHeadSelectedCity()
        pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

        global g_NumEmphasizeInfos
        global g_NumCityTabTypes
        global g_NumHurryInfos
        global g_NumUnitClassInfos
        global g_NumBuildingClassInfos
        global g_NumProjectInfos
        global g_NumProcessInfos
        global g_NumActionInfos

        # Find out our resolution
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        # Ramk, Width correction to avoid horizontal scrollbar
        screen.addMultiListControlGFC("BottomButtonContainer", u"",
                                      iMultiListXL, yResolution - 113,
                                      self.m_iNumMenuButtons * 50 + 34,
                                      100, 4, 48, 48,
                                      TableStyles.TABLE_STYLE_STANDARD)

        screen.clearMultiList("BottomButtonContainer")
        screen.hide("BottomButtonContainer")

        # All of the hides...
        self.setMinimapButtonVisibility(False)

        screen.hideList(0)

        for i in xrange(g_NumEmphasizeInfos):
            szButtonID = "Emphasize" + str(i)
            screen.hide(szButtonID)

        # Hurry button show...
        for i in xrange(g_NumHurryInfos):
            szButtonID = "Hurry" + str(i)
            screen.hide(szButtonID)

        # Conscript Button Show
        screen.hide("Conscript")
        #screen.hide( "Liberate" )
        screen.hide("AutomateProduction")
        screen.hide("AutomateCitizens")

        if not CyEngine().isGlobeviewUp() and pHeadSelectedCity:

            self.setMinimapButtonVisibility(True)

            if pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode():

                iBtnX = xResolution - 284
                iBtnY = yResolution - 177
                iBtnW = 64
                iBtnH = 30

                # Liberate button
                #szText = "<font=1>" + localText.getText("TXT_KEY_LIBERATE_CITY", ()) + "</font>"
                #screen.setButtonGFC( "Liberate", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_LIBERATE_CITY, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
                #screen.setStyle( "Liberate", "Button_CityT1_Style" )
                #screen.hide( "Liberate" )

                iBtnSX = xResolution - 284

                iBtnX = iBtnSX
                iBtnY = yResolution - 140
                iBtnW = 64
                iBtnH = 30

                # Conscript button
                szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
                screen.setButtonGFC("Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
                screen.setStyle("Conscript", "Button_CityT1_Style")
                screen.hide("Conscript")

                iBtnY += iBtnH
                iBtnW = 32
                iBtnH = 28

                # Hurry Buttons
                screen.setButtonGFC("Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
                screen.setStyle("Hurry0", "Button_CityC1_Style")
                screen.hide("Hurry0")

                iBtnX += iBtnW

                screen.setButtonGFC("Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
                screen.setStyle("Hurry1", "Button_CityC2_Style")
                screen.hide("Hurry1")

                iBtnX = iBtnSX
                iBtnY += iBtnH

                # Automate Production Button
                screen.addCheckBoxGFC("AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
                screen.setStyle("AutomateProduction", "Button_CityC3_Style")

                iBtnX += iBtnW

                # Automate Citizens Button
                screen.addCheckBoxGFC("AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
                screen.setStyle("AutomateCitizens", "Button_CityC4_Style")

                iBtnY += iBtnH
                iBtnX = iBtnSX

                iBtnW = 22
                iBtnWa = 20
                iBtnH = 24
                iBtnHa = 27

                # Set Emphasize buttons
                i = 0
                szButtonID = "Emphasize" + str(i)
                screen.addCheckBoxGFC(szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
                szStyle = "Button_CityB" + str(i+1) + "_Style"
                screen.setStyle(szButtonID, szStyle)
                screen.hide(szButtonID)

                i += 1
                szButtonID = "Emphasize" + str(i)
                screen.addCheckBoxGFC(szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
                szStyle = "Button_CityB" + str(i+1) + "_Style"
                screen.setStyle(szButtonID, szStyle)
                screen.hide(szButtonID)

                i += 1
                szButtonID = "Emphasize" + str(i)
                screen.addCheckBoxGFC(szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
                szStyle = "Button_CityB" + str(i+1) + "_Style"
                screen.setStyle(szButtonID, szStyle)
                screen.hide(szButtonID)

                iBtnY += iBtnH

                i += 1
                szButtonID = "Emphasize" + str(i)
                screen.addCheckBoxGFC(szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
                szStyle = "Button_CityB" + str(i+1) + "_Style"
                screen.setStyle(szButtonID, szStyle)
                screen.hide(szButtonID)

                i += 1
                szButtonID = "Emphasize" + str(i)
                screen.addCheckBoxGFC(szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
                szStyle = "Button_CityB" + str(i+1) + "_Style"
                screen.setStyle(szButtonID, szStyle)
                screen.hide(szButtonID)

                i += 1
                szButtonID = "Emphasize" + str(i)
                screen.addCheckBoxGFC(szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
                szStyle = "Button_CityB" + str(i+1) + "_Style"
                screen.setStyle(szButtonID, szStyle)
                screen.hide(szButtonID)

                g_pSelectedUnit = 0
                screen.setState("AutomateCitizens", pHeadSelectedCity.isCitizensAutomated())
                screen.setState("AutomateProduction", pHeadSelectedCity.isProductionAutomated())

                for i in xrange(g_NumEmphasizeInfos):
                    szButtonID = "Emphasize" + str(i)
                    screen.show(szButtonID)
                    if pHeadSelectedCity.AI_isEmphasize(i):
                        screen.setState(szButtonID, True)
                    else:
                        screen.setState(szButtonID, False)

                # City Tabs
                for i in xrange(g_NumCityTabTypes):
                    szButtonID = "CityTab" + str(i)
                    screen.show(szButtonID)

                # Hurry button show...
                for i in xrange(g_NumHurryInfos):
                    szButtonID = "Hurry" + str(i)
                    screen.show(szButtonID)
                    screen.enable(szButtonID, pHeadSelectedCity.canHurry(i, False))

                # Conscript Button Show
                screen.show("Conscript")
                if pHeadSelectedCity.canConscript():
                    screen.enable("Conscript", True)
                else:
                    screen.enable("Conscript", False)

                # Liberate Button Show
                #screen.show( "Liberate" )
                # if (-1 != pHeadSelectedCity.getLiberationPlayer()):
                #   screen.enable("Liberate", True)
                # else:
                #   screen.enable("Liberate", False)

                # """ (PAE, Ramk)
                # - Unterteilung in in linken und rechten Block.
                # - Maximale Anzahl von Icons pro Zeile: N.
                # - Normale Aufteilung Links/Rechts: Jeweils N/2. ( links + N%2 )
                # - Links und rechts werden zeilenweise Listen angelegt. Die Zeilen koennen beliebig lang sein.
                # - Beginnt eine Zeile mit 'None', so erzwingt das immer eine neue Zeile fuer das folgende Icon.
                #   (Beispiel: Sprung von Gebaeuden zu Wundern)
                # - Danach werden Icons zeilenweise durchlaufen. Sind zu viele fuer die Maximalbreite angegeben,
                #   werden die ueberschuessigen in die naechste Zeile verschoben.
                # - Falls links die Maximalbreite (N/2) nicht erreicht wird, wird der rechten Seite mehr Platz
                #   eingeraeumt (sofern notwendig).
                # - Am Ende werden die beiden Listen nebeneinander in den "BottomButtonContainer" eingefuegt, wobei
                #   die Freistellen mit Platzhaltern gefuellt werden.
                # """

                #numIcons = 23
                numIcons = max(2, self.m_iNumMenuButtons) - 1
                numIconsRight = numIcons/2
                numIconsLeft = numIcons - numIconsRight
                self.iconsLeft = [[]]
                self.iconsRight = [[]]
                rowLeft = 0
                rowRight = 0
                cityTab = 0

                iCount = 0
                iRow = 0
                bFound = False

                # """# Debug, comment normal setText for this widget out, if you uncomment this...
                # szBuffer = u"<font=4>"
                # szBuffer += u"%s: %d %d %d" %("Test", numIcons, numIconsLeft, numIconsRight)
                # szBuffer += u"</font>"
                # screen.setText( "CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
                # """

                # Units to construct
                for i in xrange(g_NumUnitClassInfos):
                    # PAE - Abbruch bei unbaubare Einheiten
                    if i == gc.getInfoTypeForString("UNITCLASS_PROPHET"):
                        break

                    eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)

                    # PAE - Zeilenumbruch bei bestimmten Einheitenklassen (unitcombattypes)
                    lBreakLineUnits = [
                        gc.getInfoTypeForString("UNIT_WARRIOR"),
                        gc.getInfoTypeForString("UNIT_LIGHT_ARCHER"),
                        gc.getInfoTypeForString("UNIT_LIGHT_CHARIOT"),
                        gc.getInfoTypeForString("UNIT_INQUISITOR"),
                        gc.getInfoTypeForString("UNITCLASS_ARCHER_KRETA")
                    ]
                    if iCount > 6 and (eLoopUnit in lBreakLineUnits or i == gc.getInfoTypeForString("UNITCLASS_SPECIAL1")):
                        iCount = 0
                        if bFound:
                            iRow = iRow + 1
                            rowLeft += 1
                            self.iconsLeft.append([])
                        bFound = False

                    # Ramks city widgets
                    if pHeadSelectedCity.canTrain(eLoopUnit, False, True):

                        # Manufaktur Einheiten: Doppelte Einheitenproduktion
                        bManufaktur = False
                        iUnitCombatType = gc.getUnitInfo(eLoopUnit).getUnitCombatType()
                        if iUnitCombatType in L.DManufakturen:
                            iBuilding = L.DManufakturen[iUnitCombatType]
                            bManufaktur = pHeadSelectedCity.isHasBuilding(iBuilding)

                        szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
                        self.iconsLeft[rowLeft].append(([szButton, WidgetTypes.WIDGET_TRAIN, i, -1, False], pHeadSelectedCity.canTrain(eLoopUnit, False, False), cityTab, bManufaktur))
                        iCount = iCount + 1
                        bFound = True

                iCount = 0
                if bFound:
                    iRow = iRow + 1
                bFound = False
                cityTab += 1

                # Buildings to construct
                for i in xrange(g_NumBuildingClassInfos):
                    if not isLimitedWonderClass(i):
                        eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
                        if pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False):
                            szButton = gc.getBuildingInfo(eLoopBuilding).getButton()
                            self.iconsRight[rowRight].append(([szButton, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False], pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False), cityTab, False))
                            iCount = iCount + 1
                            bFound = True

                iCount = 0
                if bFound:
                    iRow = iRow + 1
                    rowRight += 1
                    self.iconsRight.append([None])
                bFound = False
                cityTab += 1

                # Wonders to construct
                i = 0
                for i in xrange(g_NumBuildingClassInfos):
                    if isLimitedWonderClass(i):
                        eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
                        if pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False):
                            szButton = gc.getBuildingInfo(eLoopBuilding).getButton()
                            self.iconsRight[rowRight].append(([szButton, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False], pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False), cityTab, False))
                            iCount = iCount + 1
                            bFound = True

                iCount = 0
                if bFound:
                    iRow = iRow + 1
                bFound = False

                # Projects
                for i in xrange(g_NumProjectInfos):
                    if pHeadSelectedCity.canCreate(i, False, True):
                        szButton = gc.getProjectInfo(i).getButton()
                        self.iconsRight[rowRight].append(([szButton, WidgetTypes.WIDGET_CREATE, i, -1, False], pHeadSelectedCity.canCreate(i, False, False), cityTab, False))
                        iCount = iCount + 1
                        bFound = True

                # Processes
                for i in xrange(g_NumProcessInfos):
                    if pHeadSelectedCity.canMaintain(i, False):
                        szButton = gc.getProcessInfo(i).getButton()
                        self.iconsRight[rowRight].append(([szButton, WidgetTypes.WIDGET_MAINTAIN, i, -1, False], True, cityTab, False))
                        iCount = iCount + 1
                        bFound = True

                if numIcons > 15:
                    self.sortButtons(self.iconsLeft, numIconsLeft)
                    # Flunky: keep the partition at 50/50
                    # [numIconsLeft, numIconsRight] = self.optimalPartition(numIconsLeft, numIconsRight, self.iconsLeft, self.iconsRight)
                    self.sortButtons(self.iconsRight, numIconsRight)
                    self.insertButtons(self.iconsLeft, self.iconsRight, numIconsLeft+1, numIcons+1)
                    self.cityTabsJumpmarks = [0, 0, self.findCityTabRow(self.iconsRight, 2)]
                else:
                    self.sortButtons(self.iconsLeft, numIcons+1)
                    self.sortButtons(self.iconsRight, numIcons+1)
                    self.insertButtons(self.iconsLeft+self.iconsRight, [], 0, numIcons+1)
                    # Find indizes of first building row and first wonder row
                    rowBuildings = len(self.iconsLeft)
                    rowWonders = rowBuildings + self.findCityTabRow(self.iconsRight, 2)
                    self.cityTabsJumpmarks = [0, rowBuildings, rowWonders]
                screen.show("BottomButtonContainer")
                screen.selectMultiList("BottomButtonContainer", CyInterface().getCityTabSelectionRow())

        elif (not CyEngine().isGlobeviewUp()
              and pHeadSelectedUnit
              and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL
              and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

            self.setMinimapButtonVisibility(True)
            if CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION:
                if (pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer()
                    and g_pSelectedUnit != pHeadSelectedUnit):

                    g_pSelectedUnit = pHeadSelectedUnit
                    iCount = 0
                    # Limes
                    actions = CyInterface().getActionsToShow()
                    for i in actions:

                        if (not gc.getActionInfo(i).getMissionType() == MissionTypes.MISSION_BUILD
                            or not gc.getActionInfo(i).getMissionData() in L.LBuildLimes):

                            screen.appendMultiListButton("BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False)
                            screen.show("BottomButtonContainer")

                            if not CyInterface().canHandleAction(i, False):
                                screen.disableMultiListButton("BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton())

                            # funkt leider nicht
                            # Flunky: funktioniert doch?
                            # TODO grey out button if no opponent in xrange
                            if (gc.getActionInfo(i).getMissionType() == MissionTypes.MISSION_RANGE_ATTACK
                                and not pHeadSelectedUnit.canMove()):
                                screen.disableMultiListButton("BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton())

                            if pHeadSelectedUnit.isActionRecommended(i):  # or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):
                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                            else:
                                screen.enableMultiListPulse("BottomButtonContainer", False, 0, iCount)

                            # PAE V: Aussenhandelsposten fuer HI nur ausserhalb der eigenen Kulturgrenzen baubar
                            # if gc.getActionInfo(i).getMissionData() == gc.getInfoTypeForString("BUILD_HANDELSPOSTEN"):
                            #  if g_pSelectedUnit.plot().getOwner() == g_pSelectedUnit.getOwner():
                            #    screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )

                            iCount = iCount + 1

                    if CyInterface().canCreateGroup():
                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False)
                        screen.show("BottomButtonContainer")
                        iCount = iCount + 1

                    if CyInterface().canDeleteGroup():
                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False)
                        screen.show("BottomButtonContainer")
                        iCount = iCount + 1

                    ############################################ Unit Buttons #############################################
                    pUnit = g_pSelectedUnit
                    iUnitType = pUnit.getUnitType()
                    iUnitOwner = pUnit.getOwner()
                    pUnitOwner = gc.getPlayer(iUnitOwner)
                    pTeam = gc.getTeam(pUnitOwner.getTeam())

                    # isTurnActive wohl wegen PBEM
                    if pUnitOwner.isTurnActive() or CyGame().isNetworkMultiPlayer():
                        bCapital = False
                        bCity = False
                        if g_pSelectedUnit.plot().isCity():
                            bCity = True
                            pCity = g_pSelectedUnit.plot().getPlotCity()
                            if pCity.getOwner() == iUnitOwner:
                                bCapital = (pCity.isCapital()
                                            or pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST"))
                                            or pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PRAEFECTUR")))
                        # ----------
                        # Missionar in eine eigene heidnische Stadt schicken
                        # if pUnit.getUnitAIType() == gc.getInfoTypeForString("UNITAI_MISSIONARY"):
                        #   screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_spread_rel.dds", 0, WidgetTypes.WIDGET_GENERAL, 731, 731, False )
                        #   screen.show( "BottomButtonContainer" )
                        #   iCount = iCount + 1

                        # ----------
                        # Haendler in die naechste fremde Stadt schicken
                        # if pUnit.getUnitAIType() == gc.getInfoTypeForString("UNITAI_MERCHANT") or iUnitType == gc.getInfoTypeForString("UNIT_GAULOS") or iUnitType == gc.getInfoTypeForString("UNIT_CARVEL_TRADE"):
                        #   if iUnitType != gc.getInfoTypeForString("UNIT_GREAT_SPY"):
                        #     screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_merchant.dds", 0, WidgetTypes.WIDGET_GENERAL, 732, 732, False )
                        #     screen.show( "BottomButtonContainer" )
                        #     iCount = iCount + 1

                        # ----------
                        # Inquisitor
                        if bCity and iUnitType == gc.getInfoTypeForString("UNIT_INQUISITOR"):
                            if PAE_Unit.InquisitionPossible(pCity, iUnitOwner):
                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GODS_PERSICUTION").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 665, 665, False)
                                screen.show("BottomButtonContainer")
                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                iCount = iCount + 1
                                return 0

                        # --------------------
                        # Hunter / Jaeger -> INFO BUTTON ob Cities in Reichweite sind
                        elif iUnitType == gc.getInfoTypeForString("UNIT_HUNTER"):
                            bOK = False
                            (loopCity, pIter) = pUnitOwner.firstCity(False)
                            while loopCity:
                                if PAE_Unit.huntingDistance(loopCity.plot(), pUnit.plot()):
                                    bOK = True
                                    break
                                (loopCity, pIter) = pUnitOwner.nextCity(pIter, False)

                            if bCity:
                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 7, False)
                            elif bOK:
                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_i_jagd_ok.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 7, False)
                            else:
                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_i_jagd_no.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 7, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1

                        # --------------------
                        # Horse/Pferd (Button per XML) (not in city)
                        elif iUnitType == gc.getInfoTypeForString("UNIT_HORSE"):
                            pPlot = pUnit.plot()
                            if pPlot.getOwner() == iUnitOwner:
                                # Check plot
                                eBonus = gc.getInfoTypeForString("BONUS_HORSE")
                                if PAE_Cultivation.isBonusCultivationChance(iUnitOwner, pPlot, eBonus, False, None):
                                    screen.appendMultiListButton("BottomButtonContainer", ",Art/Interface/Buttons/Buildings/Barracks.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,7,1", 0, WidgetTypes.WIDGET_GENERAL, 721, 14, False)
                                    screen.show("BottomButtonContainer")
                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                    iCount = iCount + 1
                                return 0
                        # --------------------
                        # Camel/Kamel (not in city)
                        elif iUnitType == gc.getInfoTypeForString("UNIT_CAMEL"):
                            pPlot = pUnit.plot()
                            if pPlot.getOwner() == iUnitOwner:
                                # Check plot
                                eBonus = gc.getInfoTypeForString("BONUS_CAMEL")
                                if PAE_Cultivation.isBonusCultivationChance(iUnitOwner, pPlot, eBonus, False, None):
                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Buildings/button_camel_stable.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 4, False)
                                    screen.show("BottomButtonContainer")
                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                    iCount = iCount + 1
                                return 0
                        """
                        # Elefant
                        elif iUnitType == gc.getInfoTypeForString("UNIT_ELEFANT"):
                            # in city
                            if bCity and pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_KOLONIE")):
                              if not pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE")):
                                if pCity.getOwner() == iUnitOwner or gc.getTeam(pCity.getTeam()).isVassal(gc.getPlayer(iUnitOwner).getTeam()):
                                  # Check plots (Klima / climate)
                                  bOK = False
                                  eBonus = gc.getInfoTypeForString("BONUS_IVORY")

                                  lPlots = PAE_Cultivation.getCityCultivatedPlots(pCity, eBonus)
                                  if len(lPlots):
                                    for p in lPlots:
                                      if p.getBonusType(-1) == eBonus:
                                        iImp = p.getImprovementType()
                                        if iImp != -1 and gc.getImprovementInfo(iImp).isImprovementBonusMakesValid(eBonus):
                                          bOK = True
                                  if not bOK and PAE_Cultivation._bonusIsCultivatableFromCity(iUnitOwner, pCity, eBonus, False):
                                     if len(lPlots) == 0: bOK = True

                                  if bOK:
                                      screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Builds/button_elefantenstall.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 1, False)
                                      screen.show("BottomButtonContainer")
                                      screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                      iCount = iCount + 1
                                  else:
                                      screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_elestall_grau.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 2, False)
                                      screen.show("BottomButtonContainer")
                                      iCount = iCount + 1
                                  return
                            # not in city
                            #else:
                            #    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_elestall_grau.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 3, False)
                            #    screen.show("BottomButtonContainer")
                            #    iCount = iCount + 1
                            #    return
                        """
                        # ---- End ------

                        # ----------
                        # PAE - Cultist cannot spread cult due to civic (749:1) => Show INFO Button ! (nocult, keinKult mit Kultist)
                        #if bCity:
                        #    Cultists = [
                        #        gc.getInfoTypeForString("UNIT_EXECUTIVE_1"),
                        #        gc.getInfoTypeForString("UNIT_EXECUTIVE_2"),
                        #        gc.getInfoTypeForString("UNIT_EXECUTIVE_3")
                        #    ]
                        #    if iUnitType in Cultists:
                        #        if pUnitOwner.isCivic(gc.getInfoTypeForString("CIVIC_ANIMISM")):
                        #            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_cult_grey.dds", 0, WidgetTypes.WIDGET_GENERAL, 749, 1, False)
                        #            screen.show("BottomButtonContainer")
                        #            iCount = iCount + 1

                        # --------------------

                        # Veteran -> Eliteunit (netMessage 705) - Belobigung
                        # Auch in GameUtils fuer die KI aendern !
                        if pUnit.canMove() and pUnit.getDomainType() == DomainTypes.DOMAIN_LAND:
                            if iUnitType not in L.LNoRankUnits:
                                iCivType = pUnit.getCivilizationType()

                                # PAE 6.5 Katapult -> Feuerkatapult
                                if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_ACCURACY3")):
                                    if pUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_CATAPULT"):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_fire_catapult.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_FIRE_CATAPULT"), False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1

                                # PAE 6.9 GREEKS and Perioikian hoplite (SPARTA)
                                if iCivType in L.LGreeks or iCivType == gc.getInfoTypeForString("CIVILIZATION_SPARTA"):
                                    # experienced hoplite -> Kalos Kagathos (special hoplite)
                                    if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2")):
                                        if iUnitType == gc.getInfoTypeForString("UNIT_HOPLIT") or iUnitType == gc.getInfoTypeForString("UNIT_HOPLIT_SPARTA"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_hoplit_kalos.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                # Veterans
                                if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT4")):

                                # Rome: Roman praetorians ->  Cohors Praetoria | Cohors Urbana | Equites LH
                                # Sollte ueber XML gehen. Auch wenn iCost -1
                                # if iUnitType == gc.getInfoTypeForString("UNIT_PRAETORIAN"):
                                #    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PRINCIPAT")):
                                #      screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Units/button_praetorian2.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_PRAETORIAN2"), False )
                                #      screen.show( "BottomButtonContainer" )
                                #      iCount = iCount + 1
                                #    elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_FEUERWEHR")):
                                #      screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Units/button_cohortes_urbanae.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"), False )
                                #      screen.show( "BottomButtonContainer" )
                                #      iCount = iCount + 1
                                #    elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_LORICA_SEGMENTATA")):
                                #      screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Units/button_cohors_equitata.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"), False )
                                #      screen.show( "BottomButtonContainer" )
                                #      iCount = iCount + 1

                                    # Eliteeinheiten
                                    if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT5")):

                                        if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
                                            # Elite Cohors Equitata -> Equites Singulares Augusti
                                            if iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_praetorian2_horse.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Elite Palatini or Clibanari or Cataphracti -> Scholae
                                            elif iUnitType in [gc.getInfoTypeForString("UNIT_ROME_PALATINI"),
                                                               gc.getInfoTypeForString("UNIT_CLIBANARII_ROME"),
                                                               gc.getInfoTypeForString("UNIT_CATAPHRACT_ROME")]:
                                                #if gc.getCivilizationInfo(pUnitOwner.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ROME_SCHOLAE")) < 3:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_scholae.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                        else:
                                            # Elite Limitanei -> Imperial Guard
                                            if iUnitType == gc.getInfoTypeForString("UNIT_ROME_LIMITANEI"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_limit_garde.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ROME_LIMITANEI_GARDE"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Elite Comitatenses -> Palatini
                                            elif iUnitType in [gc.getInfoTypeForString("UNIT_ROME_COMITATENSES"),
                                                               gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2")]:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_palatini.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ROME_PALATINI"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Elite Cohorte praetoriae + Cohors urbana -> Praetorian Garde
                                            elif iUnitType in [gc.getInfoTypeForString("UNIT_PRAETORIAN"),
                                                               gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
                                                               gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"),
                                                               gc.getInfoTypeForString("UNIT_LEGION_EVOCAT")]:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_praetorian3.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_PRAETORIAN3"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Elite Assyrer und Babylon: Quradu
                                            elif iCivType in [gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
                                                              gc.getInfoTypeForString("CIVILIZATION_BABYLON")]:
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BUERGERSOLDATEN")):
                                                    if (iUnitType != gc.getInfoTypeForString("UNIT_ASSUR_RANG2")
                                                        and iUnitType != gc.getInfoTypeForString("UNIT_ASSUR_RANG3")
                                                        and gc.getUnitInfo(iUnitType).getCombat() < 11):
                                                        screen.appendMultiListButton("BottomButtonContainer", gc.getUnitInfo(gc.getInfoTypeForString("UNIT_ELITE_ASSUR")).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ELITE_ASSUR"), False)
                                                        screen.show("BottomButtonContainer")
                                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                        iCount = iCount + 1
                                            # Elite Sumerer: Gardu
                                            elif iCivType == gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BUERGERSOLDATEN")):
                                                    if gc.getUnitInfo(iUnitType).getCombat() < 11:
                                                        screen.appendMultiListButton("BottomButtonContainer", gc.getUnitInfo(gc.getInfoTypeForString("UNIT_ELITE_SUMER")).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ELITE_SUMER"), False)
                                                        screen.show("BottomButtonContainer")
                                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                        iCount = iCount + 1
                                            # Stammesfürst
                                            elif iCivType in L.LNorthern:
                                                # Stammesfuerst
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KETTENPANZER")):
                                                    # nur Nahkaempfer
                                                    if pUnit.getUnitCombatType() in L.LMeleeCombats:
                                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_stammesfuerst.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), False)
                                                        screen.show("BottomButtonContainer")
                                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                        iCount = iCount + 1

                                    # weiter mit Veteran

                                    # ROME
                                    if iCivType in [gc.getInfoTypeForString("CIVILIZATION_ROME"),
                                                    gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS")]:

                                        if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER"):

                                            # Sagittarii (Reflex) -> Arquites
                                            if iUnitType == gc.getInfoTypeForString("UNIT_ARCHER_ROME"):
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_LORICA_SEGMENTATA")):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_arquites_legionis.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ARCHER_LEGION"), False)
                                                    screen.show("BottomButtonContainer")
                                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                    iCount = iCount + 1
                                            # Arquites -> Equites Sagittarii (Horse Archer)
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_ARCHER_LEGION"):
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HORSE_ARCHER")):
                                                    screen.appendMultiListButton("BottomButtonContainer", ",Art/Interface/Buttons/Units/HorseArcher.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,1,11", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HORSE_ARCHER_ROMAN"), False)
                                                    screen.show("BottomButtonContainer")
                                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                    iCount = iCount + 1

                                        else:

                                            # Legion or Legion 2 -> Praetorians
                                            if iUnitType in [gc.getInfoTypeForString("UNIT_LEGION"),
                                                                gc.getInfoTypeForString("UNIT_LEGION2")]:
                                                # obsolete with Marching Army/Border Army
                                                if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_GRENZHEER")):
                                                    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BERUFSSOLDATEN")):
                                                        # Rang: Immunes
                                                        if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_3")):
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_praetorian.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_PRAETORIAN"), False)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1

                                            # Triari -> Praetorians
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_TRIARII") and pTeam.isHasTech(gc.getInfoTypeForString("TECH_BERUFSSOLDATEN")):
                                                # obsolete with Marching/Border Army
                                                if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_GRENZHEER")):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_praetorian.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_PRAETORIAN"), False)
                                                    screen.show("BottomButtonContainer")
                                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                    iCount = iCount + 1
                                            # Principes, Hastati, Pilumni -> Triarii
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_PRINCIPES") or iUnitType == gc.getInfoTypeForString("UNIT_HASTATI") or iUnitType == gc.getInfoTypeForString("UNIT_PILUMNI"):
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_EISENWAFFEN")):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_triarii2.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_TRIARII"), False)
                                                    screen.show("BottomButtonContainer")
                                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                    iCount = iCount + 1
                                            # Hasta Warrior -> Celeres
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_HASTA"):
                                                # if pUnit.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_celeres.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_CELERES"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                    # GREEKS
                                    elif iCivType in L.LGreeks:
                                        # Elite Reiter -> Hipparchos
                                        if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
                                            if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT5")):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_hippeus4.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                        # Reflex -> Elite
                                        elif iUnitType == gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_archer_greek.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # SPARTA
                                    elif iCivType == gc.getInfoTypeForString("CIVILIZATION_SPARTA"):
                                        if iUnitType == gc.getInfoTypeForString("UNIT_SPEARMAN") or iUnitType == gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_spartan1.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_SPARTA_1"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # PERSIA
                                    elif iCivType == gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
                                        # Garde
                                        if iUnitType == gc.getInfoTypeForString("UNIT_APFELTRAEGER"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_immortalguard.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # MACEDONIA
                                    elif iCivType == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):

                                        # Berittene
                                        if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
                                            # Prodomoi -> Hetairoi
                                            if iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON"):
                                                screen.appendMultiListButton("BottomButtonContainer", ",Art/Interface/Buttons/Units/Keshik.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,2,11", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Hetairoi -> Ilearchos
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_companion2.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Ilearchos -> Ile basilikoi
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_companion4.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Ile basilikoi -> Hipparchos
                                            elif iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_hippeus4.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                        # Ende Berittene

                                        #  Lochagos (Pezhetairoi) -> Hetairoi
                                        #elif iUnitType == gc.getInfoTypeForString("UNIT_PEZHETAIROI3"):
                                        #  screen.appendMultiListButton("BottomButtonContainer", ",Art/Interface/Buttons/Units/Keshik.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,2,11", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"), False)
                                        #  screen.show("BottomButtonContainer")
                                        #  screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        #  iCount = iCount + 1
                                        #  Hypaspist -> Argyraspidai (Silberschild)
                                        elif iUnitType == gc.getInfoTypeForString("UNIT_HYPASPIST"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_hypa2.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HYPASPIST2"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1
                                        #  Argyraspidai -> Royal Hypaspist
                                        elif iUnitType == gc.getInfoTypeForString("UNIT_HYPASPIST2"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_hypa3.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HYPASPIST3"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1
                                        # Reflex -> Elite
                                        elif iUnitType == gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_archer_greek.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # EGYPT
                                    elif iCivType == gc.getInfoTypeForString("CIVILIZATION_EGYPT") or iCivType == gc.getInfoTypeForString("CIVILIZATION_NUBIA"):
                                        if iUnitType not in L.LNoRankUnits:
                                            #  Pharaonengarde oder kuschitischer Fuerst
                                            #if gc.getCivilizationInfo(pUnitOwner.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ELITE1")) < 3:
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG4")):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_egypt_horus.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                    # Schildtraeger
                                    if iUnitType == gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"):

                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KETTENPANZER")):

                                            if iCivType == gc.getInfoTypeForString("CIVILIZATION_DAKER"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_dacianchief.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_FUERST_DAKER"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            elif iCivType == gc.getInfoTypeForString("CIVILIZATION_ISRAEL"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_israel_maccaber.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_MACCABEE"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                    # Axeman
                                    elif iUnitType == gc.getInfoTypeForString("UNIT_AXEMAN2"):
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_EISENWAFFEN")):
                                            if iCivType == gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_axeman.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                    # Spearman
                                    elif iUnitType == gc.getInfoTypeForString("UNIT_SPEARMAN"):

                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_LINOTHORAX")):
                                            # India
                                            if iCivType == gc.getInfoTypeForString("CIVILIZATION_INDIA"):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_inder_radscha.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_RADSCHA"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Greeks
                                            elif iCivType in L.LGreeks:
                                                # Spearman -> Hoplit
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_hoplit.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HOPLIT"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                                            # Karthago
                                            elif iCivType == gc.getInfoTypeForString("CIVILIZATION_CARTHAGE") or iCivType == gc.getInfoTypeForString("CIVILIZATION_PHON"):
                                                screen.appendMultiListButton("BottomButtonContainer", gc.getUnitInfo(gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT")).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                        # Harier
                                        if iCivType == gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_EISENWAFFEN")):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_harii.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_GERMAN_HARIER"), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                    # Swordsman
                                    elif iUnitType == gc.getInfoTypeForString("UNIT_SWORDSMAN"):
                                        if iCivType == gc.getInfoTypeForString("CIVILIZATION_INDIA"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_unit_nayar.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_INDIAN_NAYAR"), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # Steppenreiter -> Geissel Gottes
                                    elif iUnitType == gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_heavy_horseman.dds", 0, WidgetTypes.WIDGET_GENERAL, 705, gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN_HUN"), False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1

                                    # Allgemein Veteran -> Reservist
                                    if bCity:
                                        if pCity.getOwner() == pUnit.getOwner():
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_RESERVISTEN")):
                                                screen.appendMultiListButton("BottomButtonContainer", ",Art/Interface/MainScreen/CityScreen/Great_Engineer.dds,Art/Interface/Buttons/Warlords_Atlas_2.dds,7,6", 0, WidgetTypes.WIDGET_GENERAL, 724, 724, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1

                                # if Veteran/Routiniert -> Elite / Reservist -----------------------

                                # Legionaries koennen in Kastellen oder MilAks ausgebildet werden (Auxiliari nicht)
                                if pUnit.getUnitType() not in L.LUnitAuxiliar:
                                    if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_1")) and not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_11")) or \
                                       pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1")) and not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_10")) :

                                        iBuilding1 = gc.getInfoTypeForString("BUILDING_MILITARY_ACADEMY")
                                        iBuilding2 = gc.getInfoTypeForString("BUILDING_BARRACKS")
                                        if bCity and pUnitOwner.getGold() > 50 and pCity.getOwner() == pUnit.getOwner() and (pCity.isHasBuilding(iBuilding1) or pCity.isHasBuilding(iBuilding2)):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_kastell.dds", 0, WidgetTypes.WIDGET_GENERAL, 756, 0, True)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                        # end if can move (Routiniert, Veteran, Elite) and Domain Land

                        # Unit Rang Promos
                        if pUnit.canMove() and CvUtil.getScriptData(pUnit, ["P", "t"]) == "RangPromoUp":
                            # Belobigung fuer die meisten Einheiten immer und ueberall erlauben
                            if pUnit.getUnitType() not in L.LCapitalPromoUpUnits:
                                bCapital = True
                            if pUnitOwner.getGold() < 50:
                                bCapital = False
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Rang/button_rang_up.dds", 0, WidgetTypes.WIDGET_GENERAL, 751, pUnit.getOwner(), bCapital)
                            screen.show("BottomButtonContainer")
                            if bCapital:
                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                            iCount = iCount + 1

                        # --------------------
                        # BEGIN Horse <-> Unit
                        if pUnit.canMove():
                            bButtonDown = False
                            bButtonUp = False
                            bSearchPlot = False

                            # Horse -> Unit
                            if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
                                if iUnitType in L.DHorseDownMap:
                                    bButtonDown = True
                            elif iUnitType == gc.getInfoTypeForString("UNIT_WAR_CHARIOT"):
                                if pUnit.getCivilizationType() in L.LCivGermanen:
                                    if pUnitOwner.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_SPECIAL2")) + pUnitOwner.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_WAR_CHARIOT")) < 6:
                                        bButtonDown = True

                            # Unit -> Horse
                            elif iUnitType in L.LUnitAuxiliar or iUnitType in L.DHorseUpMap:
                                if iUnitType == gc.getInfoTypeForString("UNIT_SCOUT") or iUnitType == gc.getInfoTypeForString("UNIT_SCOUT_GREEK"):
                                    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HORSEBACK_RIDING")):
                                        bSearchPlot = True
                                elif iUnitType == gc.getInfoTypeForString("UNIT_STAMMESFUERST"):
                                    if pUnit.getCivilizationType() in L.LCivGermanen:
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_ARISTOKRATIE")):
                                            if pUnitOwner.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_SPECIAL2")) + pUnitOwner.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_WAR_CHARIOT")) < 6:
                                                bSearchPlot = True
                                elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_HUFEISEN")):
                                    bSearchPlot = True

                                # Pferd suchen
                                if bSearchPlot:
                                    pPlot = g_pSelectedUnit.plot()
                                    UnitHorse = gc.getInfoTypeForString("UNIT_HORSE")
                                    for iUnit in xrange(pPlot.getNumUnits()):
                                        if pPlot.getUnit(iUnit).getUnitType() == UnitHorse and pPlot.getUnit(iUnit).getOwner() == iUnitOwner and pPlot.getUnit(iUnit).canMove():
                                            bButtonUp = True
                                            break

                            # Horse -> Swordsman
                            if bButtonDown:
                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HORSE_DOWN").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 666, 666, False)
                                screen.show("BottomButtonContainer")
                                iCount = iCount + 1
                            # Swordsman -> Horse
                            elif bButtonUp:
                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HORSE_UP").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 667, 667, False)
                                screen.show("BottomButtonContainer")
                                iCount = iCount + 1
                        # Ende Horse <-> Unit

                        # ------------------
                        # BEGIN Merchant trade/cultivation/collect Bonus (738-741) (Boggy)
                        if pUnit.canMove():  # and not pUnit.hasMoved():
                            pPlot = g_pSelectedUnit.plot()
                            if iUnitType in L.LCultivationUnits:
                                if pPlot.getOwner() == iUnitOwner or pPlot.getOwner() != -1 and gc.getTeam(gc.getPlayer(pPlot.getOwner()).getTeam()).isVassal(pUnitOwner.getTeam()):
                                    eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
                                    # Collect bonus from plot or city
                                    ePlotBonus = pPlot.getBonusType(iUnitOwner)  # Invisible bonuses can NOT be collected
                                    # remove from plot => iData2 = 0. 1 = charge all goods without removing. Nur bei leerem Karren.
                                    if eBonus == -1:
                                        if ePlotBonus != -1 and (ePlotBonus in L.LBonusCultivatable or ePlotBonus in L.LBonusStratCultivatable):
                                            if pPlot.getOwner() == iUnitOwner:
                                                if pPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"):
                                                    iData = -1
                                                else:
                                                    iData = 0
                                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_COLLECT").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 739, iData, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                            elif not bCity:
                                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_BUY").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 739, 2, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                        if bCity:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_BUY").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 739, 1, True)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                    elif bCity:
                                        iPrice = PAE_Trade.calculateBonusSellingPrice(pUnit, pPlot.getPlotCity(), 0)
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_SELL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 741, int(iPrice), False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1
                                    else:
                                        if ePlotBonus in L.LBonusCorn and eBonus in L.LBonusCorn or ePlotBonus in L.LBonusLivestock and eBonus in L.LBonusLivestock:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_CULTIVATE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 738, 738, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                        else:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_COLLECT_IMPOSSIBLE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 739, 739, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1

                                    # Cultivate bonus onto plot
                                    if eBonus != -1 and PAE_Cultivation.isBonusCultivatable(pUnit):
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_CULTIVATE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 738, 738, bCity)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1
                            # Buy / sell goods in cities (domestic or foreign)
                            if bCity:
                                if iUnitType in L.LTradeUnits:
                                    bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA"], 0))
                                    if not bTradeRouteActive:
                                        eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
                                        # Sell
                                        if eBonus != -1:
                                            iPrice = PAE_Trade.calculateBonusSellingPrice(pUnit, pPlot.getPlotCity(), 0)
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_SELL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 741, int(iPrice), False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1
                                        # Buy
                                        else:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_BUY").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 740, 740, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                        # Set or Cancel automated trade route
                        if iUnitType in L.LTradeUnits:
                            bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA"], 0))
                            if bTradeRouteActive:
                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_AUTO_STOP").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 748, 748, False)
                                screen.show("BottomButtonContainer")
                                iCount = iCount + 1
                            else:
                                # Set Automated Trade Route
                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_AUTO_START").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 744, 744, False)
                                screen.show("BottomButtonContainer")
                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                iCount = iCount + 1

                            # Escorte / Begleitschutz anfordern
                            #if iUnitType == gc.getInfoTypeForString("UNIT_CARAVAN") or iUnitType == gc.getInfoTypeForString("UNIT_TRADE_MERCHANT"):
                            if pUnit.getDomainType() == DomainTypes.DOMAIN_LAND:
                                iPromo = gc.getInfoTypeForString("PROMOTION_SCHUTZ")
                                if not pUnit.isHasPromotion(iPromo):
                                    iCost = 20
                                    if pUnitOwner.isCivic(gc.getInfoTypeForString("CIVIC_SOELDNERTUM")):
                                        iCost = 15
                                    if pUnitOwner.getGold() >= iCost:
                                        screen.appendMultiListButton("BottomButtonContainer", gc.getPromotionInfo(iPromo).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 762, iCost, False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1

                        # END Merchant -----

                        # Goldkarren / Treasure / Beutegold -> in die Hauptstadt / Provinzhauptstadt / Bischofssitz
                        if iUnitType == gc.getInfoTypeForString("UNIT_GOLDKARREN"):
                            pPlot = g_pSelectedUnit.plot()
                            if pPlot.isCity():
                                pCity = g_pSelectedUnit.plot().getPlotCity()
                                if pCity.getOwner() == pUnit.getOwner():
                                    if bCapital:
                                        # Gold in die Schatzkammer bringen
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GOLDKARREN").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 677, 1, False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1
                                        return

                            # button zur next gov city
                            if PAE_Unit.getGovCenter(pUnit):
                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_goldkarren.dds", 0, WidgetTypes.WIDGET_GENERAL, 677, 2, False)
                                screen.show("BottomButtonContainer")
                                if pPlot.getOwner() == pUnit.getOwner():
                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                iCount = iCount + 1

                        # --------- Einheiten in einer Stadt
                        if bCity and pUnit.canMove():
                            pCity = g_pSelectedUnit.plot().getPlotCity()
                            # In der eigenen Stadt
                            if pCity.getOwner() == iUnitOwner:
                                pTeam = gc.getTeam(pUnitOwner.getTeam())

                                # Provinzstatthalter / Tribut
                                if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")):

                                    bAllowed = True
                                    PAE_City.PAEStatthalterTribut.setdefault(iUnitOwner, 0)
                                    if PAE_City.PAEStatthalterTribut[iUnitOwner] == 1:
                                        bAllowed = False

                                    # Provinzstatthalter / Tribut
                                    if bAllowed:
                                        if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_POLYARCHY")):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_statthalter_main.dds", 0, WidgetTypes.WIDGET_GENERAL, 737, 737, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                # --------------------------------------------------------

                                # Vasallen freilassen/entlassen oder denen eine Stadt schenken
                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_VASALLENTUM")):
                                    if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PALACE")):
                                        if PAE_Vassal.getVassals(iUnitOwner):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Civics/civic_buerger.dds", 0, WidgetTypes.WIDGET_GENERAL, 764, 764, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                # ------------------------------------------------


                                # Soeldner anheuern / Mercenaries (in der eigenen Stadt)
                                if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SOELDNERPOSTEN")):
                                    if not pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")):
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARIES_CITYBUTTON").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 707, 707, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                # --------------------------------------------------------

                                # Statthalter ansiedeln / Held / Hero / Feldherr / General
                                # Beim Statthalter nur Button anzeigen, wenn bereits ein Provinzpalast steht. Bauen geht übers XML.
                                # Bei Helden oder Feldherren: ändern oder bauen
                                if pUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_STATTHALTER"):
                                    if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")) or pCity.canConstruct(gc.getInfoTypeForString("BUILDING_PROVINZPALAST"), False, False, True):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Buildings/button_building_statthalter.dds", 0, WidgetTypes.WIDGET_GENERAL, 757, 0, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                elif pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
                                    if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")) or pCity.canConstruct(gc.getInfoTypeForString("BUILDING_PROVINZPALAST"), False, False, True):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Buildings/button_building_statthalter.dds", 0, WidgetTypes.WIDGET_GENERAL, 757, 1, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                # --------------------------------------------------------

                                # Sklaven in der Stadt
                                if iUnitType == gc.getInfoTypeForString("UNIT_SLAVE"):
                                    # Sklaven zu Feld oder Bergwerksklaven
                                    bFarms = False
                                    bMines = False

                                    # iX = pCity.getX()
                                    # iY = pCity.getY()
                                    for iI in xrange(gc.getNUM_CITY_PLOTS()):
                                        loopPlot = pCity.getCityIndexPlot(iI)
                                        if loopPlot is not None and not loopPlot.isNone():
                                            # Plot besetzt?
                                            if pCity.canWork(loopPlot):
                                                if loopPlot.getImprovementType() in L.LFarms:
                                                    bFarms = True
                                                elif loopPlot.getImprovementType() in L.LMines:
                                                    bMines = True
                                        # Schleife vorzeitig beenden
                                        if bFarms and bMines:
                                            break

                                    # Sklave -> SPECIALIST_SLAVE_FOOD
                                    if bFarms:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave2farm.dds", 0, WidgetTypes.WIDGET_GENERAL, 734, 1, True)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                    else:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave2farm_gr.dds", 0, WidgetTypes.WIDGET_GENERAL, 734, 1, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                    # Sklave -> SPECIALIST_SLAVE_PROD
                                    if bMines:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave2mine2.dds", 0, WidgetTypes.WIDGET_GENERAL, 734, 2, True)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                    else:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave2mine2_gr.dds", 0, WidgetTypes.WIDGET_GENERAL, 734, 2, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                    # ------------

                                    # Sklaven -> Gladiator
                                    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GLADIATOR")):
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GLADIATOR").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 669, 669, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                    # Sklaven -> Schule (Gymnasion hat bereits +5 Forschung)
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_SCHULE")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iCulture = pCity.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_RESEARCH, iBuilding1)
                                        if iCulture < 10:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2SCHOOL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 679, 679, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # Sklaven -> Bibliothek
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_LIBRARY")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iCulture = pCity.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_RESEARCH, iBuilding1)
                                        if iCulture < 10:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2LIBRARY").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 729, 729, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # Sklaven -> Bordell / Freudenhaus
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_BORDELL")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iCulture = pCity.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_CULTURE, iBuilding1)
                                        if iCulture < 10:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2BORDELL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 668, 668, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1

                                    # Sklaven -> Theater
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_THEATER")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iCulture = pCity.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_CULTURE, iBuilding1)
                                        if iCulture < 10:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2THEATRE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 670, 670, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1

                                    # Sklaven -> Brotmanufaktur
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_BROTMANUFAKTUR")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iFood = pCity.getBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), 0)
                                        if iFood < 3:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2BROTMANUFAKTUR").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 755, 755, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # Sklaven -> Manufaktur
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_CORP3")
                                    if pCity.isHasBuilding(iBuilding1):
                                        #iFood = pCity.getBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), 0)
                                        #if iFood < 5:
                                        #    screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2MANUFAKTUR_FOOD").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 680, 680, False)
                                        #    screen.show("BottomButtonContainer")
                                        #    iCount = iCount + 1

                                        iProd = pCity.getBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), 1)
                                        if iProd < 5:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2MANUFAKTUR_PROD").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 681, 681, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1

                                    # Sklaven -> Palast
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_PALACE")
                                    if pCity.isHasBuilding(iBuilding1):
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_PALACE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 692, 692, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                    # Sklaven -> Tempel
                                    for iBuilding in L.LTemples:
                                        if pCity.isHasBuilding(iBuilding):
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_TEMPLE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 693, 693, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                            break

                                    # Sklaven -> Feuerwehr
                                    # if pTeam.isHasTech(gc.getInfoTypeForString("TECH_FEUERWEHR")):
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_FEUERWEHR")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iHappyiness = pCity.getBuildingHappyChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType())
                                        if iHappyiness < 3:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_FEUERWEHR").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 696, 696, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # Sklaven -> An den Sklavenmarkt verkaufen
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")
                                    if pCity.isHasBuilding(iBuilding1):
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SELL_SLAVES").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 694, 694, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                # ---- Ende Sklaven (eigene Stadt)

                                # Kauf einer edlen Ruestung (eigene Stadt)
                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_ARMOR")):
                                    iPromo = gc.getInfoTypeForString("PROMOTION_EDLE_RUESTUNG")
                                    if not pUnit.isHasPromotion(iPromo):
                                        if pUnit.getUnitCombatType() not in L.LCombatNoRuestung and pUnit.getUnitCombatType() > 0:
                                            if pUnit.getUnitType() not in L.LUnitNoRuestung:
                                                iBuilding1 = gc.getInfoTypeForString("BUILDING_FORGE")
                                                bonus1 = gc.getInfoTypeForString("BONUS_OREICHALKOS")
                                                bonus2 = gc.getInfoTypeForString("BONUS_MESSING")
                                                iPromoPrereq = gc.getInfoTypeForString("PROMOTION_COMBAT5")

                                                if pCity.isHasBuilding(iBuilding1) and (pCity.hasBonus(bonus1) or pCity.hasBonus(bonus2)) and pUnit.isHasPromotion(iPromoPrereq):
                                                    iCost = gc.getUnitInfo(pUnit.getUnitType()).getCombat() * 12
                                                    if gc.getPlayer(iUnitOwner).getGold() >= iCost:
                                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EDLE_RUESTUNG").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 699, iCost, True)
                                                    else:
                                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EDLE_RUESTUNG2").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 699, iCost, False)
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EDLE_RUESTUNG2").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 699, -1, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                # Ende Kauf einer Edlen Ruestung

                                # Terrain Promos - Ausbildner / Trainer (in City) ID 719
                                for iPromo in L.DPromosForPromoBuilding:
                                    if pUnit.isHasPromotion(iPromo):
                                        iBuilding = L.DPromosForPromoBuilding[iPromo]
                                        if not pCity.isHasBuilding(iBuilding):
                                            kBuildingInfo = gc.getBuildingInfo(iBuilding)
                                            if not kBuildingInfo.isWater() or pCity.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()): #kBuildingInfo.getMinAreaSize()
                                                screen.appendMultiListButton("BottomButtonContainer", gc.getBuildingInfo(iBuilding).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 719, iBuilding, False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                                # Auswanderer / Emigrant -> in der eigenen Stadt
                                if iUnitType == gc.getInfoTypeForString("UNIT_EMIGRANT"):
                                    # Stadt aufloesen / disband city
                                    if pUnitOwner.getNumCities() > 1 and pCity.getPopulation() < 3 and not pCity.isCapital():
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DISBAND_CITY").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 673, 673, True)
                                    else:
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DISBAND_CITY2").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 673, 673, False)
                                    screen.show("BottomButtonContainer")
                                    iCount = iCount + 1
                                    # zuwandern / immigrate
                                    screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EMIGRANT").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 672, 672, False)
                                    screen.show("BottomButtonContainer")
                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                    iCount = iCount + 1
                                # Siedler -> in der eigenen Stadt
                                elif iUnitType == gc.getInfoTypeForString("UNIT_SETTLER"):
                                    # Stadt aufloesen / disband city
                                    if pUnitOwner.getNumCities() > 1 and pCity.getPopulation() < 3 and not pCity.isCapital():
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DISBAND_CITY").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 673, 673, True)
                                        iCount = iCount + 1

                                # Reservist -> Veteran (in der eigenen Stadt)
                                iReservists = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"))  # SPECIALIST_RESERVIST
                                if iReservists >= 1:
                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_city_reservists.dds", 0, WidgetTypes.WIDGET_GENERAL, 725, 725, False)
                                    screen.show("BottomButtonContainer")
                                    iCount = iCount + 1

                                # Nahrung abliefern
                                if iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"):
                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_getreide2town.dds", 0, WidgetTypes.WIDGET_GENERAL, 727, 1, False)
                                    screen.show("BottomButtonContainer")
                                    iCount = iCount + 1
                                # Nahrung aufsammeln
                                elif iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
                                    if pCity.getFood() > 0 and PAE_Unit.getMaxSupply(pUnit) != PAE_Unit.getSupply(pUnit):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_food2supply.dds", 0, WidgetTypes.WIDGET_GENERAL, 727, 2, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                # Karten zeichnen (innerhalb eigene Stadt)
                                elif pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_RECON"):
                                    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KARTEN")):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Techs/button_tech_karten.dds", 0, WidgetTypes.WIDGET_GENERAL, 728, 728, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                # Release slaves
                                elif pUnit.isMilitaryHappiness():
                                    eSpecialistGlad = gc.getInfoTypeForString("SPECIALIST_GLADIATOR")
                                    eSpecialistHouse = gc.getInfoTypeForString("SPECIALIST_SLAVE")
                                    eSpecialistFood = gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")
                                    eSpecialistProd = gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")
                                    iCityGlads = pCity.getFreeSpecialistCount(eSpecialistGlad)  # SPECIALIST_GLADIATOR
                                    iCitySlavesHaus = pCity.getFreeSpecialistCount(eSpecialistHouse)  # SPECIALIST_SLAVE
                                    iCitySlavesFood = pCity.getFreeSpecialistCount(eSpecialistFood)  # SPECIALIST_SLAVE_FOOD
                                    iCitySlavesProd = pCity.getFreeSpecialistCount(eSpecialistProd)  # SPECIALIST_SLAVE_PROD
                                    iCitySlaves = iCitySlavesHaus + iCitySlavesFood + iCitySlavesProd

                                    if iCityGlads + iCitySlaves > 0:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave_release.dds", 0, WidgetTypes.WIDGET_GENERAL, 730, 730, True)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                # ---- ENDE if Einheit -> in der eigenen Stadt

                                # ++++++++++++++++++++++++++++++++
                                # In eigenen und fremden Staedten:
                                # ++++++++++++++++++++++++++++++++

                                if pUnit.isMilitaryHappiness():
                                    # Verkauf von Einheiten
                                    # Soll in jeder Stadt mit Soeldnerposten verkauft werden
                                    # Unit -> An den Soeldnerposten verkaufen
                                    iBuilding1 = gc.getInfoTypeForString("BUILDING_SOELDNERPOSTEN")
                                    if pCity.isHasBuilding(iBuilding1):
                                        iCost = PyInfo.UnitInfo(pUnit.getUnitType()).getProductionCost() / 2
                                        if iCost < 1:
                                            iCost = 80
                                        if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY")):
                                            iCost = iCost / 2
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SELL_UNITS").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 695, iCost, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                    # Einheit segnen / bless unit (PAE V Patch 4)
                                    iPromo = gc.getInfoTypeForString("PROMOTION_BLESSED")
                                    if not pUnit.isHasPromotion(iPromo):
                                        iBuilding1 = gc.getInfoTypeForString("BUILDING_CHRISTIAN_CATHEDRAL")
                                        iBuilding2 = gc.getInfoTypeForString("BUILDING_HAGIA_SOPHIA")
                                        if pCity.isHasBuilding(iBuilding1) or pCity.isHasBuilding(iBuilding2):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Promotions/button_promo_blessed.dds", 0, WidgetTypes.WIDGET_GENERAL, 752, 0, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # Einheit Moral verbessern (PAE VI Patch 6.8)
                                    iPromo = gc.getInfoTypeForString("PROMOTION_MORALE")
                                    if not pUnit.isHasPromotion(iPromo):
                                        iBuilding = gc.getInfoTypeForString("BUILDING_STATUE_OF_ZEUS")
                                        if pCity.isHasBuilding(iBuilding):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Promotions/button_promo_morale.dds", 0, WidgetTypes.WIDGET_GENERAL, 752, 1, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                # Kauf von Wellen-Oil -----------
                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KUESTE")):
                                    iPromo = gc.getInfoTypeForString("PROMOTION_OIL_ON_WATER")
                                    if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL") and not pUnit.isHasPromotion(iPromo):
                                        bonus1 = gc.getInfoTypeForString("BONUS_OLIVES")
                                        iPromo2 = gc.getInfoTypeForString("PROMOTION_COMBAT2")
                                        if pUnit.isHasPromotion(iPromo2) and pCity.hasBonus(bonus1):
                                            iCost = int(PyInfo.UnitInfo(pUnit.getUnitType()).getProductionCost() / 2)
                                            if iCost <= 0:
                                                iCost = 80
                                            if gc.getPlayer(iUnitOwner).getGold() >= iCost:
                                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_PROMO_OIL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 701, iCost, True)
                                            else:
                                                screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_PROMO_OIL2").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 701, iCost, False)
                                        else:
                                            screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_PROMO_OIL2").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 701, -1, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                            # ---- ENDE if Einheit in der eigenen Stadt --------

                            # ---- Einheit egal in welcher Stadt:

                            # Versorgungswagen und Heldendenkmal / Siegesdenkmal / monument
                            # Nur Versorgungskarren, nicht Druiden! (iUnitType anstatt iUnitclassType)
                            if iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
                                if pCity.getOwner() == iUnitOwner:
                                    iBuilding = int(CvUtil.getScriptData(pUnit, ["hd"], -1))
                                    # Heldendenkmal abbauen
                                    if iBuilding == -1 and PAE_City.isHasHeldendenkmal(pCity):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_collect_heldendenkmal.dds", 0, WidgetTypes.WIDGET_GENERAL, 758, 0, True)
                                        #screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_statue1.dds", 0, WidgetTypes.WIDGET_GENERAL, 758, 0, True)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                    # Heldendenkmal wieder setzen
                                    elif iBuilding != -1 and not pCity.isHasBuilding(iBuilding):
                                        screen.appendMultiListButton("BottomButtonContainer", gc.getBuildingInfo(iBuilding).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 758, iBuilding, True)
                                        #screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_statue2.dds", 0, WidgetTypes.WIDGET_GENERAL, 758, iBuilding, True)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1


                            # ---- Ende if Einheiten in einer Stadt
                        else:
                            # ---- Einheit nicht in der Stadt

                            if pUnit.isMilitaryHappiness():
                                pPlot = pUnit.plot()

                                # Pillage Road
                                if pPlot.getRouteType() > -1:
                                    if pPlot.getOwner() < 0 or pPlot.getOwner() == iUnitOwner or gc.getTeam(pPlot.getOwner()).isAtWar(pUnitOwner.getTeam()):
                                        screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_PILLAGE_ROAD").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 700, 0, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                                # LEADER: Wald verbrennen
                                if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
                                    if pPlot.getFeatureType() in L.LForests:
                                        if pPlot.getOwner() < 0 or pPlot.getOwner() == iUnitOwner and gc.getTeam(iUnitOwner).getAtWarCount(True) or gc.getTeam(pPlot.getOwner()).isAtWar(pUnitOwner.getTeam()):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Terrainfeatures/button_brand.dds", 0, WidgetTypes.WIDGET_GENERAL, 765, 0, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1

                                # Forts/Handelsposten erobern 763
                                #if pPlot.getImprovementType() in L.LImprFortShort:
                                #  iFortOwner = int(CvUtil.getScriptData(pPlot, ["p", "t"], pPlot.getOwner()))
                                #  if iFortOwner != iUnitOwner:
                                #    if iFortOwner == -1 or gc.getTeam(gc.getPlayer(iFortOwner).getTeam()).isAtWar(gc.getPlayer(iUnitOwner).getTeam()):
                                #      # Pillage Road
                                #      screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_x.dds", 0, WidgetTypes.WIDGET_GENERAL, 763, 763, False)
                                #      screen.show("BottomButtonContainer")
                                #      iCount = iCount + 1

                            # Piraten-Feature
                            # Nur fuer bestimmte Nationen (ab PAE V Patch 3)
                            if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
                                if gc.getTeam(pUnitOwner.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_PIRACY")):

                                    # PAE VI: mit TECH moeglich = generell gesperrte Tech
                                    #if pUnit.getCivilizationType() in L.LCivPirates:
                                    if pUnit.getUnitType() in L.DCaptureFromPirate or pUnit.getUnitType() in L.DCaptureByPirate:
                                        if pUnit.hasCargo():
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_pirat2.dds", 0, WidgetTypes.WIDGET_GENERAL, 722, 3, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                        elif pUnit.getUnitType() in L.DCaptureFromPirate:
                                            screen.appendMultiListButton("BottomButtonContainer", gc.getCivilizationInfo(pUnitOwner.getCivilizationType()).getButton(), 0, WidgetTypes.WIDGET_GENERAL, 722, 2, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                        elif pUnit.getUnitType() in L.DCaptureByPirate:
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_pirat.dds", 0, WidgetTypes.WIDGET_GENERAL, 722, 1, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1

                            # Limes
                            elif iUnitType == gc.getInfoTypeForString("UNIT_LEGION") or iUnitType == gc.getInfoTypeForString("UNIT_LEGION2") or \
                                  iUnitType == gc.getInfoTypeForString("UNIT_AUXILIAR_ROME") or iUnitType == gc.getInfoTypeForString("UNIT_ROME_LIMITANEI"):
                                if gc.getTeam(pUnitOwner.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_LIMES")):
                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Buildings/button_building_limes.dds", 0, WidgetTypes.WIDGET_GENERAL, 733, -1, False)
                                    screen.show("BottomButtonContainer")
                                    iCount = iCount + 1
                            # Handelsposten
                            elif iUnitType == gc.getInfoTypeForString("UNIT_TRADE_MERCHANT") or iUnitType == gc.getInfoTypeForString("UNIT_CARAVAN"):
                                # Update: auch in eigenen Grenzen anzeigen (zB fuer Inseln), aber nur wenn nicht bereits was drauf steht
                                # if pUnit.plot().getOwner() == -1:
                                pPlot = pUnit.plot()
                                if not pPlot.isWater():
                                    if pPlot.getOwner() == -1 or (pPlot.getImprovementType() == -1 and pPlot.getOwner() == iUnitOwner):
                                        if pPlot.getBonusType(-1) != -1:
                                            if gc.getTeam(pUnitOwner.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_WARENHANDEL")):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Builds/button_build_handelsposten.dds", 0, WidgetTypes.WIDGET_GENERAL, 736, pPlot.getBonusType(-1), False)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1
                            # Sklaven ausserhalb der Stadt
                            elif iUnitType == gc.getInfoTypeForString("UNIT_SLAVE"):
                                pPlot = pUnit.plot()
                                if pPlot.getOwner() == pUnit.getOwner():
                                    if pPlot.getImprovementType() in L.LVillages:
                                        if pPlot.getUpgradeTimeLeft(pPlot.getImprovementType(), iUnitOwner) > 1:
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave2village.dds", 0, WidgetTypes.WIDGET_GENERAL, 753, 0, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1
                                    elif pPlot.getImprovementType() in L.LLatifundien:
                                        #if pPlot.getUpgradeTimeLeft(pPlot.getImprovementType(), iUnitOwner) > 1:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_slave2latifundium.dds", 0, WidgetTypes.WIDGET_GENERAL, 753, 1, False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1
                            # Trojanisches Pferd vor der Stadt
                            elif iUnitType == gc.getInfoTypeForString("UNIT_TROJAN_HORSE"):
                                if PAE_Unit.TrojanHorsePossible(g_pSelectedUnit):
                                    # Stadtverteidigung auf 0 setzen
                                    screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TROJAN_HORSE").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 697, 697, False)
                                    screen.show("BottomButtonContainer")
                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                    iCount = iCount + 1


                        # Ende ausserhalb der Stadt --------

                        # Innerhalb und ausserhalb der Stadt -------------------------------

                        # FORMATIONEN / FORMATIONS (in oder ausserhalb der Stadt ab PAE V Patch 2) --------------------------------
                        bFormationUndo = (pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2")))
                        if pUnit.canMove() or bFormationUndo:
                            # PAE V Patch 2: disabled for fights on his own units
                            if not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY")):
                                pPlot = pUnit.plot()
                                iImp = pPlot.getImprovementType()
                                #iFeat = pPlot.getFeatureType()
                                # in Festungen (keine Formationen erlauben, ausser PROMOTION_FORM_FORTRESS)
                                if iImp in L.LImprFort:
                                    # Besitzerabfrage
                                    if pPlot.getOwner() == iUnitOwner or pPlot.getOwner() == -1:
                                        # Nur Melee
                                        if pUnit.getUnitCombatType() in L.LMeleeCombats or pUnit.getUnitCombatType() in L.LArcherCombats:
                                            # Festungsformation
                                            if PyInfo.UnitInfo(pUnit.getUnitType()).getMoves() == 1:
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS")
                                            else:
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2")
                                            if not pUnit.isHasPromotion(iFormation):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_fortress.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1

                                # ausserhalb von Festungen
                                # elif iFeat not in L.LFeatureArray:
                                else:
                                    # Naval
                                    if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
                                        if gc.getTeam(pUnitOwner.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_LOGIK")):
                                            if pUnit.getUnitType() not in L.LFormationNoNaval:
                                                # Keil
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_KEIL")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_keil_marine_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, 718, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_keil_marine.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                # Zange
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_ZANGE")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_zange_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, 718, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_zange.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                # Full speed / Volle Kraft
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_FULL_SPEED")
                                                screen.appendMultiListButton("BottomButtonContainer", gc.getPromotionInfo(iFormation).getButton(), 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.disableMultiListButton("BottomButtonContainer", 0, iCount, gc.getPromotionInfo(iFormation).getButton())
                                                    bFormationUndo = True
                                                iCount = iCount + 1



                                    # Mounted mit Fernangriff
                                    elif pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
                                        if pUnit.getUnitType() in L.LFormationMountedArcher:
                                            if pUnit.getCivilizationType() in L.LCivPartherschuss and pTeam.isHasTech(gc.getInfoTypeForString("TECH_PARTHERSCHUSS")):
                                                # Partherschuss
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PARTHER")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_parther_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, 718, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_parther.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KANTAKREIS")):
                                                # Kantabrischer Kreis
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_kantakreis_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, 718, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_kantakreis.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                        # Keil (auch weiter unten fuer Melee)
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KETTENPANZER")):
                                            if pUnit.getUnitType() in L.LKeilUnits:
                                                # Keil
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KEIL")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_keil_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_keil.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                        if pUnit.getUnitType() not in L.LUnitNoSlaves:
                                            # Fourage
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BRANDSCHATZEN")):
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FOURAGE")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_fourage_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_fourage.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                    # Melee and Spear
                                    elif pUnit.getUnitCombatType() in L.LMeleeCombats:
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG4")):
                                            # Schildwall
                                            if pUnit.getUnitType() not in L.LNoSchildwallUnits:
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_SCHILDWALL")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_wall_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_wall.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                        # Manipel, Phalanx, ...
                                        if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DRILL1")):

                                            # Roman Legion (Kohorte / ersetzt alles)
                                            if pUnit.getUnitType() in L.LDrillUnits:
                                                # Kohorte
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KOHORTE")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_kohorte_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_kohorte.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                            # Treffen-Taktik ersetzt Manipel
                                            elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_TREFFEN")):
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_TREFFEN")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_treffen_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_treffen.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                            # Manipel ersetzt Phalanx, Manipular-Phalanx und Schiefe Phalanx
                                            elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_MANIPEL")):
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_MANIPEL")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_manipel_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_manipel.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                            # Phalanx-Arten und Geschlossene Formation
                                            else:
                                                # Phalanx nur Speer
                                                if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
                                                    # Manipular-Phalanx und Schiefe Phalanx ersetzt Phalanx
                                                    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX2")):
                                                        # Schiefe Schlachtordnung
                                                        iFormation = gc.getInfoTypeForString("PROMOTION_FORM_SCHIEF")
                                                        if pUnit.isHasPromotion(iFormation):
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_phalanx_s_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1
                                                            bFormationUndo = True
                                                        else:
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_phalanx_s.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1

                                                        # Manipular-Phalanx
                                                        iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PHALANX2")
                                                        if pUnit.isHasPromotion(iFormation):
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_phalanx_m_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1
                                                            bFormationUndo = True
                                                        else:
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_phalanx_m.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1

                                                    # Phalanx
                                                    elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX")):
                                                        iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PHALANX")
                                                        if pUnit.isHasPromotion(iFormation):
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_phalanx_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1
                                                            bFormationUndo = True
                                                        else:
                                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_phalanx.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                            screen.show("BottomButtonContainer")
                                                            iCount = iCount + 1

                                                # Geschlossene Formation (alle Melee)
                                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_CLOSED_FORM")):
                                                    iFormation = gc.getInfoTypeForString("PROMOTION_FORM_CLOSED_FORM")
                                                    if pUnit.isHasPromotion(iFormation):
                                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_closed_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                        screen.show("BottomButtonContainer")
                                                        iCount = iCount + 1
                                                        bFormationUndo = True
                                                    else:
                                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_closed.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                        screen.show("BottomButtonContainer")
                                                        iCount = iCount + 1
                                        # Drill end ------------

                                        # Keil (auch bei Mounted)
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KETTENPANZER")):
                                            # Keil
                                            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KEIL")
                                            if pUnit.isHasPromotion(iFormation):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_keil_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                                bFormationUndo = True
                                            else:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_keil.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1

                                        # Zangenangriff
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MILIT_STRAT")):
                                            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_ZANGENANGRIFF")
                                            if pUnit.isHasPromotion(iFormation):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_zange_a_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                                bFormationUndo = True
                                            else:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_form_zange_a.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1

                                        # Flankenschutz (nur Speer)
                                        if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_TREFFEN")):
                                                iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ")
                                                if pUnit.isHasPromotion(iFormation):
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_flanke_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1
                                                    bFormationUndo = True
                                                else:
                                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_flanke.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                    screen.show("BottomButtonContainer")
                                                    iCount = iCount + 1

                                        # Gedrillte Soldaten
                                        if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DRILL1")):

                                            # Testudo (nur Legion)
                                            if pTeam.isHasTech(gc.getInfoTypeForString("TECH_TESTUDO")):
                                                if pUnit.getUnitType() in L.LDrillUnits:
                                                    iFormation = gc.getInfoTypeForString("PROMOTION_FORM_TESTUDO")
                                                    if pUnit.isHasPromotion(iFormation):
                                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_testudo_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                        screen.show("BottomButtonContainer")
                                                        iCount = iCount + 1
                                                        bFormationUndo = True
                                                    else:
                                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_testudo.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                        screen.show("BottomButtonContainer")
                                                        iCount = iCount + 1

                                        # Elefantengasse (auch weiter unten fuer Bogen)
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GEOMETRIE2")):
                                            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_GASSE")
                                            if pUnit.isHasPromotion(iFormation):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_gasse_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                                bFormationUndo = True
                                            else:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_gasse.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1

                                    # Archers
                                    elif pUnit.getUnitCombatType() in L.LArcherCombats:
                                        # Elefantengasse
                                        if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GEOMETRIE2")):
                                            # if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DRILL1")):
                                            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_GASSE")
                                            if pUnit.isHasPromotion(iFormation):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_gasse_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                                bFormationUndo = True
                                            else:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_gasse.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1

                                    # PAE 6.9: Leader / Great General formation
                                    if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
                                        # Position des Generals in einem Stack
                                        iFormation = gc.getInfoTypeForString("PROMOTION_FORM_LEADER_POSITION")
                                        if pUnit.isHasPromotion(iFormation):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_leaderpos_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, 718, False)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                            bFormationUndo = True
                                        else:
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_leaderpos.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                            screen.show("BottomButtonContainer")
                                            iCount = iCount + 1
                                # -- Ende else Fortress

                                # Flucht
                                if pUnit.getDamage() >= 70:
                                    UnitCombatArray = [
                                        gc.getInfoTypeForString("UNITCOMBAT_MELEE"),
                                        gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"),
                                        gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN"),
                                        gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"),
                                        gc.getInfoTypeForString("UNITCOMBAT_ARCHER"),
                                        gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER")
                                    ]

                                    if pUnit.getUnitCombatType() in UnitCombatArray:
                                        if pUnit.baseMoves() == 1:
                                            iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FLIGHT")
                                            if pUnit.isHasPromotion(iFormation):
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_flight_gr.dds", 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
                                                screen.show("BottomButtonContainer")
                                                iCount = iCount + 1
                                                bFormationUndo = True
                                            else:
                                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_flight.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, iFormation, 718, True)
                                                screen.show("BottomButtonContainer")
                                                screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                                iCount = iCount + 1

                            # Keine Formation
                            if bFormationUndo:
                                screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Formations/button_formation_none.dds", 0, WidgetTypes.WIDGET_HELP_PROMOTION, -1, 718, True)
                                screen.show("BottomButtonContainer")
                                iCount = iCount + 1

                        # Formationen / Formations End ------

                        # Legend can become a Great General
                        if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT6")):
                            if pUnit.getUnitCombatType() not in L.LArcherCombats:
                                if not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
                                    screen.appendMultiListButton("BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_LEGEND_HERO_TO_GENERAL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, 720, 720, False)
                                    screen.show("BottomButtonContainer")
                                    screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                    iCount = iCount + 1

                        # Salae/Sold/Salaire und/oder Dezimation/Dezimierung
                        if pUnit.canMove():
                            if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG1")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY")):
                                if pTeam.isHasTech(gc.getInfoTypeForString("TECH_CURRENCY")):
                                    # +x Gold pro Promotion
                                    FormationArray = [
                                        gc.getInfoTypeForString("PROMOTION_WILDLIFE"),
                                        gc.getInfoTypeForString("PROMOTION_LOYALITAT"),
                                        gc.getInfoTypeForString("PROMOTION_MERCENARY")
                                    ]
                                    iGold = pUnit.baseCombatStr() * 3
                                    iRange = gc.getNumPromotionInfos()
                                    for j in xrange(iRange):
                                        if "_FORM_" in gc.getPromotionInfo(j).getType():
                                            continue
                                        if "_RANG_" in gc.getPromotionInfo(j).getType():
                                            continue
                                        if "_MORAL_" in gc.getPromotionInfo(j).getType():
                                            continue
                                        if "_TRAIT_" in gc.getPromotionInfo(j).getType():
                                            continue
                                        if pUnit.isHasPromotion(j) and j not in FormationArray:
                                            iGold += 3
                                    if iGold == 0:
                                        iGold = 20
                                    if gc.getPlayer(iUnitOwner).hasBonus(gc.getInfoTypeForString("BONUS_SALT")):
                                        iGold -= iGold / 4

                                    # Button testen
                                    screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_salae.dds", 0, WidgetTypes.WIDGET_GENERAL, 735, 1, True)
                                    screen.show("BottomButtonContainer")

                                    if gc.getPlayer(iUnitOwner).getGold() < iGold:
                                        screen.disableMultiListButton("BottomButtonContainer", 0, iCount, "Art/Interface/Buttons/Actions/button_action_salae.dds")
                                    iCount += 1

                                    # Dezimierung
                                    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_DEZIMATION")):
                                        # Button
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_dezimierung.dds", 0, WidgetTypes.WIDGET_GENERAL, 735, 2, True)
                                        screen.show("BottomButtonContainer")

                                        if pUnit.getDamage() > 80:
                                            screen.disableMultiListButton("BottomButtonContainer", 0, iCount, "Art/Interface/Buttons/Actions/button_action_dezimierung.dds")
                                        iCount += 1

                            # Moral/Sklaven/Duell/Kopfkult
                            if not pUnit.hasMoved() and pUnit.isMilitaryHappiness():

                                # Einheit Moral vergeben / give morale (PAE VI)
                                if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RHETORIK")):
                                    if pPlot.getNumDefenders(iUnitOwner) > 1:
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_leader_moral.dds", 0, WidgetTypes.WIDGET_GENERAL, 759, 1, False)
                                        screen.show("BottomButtonContainer")
                                        screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                        iCount = iCount + 1

                                # Sklaven auf dem Plot -> Moral steigern
                                pPlot = g_pSelectedUnit.plot()
                                bSlaves = False
                                iUnitSlave = gc.getInfoTypeForString("UNIT_SLAVE")
                                for iUnit in xrange(pPlot.getNumUnits()):
                                    if pPlot.getUnit(iUnit).getUnitType() == iUnitSlave and pPlot.getUnit(iUnit).getOwner() == iUnitOwner:
                                        bSlaves = True
                                        break

                                if bSlaves:

                                    # Druide (Sklaven opfern: Moral der Truppe verbessern)
                                    if iUnitType == gc.getInfoTypeForString("UNIT_DRUIDE"):
                                        if pPlot.getNumDefenders(iUnitOwner) > 1:
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Units/button_slave.dds", 0, WidgetTypes.WIDGET_GENERAL, 759, 2, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1
                                    elif not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORALE")):
                                        # Kopfkult
                                        if pUnit.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_CELT") \
                                        or pUnit.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN") \
                                        or pUnit.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_BRITEN"):
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_sklave_kopf.dds", 0, WidgetTypes.WIDGET_GENERAL, 760, 0, False)
                                            screen.show("BottomButtonContainer")
                                            screen.enableMultiListPulse("BottomButtonContainer", True, 0, iCount)
                                            iCount = iCount + 1

                                    # XP gewinnen in einem Duell
                                    # nur in einer Stadt mit Holzarena
                                    if pUnit.getLevel() < 3:
                                        bCheck = False
                                        if g_pSelectedUnit.plot().isCity():
                                            pCity = g_pSelectedUnit.plot().getPlotCity()
                                            # kann auch in einer fremden Stadt gemacht werden (ohne iOwner Check)
                                            if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_ARENA")):
                                                bCheck = True

                                        if bCheck:
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_action_sklave_fight.dds", 0, WidgetTypes.WIDGET_GENERAL, 761, 0, True)
                                        else:
                                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 761, 0, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                        # PAE 6.11: Pferdewechsel / change horse to get all move points again
                        if bCity:
                            if pUnit.hasMoved() and (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED") or pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_CHARIOT")):

                                bOK = False
                                # General oder Held
                                if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")):
                                    bOK = True

                                # Kamelstall
                                if bOK and pUnit.getUnitType() in L.LCamelUnits:
                                    if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CAMEL_STABLE")):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_camel_refresh.dds", 0, WidgetTypes.WIDGET_GENERAL, 766, 1, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1
                                # Pferdestall
                                elif bOK or pUnit.getUnitType() in L.LUnits4HorseSwap:
                                    if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STABLE")):
                                        screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_horse_refresh.dds", 0, WidgetTypes.WIDGET_GENERAL, 766, 0, False)
                                        screen.show("BottomButtonContainer")
                                        iCount = iCount + 1

                        # ---------- INFO BUTTONS --------------------

                        # Info Button: Legion
                        if iUnitType == gc.getInfoTypeForString("UNIT_LEGION") or iUnitType == gc.getInfoTypeForString("UNIT_LEGION2"):
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 8, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1
                        # Info Button: Praetorianer
                        elif iUnitType == gc.getInfoTypeForString("UNIT_PRAETORIAN"):
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 9, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1
                        # Info Button: Versorgungswagen
                        elif iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 10, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1
                        # Info Button: Getreidekarren
                        elif iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"):
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 11, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1
                        # Info Button: Handelskarren/Merchant
                        elif iUnitType in L.LTradeUnits:
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 12, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1
                        # Info Button: Kriegslager/Camp
                        elif iUnitType == gc.getInfoTypeForString("UNIT_CAMP"):
                            screen.appendMultiListButton("BottomButtonContainer", "Art/Interface/Buttons/Actions/button_info.dds", 0, WidgetTypes.WIDGET_GENERAL, 721, 13, False)
                            screen.show("BottomButtonContainer")
                            iCount += 1

        elif CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY:
            self.setMinimapButtonVisibility(True)

        return 0

    # Will update the research buttons
    def updateResearchButtons(self):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        for i in xrange(gc.getNumTechInfos()):
            szName = "ResearchButton" + str(i)
            screen.hide(szName)

        # Find out our resolution
        # xResolution = screen.getXResolution()
        # yResolution = screen.getYResolution()

        #screen.hide( "InterfaceOrnamentLeftLow" )
        #screen.hide( "InterfaceOrnamentRightLow" )

        for i in xrange(gc.getNumReligionInfos()):
            szName = "ReligionButton" + str(i)
            screen.hide(szName)

        i = 0
        if CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
            iCount = 0
            for i in xrange(gc.getNumTechInfos()):
                if gc.getActivePlayer().canResearch(i, False):
                    if iCount < 20:
                        szName = "ResearchButton" + str(i)
                        bDone = False
                        for j in xrange(gc.getNumReligionInfos()):
                            if not bDone:
                                if gc.getReligionInfo(j).getTechPrereq() == i:
                                    if not gc.getGame().isReligionSlotTaken(j):
                                        szName = "ReligionButton" + str(j)
                                        bDone = True
                        screen.show(szName)
                        self.setResearchButtonPosition(szName, iCount)
                    iCount = iCount + 1
        return 0

    # SPECIALIST STACKER        05/02/07      JOHNY
    def updateCitizenButtons(self):

        global MAX_CITIZEN_BUTTONS
        global MAX_SUPER_SPECIALIST_BUTTONS
        global MAX_ANGRY_CITIZEN_BUTTONS
        global g_iSuperSpecialistCount
        global g_iAngryCitizensCount

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        for i in xrange(g_iSuperSpecialistCount):
            szName = "FreeSpecialist" + str(i)
            screen.hide(szName)

        for i in xrange(g_iAngryCitizensCount):
            szName = "AngryCitizen" + str(i)
            screen.hide(szName)

        for i in xrange(gc.getNumSpecialistInfos()):
            szName = "IncreaseSpecialist" + str(i)
            screen.hide(szName)
            szName = "DecreaseSpecialist" + str(i)
            screen.hide(szName)
            szName = "CitizenDisabledButton" + str(i)
            screen.hide(szName)
            for j in xrange(MAX_CITIZEN_BUTTONS):
                szName = "CitizenButton" + str((i * 100) + j)
                screen.hide(szName)
                szName = "CitizenButtonHighlight" + str((i * 100) + j)
                screen.hide(szName)


        screen.hide("SpecialistBackground")
        screen.hide("SpecialistLabel")

        if not CyInterface().isCityScreenUp():
            return 0

        pHeadSelectedCity = CyInterface().getHeadSelectedCity()
        if not pHeadSelectedCity or CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_SHOW:
            return 0


        bHandled = False

        # Find out our resolution
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        currentAngryCitizenCount = pHeadSelectedCity.angryPopulation(0)

        stackWidth = self.angryCitizenStackWidth(currentAngryCitizenCount)

        for i in xrange(currentAngryCitizenCount):
            bHandled = True
            szName = "AngryCitizen" + str(i)
            xCoord = xResolution - 74 - (stackWidth * i)
            yCoord = yResolution - 228
            screen.setImageButton(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1)
            screen.show(szName)

        # update the max ever citizen counts
        if g_iAngryCitizensCount < currentAngryCitizenCount:
            g_iAngryCitizensCount = currentAngryCitizenCount

        iCount = 0
        bHandled = False
        currentFreeSpecialistCount = 0

        for i in xrange(gc.getNumSpecialistInfos()):
            if pHeadSelectedCity.getFreeSpecialistCount(i) > 0:
                if g_bDisplayUniqueSuperSpecialistsOnly:
                    currentFreeSpecialistCount += 1
                else:
                    currentFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

        stackWidth = self.superSpecialistStackWidth(currentFreeSpecialistCount)

        for i in xrange(gc.getNumSpecialistInfos()):
            for j in xrange(pHeadSelectedCity.getFreeSpecialistCount(i)):
                if not g_bStackSuperSpecialists and iCount > MAX_SUPER_SPECIALIST_BUTTONS-1:
                    break
                xCoord = xResolution - 74 - (stackWidth * iCount)
                yCoord = yResolution - 203
                szName = "FreeSpecialist" + str(iCount)
                screen.setImageButton(szName, gc.getSpecialistInfo(i).getTexture(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1)
                screen.show(szName)
                bHandled = True

                iCount = iCount + 1

                if g_bDisplayUniqueSuperSpecialistsOnly:
                    break

        # update the max ever citizen counts
        if g_iSuperSpecialistCount < iCount:
            g_iSuperSpecialistCount = iCount

        iXShiftVal = 0
        iYShiftVal = 0
        iSpecialistCount = 0

        for i in xrange(gc.getNumSpecialistInfos()):

            bHandled = False
            if iSpecialistCount > 5:
                iXShiftVal = 110
                iYShiftVal = (iSpecialistCount % 5) - 1
            else:
                iYShiftVal = iSpecialistCount

            if gc.getSpecialistInfo(i).isVisible():
                iSpecialistCount = iSpecialistCount + 1

            if pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode():

                if pHeadSelectedCity.isSpecialistValid(i, 1) and pHeadSelectedCity.getForceSpecialistCount(i) < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()):
                    szName = "IncreaseSpecialist" + str(i)
                    screen.show(szName)
                    szName = "CitizenDisabledButton" + str(i)
                    screen.show(szName)

                if pHeadSelectedCity.getSpecialistCount(i) > 0 or pHeadSelectedCity.getForceSpecialistCount(i) > 0:
                    szName = "CitizenDisabledButton" + str(i)
                    screen.hide(szName)
                    szName = "DecreaseSpecialist" + str(i)
                    screen.show(szName)

            if pHeadSelectedCity.getSpecialistCount(i) < MAX_CITIZEN_BUTTONS:
                iCount = pHeadSelectedCity.getSpecialistCount(i)
            else:
                iCount = MAX_CITIZEN_BUTTONS

            j = iCount-1

            while j >= 0:
                if j <= 9:
                    bHandled = True
                    szName = "CitizenButton" + str((i * 100) + j)
                    if gc.getSpecialistInfo(i).isVisible():
                        screen.addCheckBoxGFC(szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution + 5 - (74+iXShiftVal) - (SPECIALIST_STACK_WIDTH * j), (yResolution - 253 - (30 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL)
                    else:
                        screen.addCheckBoxGFC(szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution + 5 - 74 - (SPECIALIST_STACK_WIDTH * j), (yResolution - 253 - (30 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL)

                    screen.show(szName)
                    szName = "CitizenButtonHighlight" + str((i * 100) + j)
                    if gc.getSpecialistInfo(i).isVisible():
                        screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution + 5 - (74+iXShiftVal) - (SPECIALIST_STACK_WIDTH * j), (yResolution - 253 - (30 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j)
                    else:
                        screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution + 5 - 74 - (SPECIALIST_STACK_WIDTH * j), (yResolution - 253 - (30 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j)

                    if pHeadSelectedCity.getForceSpecialistCount(i) > j and g_bHighlightForcedSpecialists:
                        screen.show(szName)
                    else:
                        screen.hide(szName)

                elif j <= 20:
                    bHandled = True
                    szName = "CitizenButton" + str((i * 100) + j)
                    if gc.getSpecialistInfo(i).isVisible():
                        screen.addCheckBoxGFC(szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution + 65 - (74+iXShiftVal) - (SPECIALIST_STACK_WIDTH * j), (yResolution - 261 - (30 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL)
                    else:
                        screen.addCheckBoxGFC(szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution + 65 - 74 - (SPECIALIST_STACK_WIDTH * j), (yResolution - 261 - (30 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL)

                    screen.show(szName)
                    szName = "CitizenButtonHighlight" + str((i * 100) + j)
                    if gc.getSpecialistInfo(i).isVisible():
                        screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution + 65 - (74+iXShiftVal) - (SPECIALIST_STACK_WIDTH * j), (yResolution - 261 - (30 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j)
                    else:
                        screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution + 65 - 74 - (SPECIALIST_STACK_WIDTH * j), (yResolution - 261 - (30 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j)

                    if pHeadSelectedCity.getForceSpecialistCount(i) > j and g_bHighlightForcedSpecialists:
                        screen.show(szName)
                    else:
                        screen.hide(szName)

                j = j-1

            if not bHandled:
                szName = "CitizenDisabledButton" + str(i)
                screen.show(szName)

            screen.show("SpecialistBackground")
            screen.show("SpecialistLabel")

        return 0

    # Flunky PAE - fix specialists - start
    def angryCitizenStackWidth(self, currentAngryCitizenCount):
        if currentAngryCitizenCount < 9:
            stackWidth = 25
        elif currentAngryCitizenCount == 9:
            stackWidth = 22
        elif currentAngryCitizenCount == 10:
            stackWidth = 19
        elif currentAngryCitizenCount == 11:
            stackWidth = 17
        elif currentAngryCitizenCount == 12:
            stackWidth = 16
        elif currentAngryCitizenCount == 13:
            stackWidth = 14
        elif currentAngryCitizenCount == 14:
            stackWidth = 13
        elif currentAngryCitizenCount == 15:
            stackWidth = 12
        elif currentAngryCitizenCount == 16:
            stackWidth = 12
        elif currentAngryCitizenCount == 17:
            stackWidth = 11
        elif currentAngryCitizenCount == 18:
            stackWidth = 10
        elif currentAngryCitizenCount == 19:
            stackWidth = 10
        elif currentAngryCitizenCount == 20:
            stackWidth = 9
        elif currentAngryCitizenCount == 21:
            stackWidth = 9
        elif currentAngryCitizenCount == 22:
            stackWidth = 8
        elif currentAngryCitizenCount == 23:
            stackWidth = 8
        elif currentAngryCitizenCount == 24:
            stackWidth = 8
        elif currentAngryCitizenCount == 25:
            stackWidth = 7
        elif currentAngryCitizenCount == 26:
            stackWidth = 7
        elif currentAngryCitizenCount == 27:
            stackWidth = 7
        elif 33 > currentAngryCitizenCount > 27:
            stackWidth = 6
        elif 39 > currentAngryCitizenCount > 32:
            stackWidth = 5
        elif 48 > currentAngryCitizenCount > 38:
            stackWidth = 4
        elif 64 > currentAngryCitizenCount > 47:
            stackWidth = 3
        elif 95 > currentAngryCitizenCount > 63:
            stackWidth = 2
        else:
            stackWidth = 1
        return stackWidth

    def superSpecialistStackWidth(self, currentSuperSpecialistCount):
        stackWidth = self.angryCitizenStackWidth(currentSuperSpecialistCount)
        if g_bStackSuperSpecialists and SUPER_SPECIALIST_STACK_WIDTH > 10:
            stackWidth = SUPER_SPECIALIST_STACK_WIDTH
        if g_bStackSuperSpecialists and g_bDynamicSuperSpecialistsSpacing and currentSuperSpecialistCount > 0:
            stackWidth = 184/currentSuperSpecialistCount
        return stackWidth # min(stackWidth, MAX_SPECIALIST_BUTTON_SPACING)

    # Flunky PAE - fix specialists - end
    # SPECIALIST STACKER        END

    # Will update the game data strings
    def updateGameDataStrings(self):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        screen.hide("ResearchText")
        screen.hide("GoldText")
        screen.hide("TimeText")
        screen.hide("ResearchBar")

        screen.hide("EraText")

# PAE - Great General Bar - start
        screen.hide("GreatGeneralBar")
        screen.hide("GreatGeneralBarText")
        screen.hide("GreatGeneralBarIcon")
# PAE - Great General Bar - end
# PAE - Great Person Bar - start
        screen.hide("GreatPersonBar")
        screen.hide("GreatPersonBarText")
        screen.hide("GreatPersonBarIcon")
# PAE - Great Person Bar - end

# Mod BUG - Bars on single line for higher resolution screens - start
        screen.hide("GreatGeneralBar-w")
        screen.hide("ResearchBar-w")
        screen.hide("GreatPersonBar-w")
# Mod BUG - Bars on single line for higher resolution screens - end

# Mod BUG - Progress Bar - Tick Marks - start
        self.pBarResearchBar_n.hide(screen)
        self.pBarResearchBar_w.hide(screen)
# Mod BUG - Progress Bar - Tick Marks - end

# PAE Taxes Bar
        screen.hide("TaxesBar")
        screen.hide("TaxesBarText")
        screen.hide("TaxesBarButton")

        # bShift = CyInterface().shiftKey()

        xResolution = screen.getXResolution()
        # yResolution = screen.getYResolution()

        pHeadSelectedCity = CyInterface().getHeadSelectedCity()

        if pHeadSelectedCity:
            ePlayer = pHeadSelectedCity.getOwner()
        else:
            ePlayer = gc.getGame().getActivePlayer()

        if ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS():
            return 0

        for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
            szString = "PercentText" + str(iI)
            screen.hide(szString)
            szString = "RateText" + str(iI)
            screen.hide(szString)

        if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL \
           and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY \
           and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START:

            # Taxes | Percent of commerce
            if (CyInterface().isCityScreenUp() or not self.bHideTaxes) and gc.getPlayer(ePlayer).isAlive():
                iCount = 0
                for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
                    eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
                    #if (gc.getPlayer(ePlayer).isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
                    if self.showCommercePercent(eCommerce, ePlayer): # K-Mod
                        szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), gc.getPlayer(ePlayer).getCommercePercent(eCommerce))
                        szString = "PercentText" + str(iI)
                        screen.setLabel(szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 14, 52 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                        screen.show(szString)

                        if not CyInterface().isCityScreenUp():
                            szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (gc.getPlayer(ePlayer).getCommerceRate(CommerceTypes(eCommerce)), )) + u"</font>"
                            szString = "RateText" + str(iI)
# PAE - Min/Max Sliders - start - Alt: 112 Neu: 152
                            iMinMaxAdjustX = 0
                            if MainOpt.isShowMinMaxCommerceButtons():
                                iMinMaxAdjustX = 40
                            screen.setLabel(szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 112 + iMinMaxAdjustX, 52 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
# PAE - Min/Max Sliders - end
                            screen.show(szString)

                        iCount = iCount + 1

            # PAE Taxes Bar
            if not CyInterface().isCityScreenUp():
                szOutText = u"<font=2>%d%%%c</font>" % (gc.getPlayer(ePlayer).getCommercePercent(CommerceTypes.COMMERCE_RESEARCH), gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
                screen.setLabel("TaxesBarText", "Background", szOutText, CvUtil.FONT_CENTER_JUSTIFY, 35, 30, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("TaxesBarText", HitTestTypes.HITTEST_NOHIT)
                screen.show("TaxesBar")
                screen.show("TaxesBarText")
                #screen.show( "TaxesBarButton" )
            # ------

            self.updateTimeText()
            screen.setLabel("TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
            screen.show("TimeText")

            if gc.getPlayer(ePlayer).isAlive():

# Mod BUG - Gold Rate Warning - start
                if MainOpt.isGoldRateWarning():
                    pPlayer = gc.getPlayer(ePlayer)
                    iGold = pPlayer.getGold()
                    iGoldRate = pPlayer.calculateGoldRate()
                    if iGold < 0:
                        szText = BugUtil.getText("TXT_KEY_MISC_NEG_GOLD", iGold)
                        if iGoldRate != 0:
                            if iGold + iGoldRate >= 0:
                                szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate)
                            elif iGoldRate >= 0:
                                szText += BugUtil.getText("TXT_KEY_MISC_POS_WARNING_GOLD_PER_TURN", iGoldRate)
                            else:
                                szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate)
                    else:
                        szText = BugUtil.getText("TXT_KEY_MISC_POS_GOLD", iGold)
                        if iGoldRate != 0:
                            if iGoldRate >= 0:
                                szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate)
                            elif iGold + iGoldRate >= 0:
                                szText += BugUtil.getText("TXT_KEY_MISC_NEG_WARNING_GOLD_PER_TURN", iGoldRate)
                            else:
                                szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate)
                    if pPlayer.isStrike():
                        szText += BugUtil.getPlainText("TXT_KEY_MISC_STRIKE")
                else:
                    szText = CyGameTextMgr().getGoldStr(ePlayer)
# Mod BUG - Gold Rate Warning - end
                screen.setLabel("GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("GoldText")

                if (gc.getPlayer(ePlayer).calculateGoldRate() != 0 and not gc.getPlayer(ePlayer).isAnarchy()) or gc.getPlayer(ePlayer).getGold() != 0:
                    screen.show("GoldText")

                szText = localText.getText("TXT_KEY_BUG_ERA", (gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getDescription(),))
                iEraColor = ClockOpt.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType())
                if iEraColor >= 0:
                    szText = localText.changeTextColor(szText, iEraColor)
                screen.setLabel("EraText", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, 250, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("EraText")

                if gc.getPlayer(ePlayer).isAnarchy():

# Mod BUG - Bars on single line for higher resolution screens - start
                    if xResolution >= 1280:
                        xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
                    else:
                        xCoord = screen.centerX(512)

                    yCoord = 5  # Ruff: this use to be 3 but I changed it so it lines up with the Great Person Bar
                    szText = localText.getText("INTERFACE_ANARCHY", (gc.getPlayer(ePlayer).getAnarchyTurns(), ))
                    screen.setText("ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1)
# Mod BUG - Bars on single line for higher resolution screens - end

                    if gc.getPlayer(ePlayer).getCurrentResearch() != -1:
                        screen.show("ResearchText")
                    else:
                        screen.hide("ResearchText")

                elif gc.getPlayer(ePlayer).getCurrentResearch() != -1:

                    szText = CyGameTextMgr().getResearchStr(ePlayer)

# Mod BUG - Bars on single line for higher resolution screens - start
                    if xResolution >= 1280:
                        szResearchBar = "ResearchBar-w"
                        xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
                    else:
                        szResearchBar = "ResearchBar"
                        # PAE x - 30
                        xCoord = screen.centerX(512) - 30

                    yCoord = 5  # Ruff: this use to be 3 but I changed it so it lines up with the Great Person Bar
                    screen.setText("ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1)
                    screen.show("ResearchText")
# Mod BUG - Bars on single line for higher resolution screens - end

                    researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
                    overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
                    researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
                    researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)

                    iFirst = float(researchProgress + overflowResearch) / float(researchCost)
                    screen.setBarPercentage(szResearchBar, InfoBarTypes.INFOBAR_STORED, iFirst)
                    # PAE
                    if iFirst == 1:
                        screen.setBarPercentage(szResearchBar, InfoBarTypes.INFOBAR_RATE, float(researchRate) / float(researchCost))
                    else:
                        screen.setBarPercentage(szResearchBar, InfoBarTypes.INFOBAR_RATE, (float(researchRate) / float(researchCost)) / (1 - iFirst))
                    # kmod
                    # if researchCost >  researchProgress + overflowResearch:
                        # screen.setBarPercentage(szResearchBar, InfoBarTypes.INFOBAR_RATE, float(researchRate) / float(researchCost - researchProgress - overflowResearch))
                    # else:
                        # screen.setBarPercentage(szResearchBar, InfoBarTypes.INFOBAR_RATE, 0.0)

                    screen.show(szResearchBar)

# Mod BUG - Progress Bar - Tick Marks - start
                    if MainOpt.isShowpBarTickMarks():
                        if szResearchBar == "ResearchBar":
                            self.pBarResearchBar_n.drawTickMarks(screen, researchProgress + overflowResearch, researchCost, researchRate, researchRate, False)
                        else:
                            self.pBarResearchBar_w.drawTickMarks(screen, researchProgress + overflowResearch, researchCost, researchRate, researchRate, False)
# Mod BUG - Progress Bar - Tick Marks - end


                # ERA Text _era era_
                screen.setLabel("EraText", "Background", gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getDescription(), CvUtil.FONT_RIGHT_JUSTIFY, 244, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("EraText")

# PAE - Great Person Bar - start
                self.updateGreatPersonBar(screen)
# PAE - Great Person Bar - end

# PAE - Great General Bar - start
                self.updateGreatGeneralBar(screen)
# PAE - Great General Bar - end

        return 0

# PAE - Great Person Bar - start
    def updateGreatPersonBar(self, screen):
        if not CyInterface().isCityScreenUp():
            pPlayer = gc.getActivePlayer()

            pCity, _ = GPUtil.findNextCity()
            if not pCity:
                return
            iCityPersonRate = pCity.getGreatPeopleRate()
            iCityPersonProgress = pCity.getGreatPeopleProgress()

            if iCityPersonProgress > 0:
                iPlayerTreshold = pPlayer.greatPeopleThreshold(False)

                # Spezialistengeburtenwahrscheinlichkeit herausfinden
                # INT getGreatPeopleUnitProgress (UnitType iIndex)
                # INT getGreatPeopleUnitRate (UnitType iIndex)
                iGreatPersonNum = 0
                iGreatPersonType = -1
                for i in xrange(gc.getNumSpecialistInfos()):
                    if iGreatPersonNum < pCity.getSpecialistCount(i):
                        iGreatPersonNum = pCity.getSpecialistCount(i)
                        iGreatPersonType = i

                # Bei Chancengleichheit allg
                bGleicheChance = False
                for i in xrange(gc.getNumSpecialistInfos()):
                    if iGreatPersonNum == pCity.getSpecialistCount(i) and i != iGreatPersonType:
                        bGleicheChance = True

                szGreatPersonBar = "GreatPersonBar"

                xResolution = screen.getXResolution()
                # >= 1440
                if xResolution >= 1280:
                    xCoord = xResolution - 470
                    yCoord = 7
                else:
                    xCoord = xResolution - 510
                    yCoord = 32

                # General Bar ist bei xResolution - 480 / B = 200
                if bGleicheChance:
                    szText = localText.getText("TXT_NEXT_GP_1", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), 0))
                    screen.setLabel("GreatPersonBarIcon", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord + 12, yCoord, -1.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                else:
                    screen.setImageButton("GreatPersonBarIcon", gc.getSpecialistInfo(iGreatPersonType).getTexture(), xCoord, yCoord - 3, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("GreatPersonBarIcon")

                szText = localText.getText("TXT_NEXT_GP_2", (pCity.getName(), iCityPersonRate, iCityPersonProgress, iPlayerTreshold))

                screen.setLabel("GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord + 106, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("GreatPersonBarText", HitTestTypes.HITTEST_NOHIT)
                screen.show("GreatPersonBarText")

                iFirst = float(iCityPersonProgress) / float(iPlayerTreshold)
                screen.setBarPercentage(szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, iFirst)
                if iFirst == 1:
                    screen.setBarPercentage(szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, (float(iCityPersonRate) / float(iPlayerTreshold)))
                else:
                    screen.setBarPercentage(szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, ((float(iCityPersonRate) / float(iPlayerTreshold))) / (1 - iFirst))
                screen.show(szGreatPersonBar)

# PAE - Great Person Bar - end

# PAE - Great General Bar - start - edited for PAE from BUG
    def updateGreatGeneralBar(self, screen):
        if not CyInterface().isCityScreenUp(): #and MainOpt.isShowGGProgressBar()
            pPlayer = gc.getActivePlayer()
            iCombatExp = pPlayer.getCombatExperience()
            iThresholdExp = pPlayer.greatPeopleThreshold(True)

            szText = u"<font=2>%s</font>" %(localText.getText("TXT_NEXT_GG_EXPERIENCE", (iCombatExp, iThresholdExp)))

# Mod BUG - Bars on single line for higher resolution screens - start
            xResolution = screen.getXResolution()
            if xResolution >= 1280:
                szGreatGeneralBar = "GreatGeneralBar-w"
                xCoord = 270
                yCoord = 7
            else:
                szGreatGeneralBar = "GreatGeneralBar"
                xCoord = 310
                yCoord = 32

            # General Bar ist bei X = 278 / B = 120
            iGeneralIcon = gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")
            screen.setImageButton("GreatGeneralBarIcon", gc.getSpecialistInfo(iGeneralIcon).getTexture(), xCoord, yCoord - 3, 24, 24, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
            screen.show("GreatGeneralBarIcon")
            screen.setLabel("GreatGeneralBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord + 64, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
            screen.show("GreatGeneralBarText")
# Mod BUG - Bars on single line for higher resolution screens - end

            fProgress = float(iCombatExp) / float(iThresholdExp)
            screen.setBarPercentage(szGreatGeneralBar, InfoBarTypes.INFOBAR_STORED, fProgress)
            screen.show(szGreatGeneralBar)
# PAE - Great General Bar - end

    def updateTimeText(self):

        global g_szTimeText

        ePlayer = gc.getGame().getActivePlayer()

# Mod BUG - NJAGC - start
        if ClockOpt.isEnabled():
            """
            Format: Time - GameTurn/Total Percent - GA (TurnsLeft) Date
            Ex: 10:37 - 220/660 33% - GA (3) 1925
            """
            if g_bShowTimeTextAlt:
                bShowTime = ClockOpt.isShowAltTime()
                bShowGameTurn = ClockOpt.isShowAltGameTurn()
                bShowTotalTurns = ClockOpt.isShowAltTotalTurns()
                bShowPercentComplete = ClockOpt.isShowAltPercentComplete()
                bShowDateGA = ClockOpt.isShowAltDateGA()
            else:
                bShowTime = ClockOpt.isShowTime()
                bShowGameTurn = ClockOpt.isShowGameTurn()
                bShowTotalTurns = ClockOpt.isShowTotalTurns()
                bShowPercentComplete = ClockOpt.isShowPercentComplete()
                bShowDateGA = ClockOpt.isShowDateGA()

            if not gc.getGame().getMaxTurns() > 0:
                bShowTotalTurns = False
                bShowPercentComplete = False

            bFirst = True
            g_szTimeText = ""

            if bShowTime:
                bFirst = False
                g_szTimeText += getClockText()

            if bShowGameTurn:
                if bFirst:
                    bFirst = False
                else:
                    g_szTimeText += u" - "
                g_szTimeText += u"%d" %(gc.getGame().getElapsedGameTurns())
                if bShowTotalTurns:
                    g_szTimeText += u"/%d" %(gc.getGame().getMaxTurns())

            if bShowPercentComplete:
                if bFirst:
                    bFirst = False
                else:
                    if not bShowGameTurn:
                        g_szTimeText += u" - "
                    else:
                        g_szTimeText += u" "
                g_szTimeText += u"%2.2f%%" %(100 *(float(gc.getGame().getElapsedGameTurns()) / float(gc.getGame().getMaxTurns())))

            if bShowDateGA:
                if bFirst:
                    bFirst = False
                else:
                    g_szTimeText += u" - "
                # szDateGA = unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
                szDateGA = CyGameTextMgr().getInterfaceTimeStr(ePlayer).decode("utf-8")

                iEraColor = ClockOpt.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType())
                if iEraColor >= 0:
                    szDateGA = localText.changeTextColor(szDateGA, iEraColor)
                g_szTimeText += szDateGA
        else:
            """
            Original Clock
            Format: Time - 'Turn' GameTurn - GA (TurnsLeft) Date

            Ex: 10:37 - Turn 220 - GA (3) 1925
            """

            # g_szTimeText = localText.getText("TXT_KEY_TIME_TURN", (gc.getGame().getGameTurn(), )) + u" - " + unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
            g_szTimeText = localText.getText("TXT_KEY_TIME_TURN", (gc.getGame().getGameTurn(), )) + u" - " + CyGameTextMgr().getInterfaceTimeStr(ePlayer).decode("utf-8")
            if CyUserProfile().isClockOn():
                g_szTimeText = getClockText() + u" - " + g_szTimeText
# Mod BUG - NJAGC - end

    # Will update the selection Data Strings
    def updateCityScreen(self):

        global MAX_DISPLAYABLE_BUILDINGS
        global MAX_DISPLAYABLE_TRADE_ROUTES
        global MAX_BONUS_ROWS

        global g_iNumTradeRoutes
        global g_iNumBuildings
        global g_iNumLeftBonus
        global g_iNumCenterBonus
        global g_iNumRightBonus

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        pHeadSelectedCity = CyInterface().getHeadSelectedCity()

        # Find out our resolution
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        # bShift = CyInterface().shiftKey()

        screen.hide("PopulationBar")
        screen.hide("ProductionBar")
        screen.hide("GreatPeopleBar")
        screen.hide("CultureBar")
        screen.hide("MaintenanceText")
        screen.hide("MaintenanceAmountText")
        screen.hide("PAE_SupplyText")
        screen.hide("PAE_SupplyBar")
        screen.hide("PAE_EmigrationText")
        screen.hide("PAE_EmigrationBar")
        screen.hide("PAE_RevoltText")
        screen.hide("PAE_RevoltBar")
        screen.hide("PAE_SlavesText")
        screen.hide("PAE_SlavesBar")
    #    screen.hide( "PAE_RebellionText" )
    #    screen.hide( "PAE_RebellionBar" )
        screen.hide("PAE_Rebellion2Text")
        screen.hide("PAE_Rebellion2Bar")
        screen.hide("NationalityText")
        screen.hide("NationalityBar")
        screen.hide("DefenseText")
        screen.hide("CityScrollMinus")
        screen.hide("CityScrollPlus")
        screen.hide("CityNameText")
        screen.hide("PopulationText")
        screen.hide("PopulationInputText")
        screen.hide("HealthText")
        screen.hide("ProductionText")
        screen.hide("ProductionInputText")
        screen.hide("HappinessText")
        screen.hide("CultureText")
        screen.hide("GreatPeopleText")

# Mod BUG - Progress Bar - Tick Marks - start
        self.pBarPopulationBar.hide(screen)
        self.pBarProductionBar.hide(screen)
        self.pBarProductionBar_Whip.hide(screen)
# Mod BUG - Progress Bar - Tick Marks - end

# Mod BUG - Raw Commerce - start
        screen.hide("RawYieldsTrade0")
        screen.hide("RawYieldsFood1")
        screen.hide("RawYieldsProduction2")
        screen.hide("RawYieldsCommerce3")
        screen.hide("RawYieldsWorkedTiles4")
        screen.hide("RawYieldsCityTiles5")
        screen.hide("RawYieldsOwnedTiles6")
# Mod BUG - Raw Commerce - end


        for i in xrange(gc.getNumReligionInfos()):
            szName = "ReligionHolyCityDDS" + str(i)
            screen.hide(szName)
            szName = "ReligionDDS" + str(i)
            screen.hide(szName)

        for i in xrange(gc.getNumCorporationInfos()):
            szName = "CorporationHeadquarterDDS" + str(i)
            screen.hide(szName)
            szName = "CorporationDDS" + str(i)
            screen.hide(szName)

        for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
            szName = "CityPercentText" + str(i)
            screen.hide(szName)

        # Bonuspanel BTS changed by Pie
        screen.addPanel("BonusPane0", u"", u"", True, True, xResolution - 244, 94, 60, yResolution - 500, PanelStyles.PANEL_STYLE_CITY_COLUMNL)
        screen.hide("BonusPane0")
        screen.addScrollPanel("BonusBack0", u"", xResolution - 250, 86, 74, yResolution - 560, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.hide("BonusBack0")

        screen.addPanel("BonusPane1", u"", u"", True, True, xResolution - 182, 94, 80, yResolution - 500, PanelStyles.PANEL_STYLE_CITY_COLUMNC)
        screen.hide("BonusPane1")
        screen.addScrollPanel("BonusBack1", u"", xResolution - 188, 86, 100, yResolution - 560, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.hide("BonusBack1")

        screen.addPanel("BonusPane2", u"", u"", True, True, xResolution - 100, 94, 84, yResolution - 500, PanelStyles.PANEL_STYLE_CITY_COLUMNR)
        screen.hide("BonusPane2")
        screen.addScrollPanel("BonusBack2", u"", xResolution - 102, 86, 104, yResolution - 560, PanelStyles.PANEL_STYLE_EXTERNAL)
        screen.hide("BonusBack2")
        # ------------------------

        screen.hide("TradeRouteTable")
        screen.hide("BuildingListTable")

        screen.hide("BuildingListBackground")
        screen.hide("TradeRouteListBackground")
        screen.hide("BuildingListLabel")
        screen.hide("TradeRouteListLabel")

        i = 0
        for i in xrange(g_iNumLeftBonus):
            szName = "LeftBonusItem" + str(i)
            screen.hide(szName)

        i = 0
        for i in xrange(g_iNumCenterBonus):
            szName = "CenterBonusItemLeft" + str(i)
            screen.hide(szName)
            szName = "CenterBonusItemRight" + str(i)
            screen.hide(szName)

        i = 0
        for i in xrange(g_iNumRightBonus):
            szName = "RightBonusItemLeft" + str(i)
            screen.hide(szName)
            szName = "RightBonusItemRight" + str(i)
            screen.hide(szName)

        # Bonuspanel BTS
        i = 0
        for i in xrange(3):
            szName = "BonusPane" + str(i)
            screen.hide(szName)
            szName = "BonusBack" + str(i)
            screen.hide(szName)

        i = 0
        if CyInterface().isCityScreenUp():
            if pHeadSelectedCity:

                pPlot = pHeadSelectedCity.plot()
                iPlayer = pHeadSelectedCity.getOwner()
                pPlayer = gc.getPlayer(iPlayer)
                iCitySlaves = pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE")) + pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")) + pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD"))
                iCityGlads = pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GLADIATOR"))
                iCityPop = pHeadSelectedCity.getPopulation()
                # Revolten-Gefahrenanzeige und -texte (City Statusbar)
                bRevoltDanger = False
                bRevoltWarning = False

                screen.show("InterfaceTopLeftBackgroundWidget")
                screen.show("InterfaceTopRightBackgroundWidget")
                screen.show("InterfaceCenterLeftBackgroundWidget")
                screen.show("CityScreenTopWidget")
                screen.show("CityNameBackground")
                screen.show("TopCityPanelLeft")
                screen.show("TopCityPanelRight")
                screen.show("CityScreenAdjustPanel")
                screen.show("InterfaceCenterRightBackgroundWidget")

                if pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam():
                    if gc.getActivePlayer().getNumCities() > 1:
                        screen.show("CityScrollMinus")
                        screen.show("CityScrollPlus")

                # Help Text Area
                screen.setHelpTextArea(390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0)

                iFoodDifference = pHeadSelectedCity.foodDifference(True)
                iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
                iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

                # PAE city food supply for units / city supply
                #pPlot = gc.getMap().plot(pHeadSelectedCity.getX(), pHeadSelectedCity.getY())
                #iCityUnits = pPlot.getNumDefenders(pHeadSelectedCity.getOwner())
                #iCityPop = pHeadSelectedCity.getPopulation()
                # 1 food for 2 additional units (1 pop serves 1 unit)
                #iUnitFoodConsumption = 0
                #if iCityUnits > iCityPop * 2: iUnitFoodConsumption = (iCityUnits-iCityPop*2) / 2
                #iFoodDifference -= iUnitFoodConsumption

                szBuffer = u"<font=4>"

                if pHeadSelectedCity.isCapital():
                    szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
                elif pHeadSelectedCity.isGovernmentCenter():
                    szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))

                if pHeadSelectedCity.isPower():
                    szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))

                szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())

                if pHeadSelectedCity.isOccupation():
                    szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())

                szBuffer += u"</font>"

                screen.setText("CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1)
                screen.setStyle("CityNameText", "Button_Stone_Style")
                screen.show("CityNameText")

# Mod BUG - Food Assist - start
                if CityUtil.willGrowThisTurn(pHeadSelectedCity) or iFoodDifference != 0 or not pHeadSelectedCity.isFoodProduction():
                    if iFoodDifference > 0:
                        szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))
                    elif iFoodDifference < 0:
                        if CityScreenOpt.isShowFoodAssist():
                            iTurnsToStarve = pHeadSelectedCity.getFood() / -iFoodDifference + 1
                            if iTurnsToStarve > 1:
                                szBuffer = localText.getText("INTERFACE_CITY_SHRINKING", (iTurnsToStarve, ))
                            else:
                                szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())
                        else:
                            szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())
# Mod BUG - Food Assist - end
                    else:
                        szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())

                    screen.setLabel("PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                    screen.setHitTest("PopulationText", HitTestTypes.HITTEST_NOHIT)
                    screen.show("PopulationText")

                if not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction():

# Mod BUG - Food Assist - start
                    if CityScreenOpt.isShowFoodAssist():
                        iFoodYield = pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD)
                        iFoodEaten = pHeadSelectedCity.foodConsumption(False, 0)
                        if iFoodYield == iFoodEaten:
                            szBuffer = localText.getText("INTERFACE_CITY_FOOD_STAGNATE", (iFoodYield, iFoodEaten))
                        elif iFoodYield > iFoodEaten:
                            szBuffer = localText.getText("INTERFACE_CITY_FOOD_GROW", (iFoodYield, iFoodEaten, iFoodYield - iFoodEaten))
                        else:
                            szBuffer = localText.getText("INTERFACE_CITY_FOOD_SHRINK", (iFoodYield, iFoodEaten, iFoodYield - iFoodEaten))
                    else:
                        szBuffer = u"%d%c - %d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD), gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
# Mod BUG - Food Assist - end
                    # draw label below
                else:
                    szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
                    # draw label below
                screen.setLabel("PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.show("PopulationInputText")

                if pHeadSelectedCity.badHealth(False) > 0 or pHeadSelectedCity.goodHealth() >= 0:
                    if pHeadSelectedCity.healthRate(False, 0) < 0:
                        szBuffer = localText.getText("INTERFACE_CITY_HEALTH_BAD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False), pHeadSelectedCity.healthRate(False, 0)))
                    elif pHeadSelectedCity.badHealth(False) > 0:
                        szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False)))
                    else:
                        szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD_NO_BAD", (pHeadSelectedCity.goodHealth(), ))

                    screen.setLabel("HealthText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1)
                    screen.show("HealthText")

                if iFoodDifference < 0:
                    if pHeadSelectedCity.getFood() + iFoodDifference > 0:
                        iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
                        iExtraFood = -iFoodDifference
                    else:
                        iDeltaFood = 0
                        iExtraFood = pHeadSelectedCity.getFood()

                    iFirst = float(iDeltaFood) / float(pHeadSelectedCity.growthThreshold())
                    screen.setBarPercentage("PopulationBar", InfoBarTypes.INFOBAR_STORED, iFirst)
                    screen.setBarPercentage("PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0)

                    if pHeadSelectedCity.growthThreshold() > iDeltaFood:
                        iSecond = float(iExtraFood) / (pHeadSelectedCity.growthThreshold() - iDeltaFood)
                    else:
                        iSecond = 0.0
                    screen.setBarPercentage("PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, iSecond)

                else:
                    iFirst = float(pHeadSelectedCity.getFood()) / float(pHeadSelectedCity.growthThreshold())
                    screen.setBarPercentage("PopulationBar", InfoBarTypes.INFOBAR_STORED, iFirst)

                    if pHeadSelectedCity.growthThreshold() > pHeadSelectedCity.getFood():
                        iSecond = float(iFoodDifference) / (pHeadSelectedCity.growthThreshold() - pHeadSelectedCity.getFood())
                    else:
                        iSecond = 0.0
                    screen.setBarPercentage("PopulationBar", InfoBarTypes.INFOBAR_RATE, iSecond)
                    screen.setBarPercentage("PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)

                screen.show("PopulationBar")

# Mod BUG - Progress Bar - Tick Marks - start
                if MainOpt.isShowpBarTickMarks():
                    self.pBarPopulationBar.drawTickMarks(screen, pHeadSelectedCity.getFood(), pHeadSelectedCity.growthThreshold(), iFoodDifference, iFoodDifference, False)
# Mod BUG - Progress Bar - Tick Marks - end

                if pHeadSelectedCity.getOrderQueueLength() > 0:
                    if pHeadSelectedCity.isProductionProcess():
                        szBuffer = pHeadSelectedCity.getProductionName()
# Mod BUG - Whip Assist - start
                    else:
                        HURRY_WHIP = gc.getInfoTypeForString("HURRY_POPULATION")
                        HURRY_BUY = gc.getInfoTypeForString("HURRY_GOLD")
                        if CityScreenOpt.isShowWhipAssist() and pHeadSelectedCity.canHurry(HURRY_WHIP, False):
                            iHurryPop = pHeadSelectedCity.hurryPopulation(HURRY_WHIP)
                            iOverflow = pHeadSelectedCity.hurryProduction(HURRY_WHIP) - pHeadSelectedCity.productionLeft()
                            if CityScreenOpt.isWhipAssistOverflowCountCurrentProduction():
                                iOverflow += pHeadSelectedCity.getCurrentProductionDifference(False, True)
                            iMaxOverflow = max(pHeadSelectedCity.getProductionNeeded(), pHeadSelectedCity.getCurrentProductionDifference(False, False))
                            iLost = max(0, iOverflow - iMaxOverflow)
                            iOverflow = min(iOverflow, iMaxOverflow)
                            iItemModifier = pHeadSelectedCity.getProductionModifier()
                            iBaseModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_PRODUCTION, 0)
                            iTotalModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_PRODUCTION, iItemModifier)
                            iLost *= iBaseModifier
                            iLost /= max(1, iTotalModifier)
                            iOverflow = (iBaseModifier * iOverflow) / max(1, iTotalModifier)
                            if iLost > 0:
                                if pHeadSelectedCity.isProductionUnit():
                                    iGoldPercent = gc.getDefineINT("MAXED_UNIT_GOLD_PERCENT")
                                elif pHeadSelectedCity.isProductionBuilding():
                                    iGoldPercent = gc.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")
                                elif pHeadSelectedCity.isProductionProject():
                                    iGoldPercent = gc.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")
                                else:
                                    iGoldPercent = 0
                                iOverflowGold = iLost * iGoldPercent / 100
                                szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_WHIP_PLUS_GOLD", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryPop, iOverflow, iOverflowGold))
                            else:
                                szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_WHIP", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryPop, iOverflow))
                        elif CityScreenOpt.isShowWhipAssist() and pHeadSelectedCity.canHurry(HURRY_BUY, False):
                            iHurryCost = pHeadSelectedCity.hurryGold(HURRY_BUY)
                            szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_BUY", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryCost))
                        else:
                            szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))
# Mod BUG - Whip Assist - end

                    screen.setLabel("ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                    screen.setHitTest("ProductionText", HitTestTypes.HITTEST_NOHIT)
                    screen.show("ProductionText")

                if pHeadSelectedCity.isProductionProcess():
                    szBuffer = u"%d%c" % (pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
                elif pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0):
                    szBuffer = u"%d%c + %d%c" % (iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
                else:
                    szBuffer = u"%d%c" % (iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())

                screen.setLabel("ProductionInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1)
                screen.show("ProductionInputText")

                if pHeadSelectedCity.happyLevel() >= 0 or pHeadSelectedCity.unhappyLevel(0) > 0:
                    if pHeadSelectedCity.isDisorder():
                        szBuffer = u"%d%c" % (pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
                    elif pHeadSelectedCity.angryPopulation(0) > 0:
                        szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
                    elif pHeadSelectedCity.unhappyLevel(0) > 0:
                        szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
                    else:
                        szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))

# Mod BUG - Anger Display - start
                    if CityScreenOpt.isShowAngerCounter() and (pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam() or gc.getGame().isDebugMode()): # K-Mod
                        iAngerTimer = max(pHeadSelectedCity.getHurryAngerTimer(), pHeadSelectedCity.getConscriptAngerTimer())
                        if iAngerTimer > 0:
                            szBuffer += u" (%i)" % iAngerTimer
# Mod BUG - Anger Display - end

                    screen.setLabel("HappinessText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1)
                    screen.show("HappinessText")

                if not pHeadSelectedCity.isProductionProcess():

                    iNeeded = pHeadSelectedCity.getProductionNeeded()
                    iStored = pHeadSelectedCity.getProduction()
                    iFirst = float(iStored) / float(iNeeded)
                    screen.setBarPercentage("ProductionBar", InfoBarTypes.INFOBAR_STORED, iFirst)

                    # kmod
                    if iNeeded > iStored:
                        iSecond = float(iProductionDiffNoFood) / (iNeeded - iStored)
                    else:
                        iSecond = 0.0
                    screen.setBarPercentage("ProductionBar", InfoBarTypes.INFOBAR_RATE, iSecond)

                    if iNeeded > iStored + iProductionDiffNoFood:
                        iThird = float(iProductionDiffJustFood) / (iNeeded - iStored - iProductionDiffNoFood)
                    else:
                        iThird = 0.0
                    screen.setBarPercentage("ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, iThird)

                    screen.show("ProductionBar")

# Mod BUG - Progress Bar - Tick Marks - start
                    if MainOpt.isShowpBarTickMarks():
                        if pHeadSelectedCity.isProductionProcess():
                            iFirst = 0
                            iRate = 0
                        elif pHeadSelectedCity.isFoodProduction() and iProductionDiffJustFood > 0:
                            iFirst = pHeadSelectedCity.getCurrentProductionDifference(False, True)
                            iRate = pHeadSelectedCity.getCurrentProductionDifference(False, False)
                        else:
                            iFirst = pHeadSelectedCity.getCurrentProductionDifference(True, True)
                            iRate = pHeadSelectedCity.getCurrentProductionDifference(True, False)
                        self.pBarProductionBar.drawTickMarks(screen, pHeadSelectedCity.getProduction(), pHeadSelectedCity.getProductionNeeded(), iFirst, iRate, False)

                    HURRY_WHIP = gc.getInfoTypeForString("HURRY_POPULATION")
                    if pHeadSelectedCity.canHurry(HURRY_WHIP, True): # K-Mod, changed from False to True
                        iRate = pHeadSelectedCity.hurryProduction(HURRY_WHIP) / pHeadSelectedCity.hurryPopulation(HURRY_WHIP)
                        self.pBarProductionBar_Whip.drawTickMarks(screen, pHeadSelectedCity.getProduction(), pHeadSelectedCity.getProductionNeeded(), iFirst, iRate, True)
# Mod BUG - Progress Bar - Tick Marks - end

                iCount = 0

                # Taxes
                for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
                    eCommerce = (i + 1) % CommerceTypes.NUM_COMMERCE_TYPES
                    if self.showCommercePercent(eCommerce, pHeadSelectedCity.getOwner()): # K-Mod
                        szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce) % 100, gc.getCommerceInfo(eCommerce).getChar())
                        iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)
                        if iHappiness != 0:
                            if iHappiness > 0:
                                szTempBuffer = u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
                            else:
                                szTempBuffer = u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
                            szBuffer = szBuffer + szTempBuffer

                        szName = "CityPercentText" + str(iCount)
                        screen.setLabel(szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 50 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1)
                        screen.show(szName)
                        iCount = iCount + 1

                iCount = 0

                screen.addTableControlGFC("BuildingListTable", 3, 10, 317, 238, yResolution - 642, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)  # nur yResolution: +16 pro Balken
                screen.setStyle("BuildingListTable", "Table_City_Style")

# Mod BUG - Raw Yields - start
                bShowRawYields = g_bYieldView and CityScreenOpt.isShowRawYields()
                if bShowRawYields:
                    screen.addTableControlGFC("TradeRouteTable", 4, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
                    screen.setStyle("TradeRouteTable", "Table_City_Style" )
                    screen.setTableColumnHeader("TradeRouteTable", 0, u"", 110 )
                    screen.setTableColumnHeader("TradeRouteTable", 1, u"", 60 )
                    screen.setTableColumnHeader("TradeRouteTable", 2, u"", 55 )
                    screen.setTableColumnHeader("TradeRouteTable", 3, u"", 10 )
                    screen.setTableColumnRightJustify( "TradeRouteTable", 1 )
                    screen.setTableColumnRightJustify( "TradeRouteTable", 2 )
                else:
                    screen.addTableControlGFC("TradeRouteTable", 3, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
                    screen.setStyle("TradeRouteTable", "Table_City_Style")

                    screen.setTableColumnHeader("TradeRouteTable", 0, u"", 108)
                    screen.setTableColumnHeader("TradeRouteTable", 1, u"", 118)
                    screen.setTableColumnHeader("TradeRouteTable", 2, u"", 10)
                    screen.setTableColumnRightJustify("TradeRouteTable", 1)
# Mod BUG - Raw Yields - end

                screen.setTableColumnHeader("BuildingListTable", 0, u"", 108)
                screen.setTableColumnHeader("BuildingListTable", 1, u"", 118)
                screen.setTableColumnHeader("BuildingListTable", 2, u"", 10)
                screen.setTableColumnRightJustify("BuildingListTable", 1)

                screen.show("BuildingListBackground")
                screen.show("TradeRouteListBackground")
                screen.show("BuildingListLabel")

# Mod BUG - Raw Yields - start
                if CityScreenOpt.isShowRawYields():
                    screen.setState("RawYieldsTrade0", not g_bYieldView)
                    screen.show("RawYieldsTrade0")

                    screen.setState("RawYieldsFood1", g_bYieldView and g_iYieldType == YieldTypes.YIELD_FOOD)
                    screen.show("RawYieldsFood1")
                    screen.setState("RawYieldsProduction2", g_bYieldView and g_iYieldType == YieldTypes.YIELD_PRODUCTION)
                    screen.show("RawYieldsProduction2")
                    screen.setState("RawYieldsCommerce3", g_bYieldView and g_iYieldType == YieldTypes.YIELD_COMMERCE)
                    screen.show("RawYieldsCommerce3")

                    screen.setState("RawYieldsWorkedTiles4", g_iYieldTiles == RawYields.WORKED_TILES)
                    screen.show("RawYieldsWorkedTiles4")
                    screen.setState("RawYieldsCityTiles5", g_iYieldTiles == RawYields.CITY_TILES)
                    screen.show("RawYieldsCityTiles5")
                    screen.setState("RawYieldsOwnedTiles6", g_iYieldTiles == RawYields.OWNED_TILES)
                    screen.show("RawYieldsOwnedTiles6")
                else:
                    screen.show("TradeRouteListLabel")
# Mod BUG - Raw Yields - end

                # Bonuspanel BTS
                for i in xrange(3):
                    szName = "BonusPane" + str(i)
                    screen.show(szName)
                    szName = "BonusBack" + str(i)
                    screen.show(szName)

                i = 0
                iNumBuildings = 0
# Mod BUG - Raw Yields - start
                self.yields = RawYields.Tracker()
# Mod BUG - Raw Yields - end
                for i in xrange(gc.getNumBuildingInfos()):
                    if pHeadSelectedCity.getNumBuilding(i) > 0 and gc.getBuildingInfo(i).getArtDefineTag() != "ART_DEF_BUILDING_FAKE":
                        for k in xrange(pHeadSelectedCity.getNumBuilding(i)):
                            szLeftBuffer = gc.getBuildingInfo(i).getDescription()
                            szRightBuffer = u""
                            bFirst = True

                            # Bonus der aktiven (nicht obsolet) Buildings
                            if pHeadSelectedCity.getNumActiveBuilding(i) > 0:

                                # Trade
                                iValue = gc.getBuildingInfo(i).getTradeRoutes()
                                if iValue > 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False
                                    szTempBuffer = u"+%d%c" %(iValue, CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
                                    szRightBuffer = szRightBuffer + szTempBuffer
                                # Trade modifier in %
                                iValue = gc.getBuildingInfo(i).getTradeRouteModifier()
                                if iValue > 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False
                                    szTempBuffer = u"+%d%s%c" %(iValue, "%", CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
                                    szRightBuffer = szRightBuffer + szTempBuffer

                                # XP
                                iValue = gc.getBuildingInfo(i).getFreeExperience()
                                if iValue > 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False
                                    szTempBuffer = u"+%d%s" %(iValue, "XP")
                                    szRightBuffer = szRightBuffer + szTempBuffer

                            # K-Mod. I've just swapped the order of health / happiness, to match the DLL hover-text.
                                iHappiness = pHeadSelectedCity.getBuildingHappiness(i)
                                if iHappiness != 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False

                                    if iHappiness > 0:
                                        szTempBuffer = u"+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
                                    else:
                                        szTempBuffer = u"+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
                                    szRightBuffer = szRightBuffer + szTempBuffer

                                iHealth = pHeadSelectedCity.getBuildingHealth(i)
                                if iHealth != 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False

                                    if iHealth > 0:
                                        szTempBuffer = u"+%d%c" %(iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
                                    else:
                                        szTempBuffer = u"+%d%c" %(-(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))
                                    szRightBuffer = szRightBuffer + szTempBuffer
                            #K-Mod end

                                # Yieldbonus (Food, Prod, Commerce)
                                for j in xrange(YieldTypes.NUM_YIELD_TYPES):
                                    # Fixwerte
                                    iYield = gc.getBuildingInfo(i).getYieldChange(j) + pHeadSelectedCity.getNumBuilding(i) * pHeadSelectedCity.getBuildingYieldChange(gc.getBuildingInfo(i).getBuildingClassType(), j)
                                    if iYield != 0:
                                        if not bFirst:
                                            szRightBuffer = szRightBuffer + ", "
                                        else:
                                            bFirst = False

                                        if iYield > 0:
                                            szTempBuffer = u"+%d%c" %(iYield, gc.getYieldInfo(j).getChar())
                                        else:
                                            szTempBuffer = u"%d%c" %(iYield, gc.getYieldInfo(j).getChar())
                                        szRightBuffer = szRightBuffer + szTempBuffer

# Mod BUG - Raw Yields - start
                                        self.yields.addBuilding(j, iYield)
# Mod BUG - Raw Yields - end
                                    # Prozent
                                    iYield = gc.getBuildingInfo(i).getYieldModifier(j)
                                    if iYield != 0:
                                        if not bFirst:
                                            szRightBuffer = szRightBuffer + ", "
                                        else:
                                            bFirst = False

                                        if iYield > 0:
                                            szTempBuffer = u"+%d%s%c" %(iYield, "%", gc.getYieldInfo(j).getChar())
                                        else:
                                            szTempBuffer = u"%d%s%c" %(iYield, "%", gc.getYieldInfo(j).getChar())
                                        szRightBuffer = szRightBuffer + szTempBuffer

                            # betrifft hier auch obsolete Buildings
                            # Commercebonus (Gold, Wissen, Kultur, Spionage)
                            for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):

                                # Fixwerte
                                iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i) / pHeadSelectedCity.getNumBuilding(i)
                                if iCommerce != 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False

                                    if iCommerce > 0:
                                        szTempBuffer = u"+%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar())
                                    else:
                                        szTempBuffer = u"%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar())
                                    szRightBuffer = szRightBuffer + szTempBuffer

                                # in Prozent
                                iCommerce = gc.getBuildingInfo(i).getCommerceModifier(j)
                                if iCommerce != 0:
                                    if not bFirst:
                                        szRightBuffer = szRightBuffer + ", "
                                    else:
                                        bFirst = False

                                    if iCommerce > 0:
                                        szTempBuffer = u"+%d%s%c" % (iCommerce, "%", gc.getCommerceInfo(j).getChar())
                                    else:
                                        szTempBuffer = u"%d%s%c" % (iCommerce, "%", gc.getCommerceInfo(j).getChar())
                                    szRightBuffer = szRightBuffer + szTempBuffer


                            # Stadtansicht: Textausgabe
                            szBuffer = szLeftBuffer + "  " + szRightBuffer

                            screen.appendTableRow("BuildingListTable")
                            screen.setTableText("BuildingListTable", 0, iNumBuildings, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
                            screen.setTableText("BuildingListTable", 1, iNumBuildings, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_RIGHT_JUSTIFY)

                            iNumBuildings = iNumBuildings + 1

                if iNumBuildings > g_iNumBuildings:
                    g_iNumBuildings = iNumBuildings

                iNumTradeRoutes = 0

                for i in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
                    pLoopCity = pHeadSelectedCity.getTradeCity(i)

                    if pLoopCity and pLoopCity.getOwner() >= 0:
                        player = gc.getPlayer(pLoopCity.getOwner())
                        szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName())
                        szRightBuffer = u""

                        for j in xrange(YieldTypes.NUM_YIELD_TYPES):
# Mod BUG - Fractional Trade - start
                            iTradeProfit = TradeUtil.calculateTradeRouteYield(pHeadSelectedCity, i, j)

                            if iTradeProfit != 0:
                                if iTradeProfit > 0:
                                    if TradeUtil.isFractionalTrade():
                                        szTempBuffer = u"+%d.%02d%c" %(iTradeProfit // 100,  iTradeProfit % 100, gc.getYieldInfo(j).getChar())
                                    else:
                                        szTempBuffer = u"+%d%c" %(iTradeProfit, gc.getYieldInfo(j).getChar())
                                    szRightBuffer = szRightBuffer + szTempBuffer
                                else:
                                    if TradeUtil.isFractionalTrade():
                                        szTempBuffer = u"%d.%02d%c" %(iTradeProfit // 100,  iTradeProfit % 100, gc.getYieldInfo(j).getChar())
                                    else:
                                        szTempBuffer = u"%d%c" %(iTradeProfit, gc.getYieldInfo(j).getChar())
                                    szRightBuffer = szRightBuffer + szTempBuffer
# Mod BUG - Fractional Trade - end
# Mod BUG - Raw Yields - start
                                if j == YieldTypes.YIELD_COMMERCE:
                                    if pHeadSelectedCity.getTeam() == pLoopCity.getTeam():
                                        self.yields.addDomesticTrade(iTradeProfit)
                                    else:
                                        self.yields.addForeignTrade(iTradeProfit)
# K-Mod: Trade culture
                        iTradeCultureTimes100 = pLoopCity.getTradeCultureRateTimes100(pHeadSelectedCity.getCultureLevel())
                        if iTradeCultureTimes100 >= 20:
                            szTradeCultureBuffer = u"%s%.1f%c" %( "+", iTradeCultureTimes100/100.0, gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
                            szRightBuffer = szRightBuffer + szTradeCultureBuffer
# K-Mod: Trade culture end


                        if not bShowRawYields:
                            screen.appendTableRow("TradeRouteTable")
                            screen.setTableText("TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
                            screen.setTableText("TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY)
# Mod BUG - Raw Yields - end

                        iNumTradeRoutes = iNumTradeRoutes + 1

                if iNumTradeRoutes > g_iNumTradeRoutes:
                    g_iNumTradeRoutes = iNumTradeRoutes

                i = 0
                iLeftCount = 0
                iCenterCount = 0
                iRightCount = 0

                # Bonuspanel BTS changed for PAE
                iRange = gc.getNumBonusInfos()
                for i in xrange(iRange):
                    if pHeadSelectedCity.hasBonus(i):

                        iHealth = pHeadSelectedCity.getBonusHealth(i)
                        iHappiness = pHeadSelectedCity.getBonusHappiness(i)

                        szTextLeft = u"<font=1>%c" %(gc.getBonusInfo(i).getChar())

                        if pHeadSelectedCity.getNumBonuses(i) > 1:
                            szTextLeft += u"(%d)" %(pHeadSelectedCity.getNumBonuses(i))

                        szTextLeft = szTextLeft + "</font>"

                        # Right column
                        if iHealth != 0:
                            if iHealth > 0:
                                szTextRight = u"<font=1>+%d%c</font>" %(iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
                            else:
                                szTextRight = u"<font=1>+%d%c</font>" %(-iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

                            if iHappiness > 0:
                                szTextRight += u"<font=1>, %d%c</font>" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
                            elif iHappiness < 0:
                                szTextRight += u"<font=1>, %d%c</font>" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

                            szName = "RightBonusItemLeft" + str(iRightCount)
                            screen.setLabelAt(szName, "BonusBack2", szTextLeft, CvUtil.FONT_LEFT_JUSTIFY, 0, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)
                            szName = "RightBonusItemRight" + str(iRightCount)
                            screen.setLabelAt(szName, "BonusBack2", szTextRight, CvUtil.FONT_RIGHT_JUSTIFY, 64, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)

                            iRightCount = iRightCount + 1

                        # Mittlere Spalte
                        elif iHappiness != 0:
                            if iHappiness > 0:
                                szTextRight = u"<font=1>%d%c</font>" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
                            else:
                                szTextRight = u"<font=1>%d%c</font>" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

                            # if iHealth > 0:
                            #    szTextRight += u"<font=1>, %d%c</font>" %(iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
                            # elif iHealth < 0:
                            #    szTextRight += u"<font=1>, %d%c</font>" %(-iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

                            szName = "CenterBonusItemLeft" + str(iCenterCount)
                            screen.setLabelAt(szName, "BonusBack1", szTextLeft, CvUtil.FONT_LEFT_JUSTIFY, 0, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)
                            # szName = "CenterBonusItemRight" + str(iCenterCount)
                            # screen.setLabelAt(szName, "BonusBack1", szTextRight, CvUtil.FONT_RIGHT_JUSTIFY, 64, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)

                            iCenterCount = iCenterCount + 1

                        # Linke Spalte
                        else:
                            szName = "LeftBonusItem" + str(iLeftCount)
                            screen.setLabelAt(szName, "BonusBack0", szTextLeft, CvUtil.FONT_LEFT_JUSTIFY, 0, (iLeftCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)

                            iLeftCount = iLeftCount + 1
                # --------------------

                g_iNumLeftBonus = iLeftCount
                g_iNumCenterBonus = iCenterCount
                g_iNumRightBonus = iRightCount

                #iMaintenance = pHeadSelectedCity.getMaintenanceTimes100()
                iMaintenance = pHeadSelectedCity.getMaintenanceTimes100() * (100+gc.getPlayer(pHeadSelectedCity.getOwner()).getInflationRate()) / 100 # K-Mod

                szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())

                screen.setLabel("MaintenanceText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 126, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1)
                screen.show("MaintenanceText")

                szBuffer = u"-%d.%02d %c" % (iMaintenance/100, iMaintenance % 100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
                screen.setLabel("MaintenanceAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 125, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1)
                screen.show("MaintenanceAmountText")

# Mod BUG - Raw Yields - start
                if bShowRawYields:
                    self.yields.processCity(pHeadSelectedCity)
                    self.yields.fillTable(screen, "TradeRouteTable", g_iYieldType, g_iYieldTiles)
# Mod BUG - Raw Yields - end

                szBuffer = u""

                # Alot of this code is just rewriten as it now only shows
                # religions the city has and has to deal with way more then
                lReligions = []
                # if CityScreenOpt.isShowOnlyPresentReligions():
                for eReligion in xrange(gc.getNumReligionInfos()):
                    if pHeadSelectedCity.isHasReligion(eReligion):
                        lReligions.append(eReligion)
                # else:
                    # lReligions = range(gc.getNumReligionInfos())

                iMaxWidth, iMaxButtons, iButtonSize, iButtonSpace = self.getButtonSize(len(lReligions))
                for ii, i in enumerate(lReligions):
                    xCoord = xResolution - 242 + ((ii % iMaxButtons) * (iButtonSize + iButtonSpace))
                    # xCoord = xResolution - 242 + (i * 34) # Original Civ4 Code
                    yCoord = 42 + iButtonSize * (ii // iMaxButtons)
                    # yCoord = 42 # Original Civ4 Code

                    bEnable = True

                    # if pHeadSelectedCity.isHasReligion(i):
                    if pHeadSelectedCity.isHolyCityByType(i):
                        szTempBuffer = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
                        # < 47 Religions Mod Start >
                        # This is now done below since the Holy City Overlay has to be added
                        # after the Religion Icon and can not be shown before its added
                        #szName = "ReligionHolyCityDDS" + str(i)
                        #screen.show( szName )
                        # < 47 Religions Mod Start >
                    else:
                        szTempBuffer = u"%c" %(gc.getReligionInfo(i).getChar())
                    szBuffer = szBuffer + szTempBuffer

                    for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
                        iCommerce = pHeadSelectedCity.getReligionCommerceByReligion(j, i)
                        if iCommerce != 0:
                            if iCommerce > 0:
                                szTempBuffer = u",+%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar())
                            else:
                                szTempBuffer = u",%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar())
                            szBuffer = szBuffer + szTempBuffer

                    iHappiness = pHeadSelectedCity.getReligionHappiness(i)

                    if iHappiness != 0:
                        if iHappiness > 0:
                            szTempBuffer = u",+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
                        else:
                            szTempBuffer = u",+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
                        szBuffer = szBuffer + szTempBuffer

                    szBuffer = szBuffer + " "

                    szButton = gc.getReligionInfo(i).getButton()

                    # end if pHeadSelectedCity.isHasReligion(i):
                    # else:
                    #    bEnable = False
                    #    szButton = gc.getReligionInfo(i).getButton()

                    szName = "ReligionDDS" + str(i)
                    screen.setImageButton(szName, szButton, xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1)
                    screen.enable(szName, bEnable)
                    screen.show(szName)

                    # Holy City Overlay
                    if pHeadSelectedCity.isHolyCityByType(i):
                        szName = "ReligionHolyCityDDS" + str(i)
                        screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1)
                        screen.show(szName)

                # Alot of this code is just rewriten as it now only shows
                # corporations the city has and is setup to handle more then 7
                lCorporations = []
                # if CityScreenOpt.isShowOnlyPresentCorporations():
                for eCorporation in xrange(gc.getNumCorporationInfos()):
                    if pHeadSelectedCity.isHasCorporation(eCorporation):
                        lCorporations.append(eCorporation)
                # else:
                    # lCorporations = range(gc.getNumCorporationInfos())

                iMaxWidth, iMaxButtons, iButtonSize, iButtonSpace = self.getButtonSize(len(lCorporations))
                for ii, i in enumerate(lCorporations):
                    xCoord = xResolution - 242 + ((ii % iMaxButtons) * (iButtonSize + iButtonSpace))
                    # xCoord = xResolution - 242 + (i * 34) # Original Civ4 Code
                    yCoord = 66 + iButtonSize * (ii // iMaxButtons)
                    # yCoord = 66 # Original Civ4 Code

                    bEnable = True

                    # if (pHeadSelectedCity.isHasCorporation(i)):
                    if pHeadSelectedCity.isHeadquartersByType(i):
                        szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
                        #szName = "CorporationHeadquarterDDS" + str(i)
                        #screen.show( szName )
                    else:
                        szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getChar())
                    szBuffer = szBuffer + szTempBuffer

                    for j in xrange(YieldTypes.NUM_YIELD_TYPES):
                        iYield = pHeadSelectedCity.getCorporationYieldByCorporation(j, i)

                        if iYield != 0:
                            if iYield > 0:
                                szTempBuffer = u",+%d%c" %(iYield, gc.getYieldInfo(j).getChar())
                            else:
                                szTempBuffer = u",%d%c" %(iYield, gc.getYieldInfo(j).getChar())
                            szBuffer = szBuffer + szTempBuffer

                    for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
                        iCommerce = pHeadSelectedCity.getCorporationCommerceByCorporation(j, i)

                        if iCommerce != 0:
                            if iCommerce > 0:
                                szTempBuffer = u",+%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar())
                            else:
                                szTempBuffer = u",%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar())
                            szBuffer = szBuffer + szTempBuffer

                    szBuffer += " "
                    szButton = gc.getCorporationInfo(i).getButton()
                    # else:
                    #     bEnable = False
                    #     szButton = gc.getCorporationInfo(i).getButton()
                    szName = "CorporationDDS" + str(i)
                    screen.setImageButton(szName, szButton, xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1)
                    screen.enable(szName, bEnable)
                    screen.show(szName)
                    # Holy City Overlay
                    if pHeadSelectedCity.isHeadquartersByType(i):
                        szName = "CorporationHeadquarterDDS" + str(i)
                        screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1)
                        screen.show(szName)
# Mod BUG - Limit/Extra Corporations - end

                # Allgemeine Variablen fuer Revolten und Rebellionen
                pPlot = pHeadSelectedCity.plot()
                iPlayer = pHeadSelectedCity.getOwner()
                pPlayer = gc.getPlayer(iPlayer)
                # iNumCities = pPlayer.getNumCities()
                # iDistance = plotDistance(pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), pHeadSelectedCity.getX(), pHeadSelectedCity.getY())
                iCitySlaves = pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE")) + pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")) + pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD"))
                iCityGlads = pHeadSelectedCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GLADIATOR"))
                iCityPop = pHeadSelectedCity.getPopulation()

                # Revolten-Gefahrenanzeige und -texte (City Statusbar)
                bRevoltDanger = False
                bRevoltWarning = False
                szBuffer = ""

                if pHeadSelectedCity.isDisorder():
                    szBuffer = localText.getText("TXT_KEY_ANGER_RESISTANCE", ()).upper()
                elif pHeadSelectedCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")):
                    szBuffer = localText.getText("TXT_KEY_CONCEPT_CIVIL_WAR", ()).upper()
                elif pHeadSelectedCity.goodHealth() < pHeadSelectedCity.badHealth(0) and iCityPop > 4:
                    if iCityPop > 8:
                        szBuffer = localText.getText("TXT_KEY_MAIN_UNHEALTHY_PEST", (CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR), ()))
                    else:
                        szBuffer = localText.getText("TXT_KEY_MAIN_UNHEALTHY_LEPRA", (CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR), ()))
                elif iCityGlads + iCitySlaves > iCityPop:
                    if iCityGlads > iCitySlaves:
                        szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_GLADS", (CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), ()))
                    else:
                        szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_SLAVES", (CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), ()))
                elif pHeadSelectedCity.findHighestCulture() != iPlayer and pHeadSelectedCity.findHighestCulture() != gc.getBARBARIAN_PLAYER():
                    if pHeadSelectedCity.getCulturePercentAnger() / 60 > 0:
                        szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_NATIONALITY", (CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR), (pHeadSelectedCity.getCulturePercentAnger() / 60)))
                else:
                    iForeignCulture = 0
                    if pHeadSelectedCity.getOriginalOwner() != iPlayer and pHeadSelectedCity.getOriginalOwner() != gc.getBARBARIAN_PLAYER() and gc.getPlayer(pHeadSelectedCity.getOriginalOwner()).isAlive():
                        iForeignCulture = pHeadSelectedCity.plot().calculateCulturePercent(gc.getPlayer(pHeadSelectedCity.getOriginalOwner()).getTeam())

                    if iForeignCulture > 19:
                        # Chance Kultur/10 - 1% pro Einheit
                        iChance = int(iForeignCulture/10) - pPlot.getNumDefenders(iPlayer)
                        if iChance > 0:
                            szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_ALTE_HEIMAT", (CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR), (iChance)))

                    if szBuffer == "":
                        iRel = pPlayer.getStateReligion()
                        # Is grad Anarchie?
                        if pPlayer.getAnarchyTurns() > 0:
                            szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_ANARCHY", (CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR), ()))
                        # Keine Reli oder Staatsreligion
                        elif iRel != -1 and not pHeadSelectedCity.isHasReligion(iRel):
                            szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_RELIGION", (CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR), ()))
                        # Unhappiness
                        elif pHeadSelectedCity.unhappyLevel(0) > pHeadSelectedCity.happyLevel():
                            szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_UNHAPPY", (CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR), ()))
                        # Hohe Steuern
                        elif pPlayer.getCommercePercent(0) > 50:
                            iChance = int((pPlayer.getCommercePercent(0) - 50) / 5)
                            # Pro Happy Citizen 5% Nachlass
                            iChance = iChance - pHeadSelectedCity.happyLevel() + pHeadSelectedCity.unhappyLevel(0)
                            if iChance > 0:
                                szBuffer = localText.getText("TXT_KEY_MAIN_REVOLT_TAXES", (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), (iChance)))

                    if szBuffer != "" and iCityPop < 4:
                      bRevoltWarning = True

                if szBuffer != "":
                    bRevoltDanger = True
                else:
                    szBuffer = localText.getText("TXT_KEY_MAIN_NO_DANGER", (CyGame().getSymbolID(FontSymbols.HAPPY_CHAR), ()))

                screen.setLabel("PAE_RevoltText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 327, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("PAE_RevoltText", HitTestTypes.HITTEST_NOHIT)
                screen.show("PAE_RevoltText")

                if bRevoltWarning:
                    screen.setStackedBarColorsRGB("PAE_RevoltBar", 0, 255, 255, 0, 100)  # yellow/orange
                elif bRevoltDanger:
                    screen.setStackedBarColorsRGB("PAE_RevoltBar", 0, 255, 0, 0, 100)  # red
                else:
                    screen.setStackedBarColorsRGB("PAE_RevoltBar", 0, 0, 255, 0, 100)  # green
                screen.setBarPercentage("PAE_RevoltBar", 0, 1.0)  # immer 1 !

                screen.show("PAE_RevoltBar")

                # Emigration Bar / Emigrant -----------------------------------
                iTech = gc.getInfoTypeForString("TECH_COLONIZATION")
                iTeam = pPlayer.getTeam()
                pTeam = gc.getTeam(iTeam)
                iChance = 0

                if iPlayer == gc.getBARBARIAN_PLAYER():
                    szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_AB_1", ("",))
                elif not pTeam.isHasTech(iTech):
                    szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_AB_2", ("",))
                elif iCityPop < 6:
                    szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_AB_3", ("",))
                else:
                    iCityUnhappy = pHeadSelectedCity.unhappyLevel(0) - pHeadSelectedCity.happyLevel()
                    iCityUnhealthy = pHeadSelectedCity.badHealth(False) - pHeadSelectedCity.goodHealth()
                    if bRevoltDanger:
                        if iCityUnhappy < 0:
                            iCityUnhappy = 0
                        if iCityUnhealthy < 0:
                            iCityUnhealthy = 0
                        iChance = (iCityUnhappy + iCityUnhealthy) * 4  # * iCityPop

                        if iChance == 0:
                            iChance = 4

                        if iCityUnhappy > 0 and iCityUnhealthy > 0:
                            szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_DANGER_1", ("", iChance))
                        elif iCityUnhappy > 0:
                            szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_DANGER_2", ("", iChance))
                        else:
                            szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_DANGER_3", ("", iChance))
                    else:
                        szBuffer = localText.getText("TXT_KEY_MAIN_EMIGRATE_NO_DANGER", ("",))

                screen.setLabel("PAE_EmigrationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 303, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("PAE_EmigrationText", HitTestTypes.HITTEST_NOHIT)
                screen.show("PAE_EmigrationText")

                # Bar 0 ist Balken von rechts / Bar 1 = Hintergrund
                screen.setStackedBarColorsRGB("PAE_EmigrationBar", 1, 255, 0, 0, 100)  # red
                if iChance > 5:
                    screen.setStackedBarColorsRGB("PAE_EmigrationBar", 0, 255, 255, 0, 100)  # yellow
                else:
                    screen.setStackedBarColorsRGB("PAE_EmigrationBar", 0, 0, 255, 0, 100)  # green
                fPercent = iChance * 0.1
                if fPercent < 0.0:
                    fPercent = 0.0
                screen.setBarPercentage("PAE_EmigrationBar", 0, 1.0 - fPercent)  # 0.8
                screen.setBarPercentage("PAE_EmigrationBar", 1, 1.0)  # immer 1 !

                screen.show("PAE_EmigrationBar")

                # Supply Bar / City supply of units ---------------------------
                # PAE V: Food Prod * 2 (capital: * 3)
                #iCityFoodDifference = pHeadSelectedCity.foodDifference(True)
                iCityUnits = pPlot.getNumDefenders(iPlayer)
                # iCityPop

                #if pHeadSelectedCity.isCapital(): iFactor = 3
                # else: iFactor = 2
                #iFactor = 1
                iCityMaintainUnits = max(pHeadSelectedCity.getYieldRate(0),5) #+ pHeadSelectedCity.getCorporationYield(0) #* iFactor
                #for i in xrange(gc.getNumCorporationInfos()):
                #  iCityMaintainUnits += pHeadSelectedCity.getCorporationYieldByCorporation(0, i)


                #iCityMaintainUnits = iCityFoodDifference * 2 + iCityPop * 2
                #if iCityPop < 3:
                #    iCityMaintainUnits = 10
                #    #screen.setStackedBarColorsRGB("PAE_SupplyBar", 0, 0, 255, 0, 100)  # green
                #    #szBuffer = localText.getText("TXT_KEY_MAIN_CITY_SUPPLY_INFO", ())
                if iCityMaintainUnits - iCityUnits < 0:
                    screen.setStackedBarColorsRGB("PAE_SupplyBar", 0, 255, 0, 0, 100)  # red
                    szBuffer = localText.getText("TXT_KEY_MAIN_CITY_SUPPLY_DANGER", (iCityMaintainUnits, iCityUnits, iCityMaintainUnits))
                else:
                    screen.setStackedBarColorsRGB("PAE_SupplyBar", 0, 0, 255, 0, 100)  # green
                    szBuffer = localText.getText("TXT_KEY_MAIN_CITY_SUPPLY", (iCityMaintainUnits, iCityUnits, iCityMaintainUnits))

                screen.setBarPercentage("PAE_SupplyBar", 0, 1.0)
                screen.setLabel("PAE_SupplyText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 279, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("PAE_SupplyText", HitTestTypes.HITTEST_NOHIT)
                screen.show("PAE_SupplyText")

                screen.show("PAE_SupplyBar")

                # Slaves Bar / City slaves maintenance of units ---------------------------
                # PAE V: allowed Slaves = City Pop !
                # PAE V Patch4: + Kultivierungsanzeige
                # pTeam
                # iCityUnits
                # iCityPop
                # iCitySlaves
                # iCityGlads
                szBuffer = u""

                # Kultivierung/Verbreitung von Bonusresourcen
                # siehe PAE/PAE_Cultivation.py
                szBuffer += u"%d/%d" %(PAE_Cultivation.getCityCultivatedBonuses(pHeadSelectedCity,0), PAE_Cultivation.getCityCultivationAmount(pHeadSelectedCity,0))
                szBuffer += u" %c" % (gc.getBonusInfo(gc.getInfoTypeForString("BONUS_COW")).getChar())
                szBuffer += u"%c  |  " % (gc.getBonusInfo(gc.getInfoTypeForString("BONUS_WHEAT")).getChar())

                # Sklaven und Gladiatoren
                iTech = gc.getInfoTypeForString("TECH_ENSLAVEMENT")
                # iTech2 = gc.getInfoTypeForString("TECH_GLADIATOR")

                iSlaveIcon = gc.getInfoTypeForString("BONUS_SLAVES")
                iGladsIcon = gc.getInfoTypeForString("BONUS_BRONZE")

                szBuffer += u"%d %c " % (iCitySlaves, gc.getBonusInfo(iSlaveIcon).getChar())
                if not pTeam.isHasTech(iTech):
                    szBuffer += localText.getText("TXT_KEY_MAIN_CITY_SLAVES_AB", ("",))
                else:
                    szBuffer += u"%d %c " % (iCityGlads, gc.getBonusInfo(iGladsIcon).getChar())
                    if not pTeam.isHasTech(iTech):
                        szBuffer += localText.getText("TXT_KEY_MAIN_CITY_GLADS_AB", ("",))

                szBuffer += u" (%d/%d)" % (iCitySlaves + iCityGlads, iCityPop)

                if iCitySlaves + iCityGlads > iCityPop:
                    screen.setStackedBarColorsRGB("PAE_SlavesBar", 0, 255, 0, 0, 100)  # red
                else:
                    screen.setStackedBarColorsRGB("PAE_SlavesBar", 0, 0, 255, 0, 100)  # green

                screen.setBarPercentage("PAE_SlavesBar", 0, 1.0)
                screen.setLabel("PAE_SlavesText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 255, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("PAE_SlavesText", HitTestTypes.HITTEST_NOHIT)
                screen.show("PAE_SlavesText")

                screen.show("PAE_SlavesBar")

                # Rebellionsgefahr
        #        iNumCities = gc.getPlayer(iPlayer).getNumCities()
        #        iDistance = plotDistance(gc.getPlayer(iPlayer).getCapitalCity().getX(), gc.getPlayer(iPlayer).getCapitalCity().getY(), pHeadSelectedCity.getX(), pHeadSelectedCity.getY())
        #
        #        # Ab Klassik, wo es eine Hauptstadt geben sollte!
        #        if pHeadSelectedCity.getPopulation() > 4 and (gc.getPlayer(iPlayer).getCurrentEra() >= 3 and iDistance > 10 or (pHeadSelectedCity.getOriginalOwner() != iPlayer and pHeadSelectedCity.getGameTurnAcquired() + 100 > gc.getGame().getGameTurn())):
        #         iBuilding1 = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_PALACE')
        #         if not (pHeadSelectedCity.isHasBuilding(iBuilding1) or pHeadSelectedCity.isCapital()):
        #
        #          iChanceOfRebellion = pPlayer.getNumCities() * 2
        #
        #          iChanceOfRebellion += iDistance * 2
        #
        #          if pHeadSelectedCity.isHasBuilding(CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_COURTHOUSE')): iChanceOfRebellion -= 10
        #
        #          iChanceOfRebellion -= pHeadSelectedCity.getNumNationalWonders() * 10
        #
        #          iChanceOfRebellion -= pHeadSelectedCity.getNumWorldWonders() * 10
        #
        #          iChanceOfRebellion += (pHeadSelectedCity.unhappyLevel(0) - pHeadSelectedCity.happyLevel()) * 10
        #
        #          iChanceOfRebellion += pPlayer.getAnarchyTurns() * 10
        #
        #          iChanceOfRebellion += pHeadSelectedCity.foodDifference(1) * 10
        #
        #          iChanceOfRebellion -= pPlot.getNumUnits() * 10
        #
        #          if not pHeadSelectedCity.isConnectedToCapital(iPlayer): iChanceOfRebellion += 30
        #
        #          if pHeadSelectedCity.getOccupationTimer() > 0: iChanceOfRebellion += pHeadSelectedCity.getOccupationTimer() * 10
        #
        #          if gc.getPlayer(iPlayer).getCapitalCity().getOccupationTimer() > 0: iChanceOfRebellion += pHeadSelectedCity.getOccupationTimer() * 20
        #
        #          if not pHeadSelectedCity.isHasReligion(pPlayer.getStateReligion()): iChanceOfRebellion += 20
        #
        #          if pPlayer.isCivic(1)  or   pPlayer.isCivic(2): iChanceOfRebellion += 10
        #          if pPlayer.isCivic(18): iChanceOfRebellion += 10
        #          if pPlayer.isCivic(16): iChanceOfRebellion += 20
        #          if pPlayer.isCivic(3)  or   pPlayer.isCivic(4) : iChanceOfRebellion -= 20
        #          if pPlayer.isCivic(1)  and  pPlayer.isCivic(9) : iChanceOfRebellion += 10
        #          if pPlayer.isCivic(4)  and  pPlayer.isCivic(8) : iChanceOfRebellion += 10
        #          if pPlayer.isCivic(24) and  pPlayer.isCivic(9) : iChanceOfRebellion += 10
        #          if pPlayer.isCivic(14) and  pPlayer.isCivic(18): iChanceOfRebellion += 10
        #          if pPlayer.isCivic(14) and (pPlayer.isCivic(1)  or pPlayer.isCivic(2)) : iChanceOfRebellion += 10
        #          if pPlayer.isCivic(14) and (pPlayer.isCivic(17) or pPlayer.isCivic(19)): iChanceOfRebellion -= 20
        #
        #          if pPlayer.getCommercePercent(0) > 50: iChanceOfRebellion += pPlayer.getCommercePercent(0) - 50
        #
        #          # Verstaerkung, weil nur jede 4te Runde check
        #          iChanceOfRebellion = iChanceOfRebellion * 3
        #
        #          fPercent = iChanceOfRebellion / 10.0
        #
        #          if fPercent < 0: fPercent = 0.1
        #          elif fPercent > 100: fPercent = 100.0
        #
        #         else:
        #          fPercent = 0.0
        #        else:
        #         fPercent = 0.0
        #
        #
        #        szBuffer = localText.getText("TXT_KEY_MAIN_REBELLION_1", (CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), str(round(fPercent,1)) ))
        #        screen.setLabel( "PAE_RebellionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 287, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        #        screen.setHitTest( "PAE_RebellionText", HitTestTypes.HITTEST_NOHIT )
        #        screen.show( "PAE_RebellionText" )
        #
        #        # Hintergrund ist rot
        #        screen.setStackedBarColorsRGB( "PAE_RebellionBar", 0, 255, 0, 0, 100 ) # red
        #        if fPercent > 4: screen.setStackedBarColorsRGB( "PAE_RebellionBar", 1, 255, 255, 0, 100 ) # yellow
        #        else: screen.setStackedBarColorsRGB( "PAE_RebellionBar", 1, 0, 255, 0, 100 ) # green
        #        screen.setBarPercentage( "PAE_RebellionBar", 0, fPercent / 10 ) # 0.8
        #        screen.setBarPercentage( "PAE_RebellionBar", 1, 1.0 ) # immer 1 !
        #
        #        screen.show( "PAE_RebellionBar" )

                # Stability against the enemy / renegade city )
                # ------ ab PAE V: soll nur mehr Stadt betreffen
                iBuilding = gc.getInfoTypeForString("BUILDING_STADT")
                # Berechnung
                if not pHeadSelectedCity.isCapital() and pHeadSelectedCity.isHasBuilding(iBuilding):
                    # Anz Einheiten im Umkreis von 1 Feld, mit denen man im Krieg ist (military units)
                    iUnitAnzahl = 0
                    for i in xrange(3):
                        for j in xrange(3):
                            loopPlot = gc.getMap().plot(pPlot.getX() + i - 1, pPlot.getY() + j - 1)
                            for iUnit in xrange(loopPlot.getNumUnits()):
                                if loopPlot.getUnit(iUnit).canFight():
                                    if pPlot.getOwner() != -1:  # kann ja garnicht sein, ist schliesslich der Stadtplot. Aber sicher ist sicher.
                                        if gc.getTeam(pPlot.getOwner()).isAtWar(gc.getPlayer(loopPlot.getUnit(iUnit).getOwner()).getTeam()):
                                            iUnitAnzahl += 1

                    # Anz Einheiten in der Stadt (military units)
                    iUnitCity = i = iChanceUnits = 0
                    for i in xrange(pPlot.getNumUnits()):
                        if pPlot.getUnit(i).canFight():
                            iUnitCity += 1
                            # loyal units ?
                            if pPlot.getUnit(i).isHasPromotion(0):
                                iChanceUnits += 3
                            else:
                                iChanceUnits += 1

                    # Verhaeltnis 1:4
                    # gemeinsamen Nenner herausfinden
                    if iUnitAnzahl == iUnitCity:
                        iV1 = iV2 = 1
                    elif iUnitAnzahl < iUnitCity:
                        if iUnitAnzahl < 1:
                            iV1 = 1
                            iV2 = 0
                        else:
                            iV1 = int(iUnitCity / iUnitAnzahl)
                            iV2 = 1
                    else:
                        if iUnitCity < 1:
                            iV1 = 0
                            iV2 = 1
                        else:
                            iV1 = 1
                            iV2 = int(iUnitAnzahl / iUnitCity)

                    # Per defense point +1%
                    iChanceDefense = pHeadSelectedCity.getNaturalDefense() + pHeadSelectedCity.getTotalDefense(0) - pHeadSelectedCity.getDefenseDamage()

                    # Per happy smile +5%
                    iChanceHappiness = (pHeadSelectedCity.happyLevel() - pHeadSelectedCity.unhappyLevel(0)) * 2

                    # Wonders: 1st +20%, 2nd +16%, 3rd +12%, 8, 4, 0
                    iNumNWs = pHeadSelectedCity.getNumNationalWonders()
                    if iNumNWs < 6:
                        iChanceNWs = iNumNWs * (11 - iNumNWs) * 2
                    else:
                        iChanceNWs = 60
                    iNumWWs = pHeadSelectedCity.getNumWorldWonders()
                    if iNumWWs < 6:
                        iChanceWWs = iNumWWs * (11 - iNumWWs) * 2
                    else:
                        iChanceWWs = 60

                    # City population +5% each pop
                    iChancePop = pHeadSelectedCity.getPopulation() * 2

                    # City connected with capital?
                    if not pHeadSelectedCity.isConnectedToCapital(pHeadSelectedCity.getOwner()):
                        iChancePop -= 10
                    else:
                        iChancePop += 10

                    # bei negativ Nahrung - !
                    iChancePop += pHeadSelectedCity.foodDifference(1) * 5

                    # Total
                    iChanceTotal = iChanceUnits + iChanceDefense + iChanceHappiness + iChanceNWs + iChanceWWs + iChancePop - iUnitAnzahl

                    if iUnitAnzahl < iUnitCity * 5 or pHeadSelectedCity.getPopulation() < 2:
                        fPercent = 1.0
                    else:
                        if iChanceTotal < 100:
                            fPercent = iChanceTotal / 100.0
            #           else:
                            # there is always a chance of 1%
            #               iChanceTotal = 99
            #               fPercent = 1.0

                    szBuffer = localText.getText("TXT_KEY_MAIN_REBELLION_2", (iChanceTotal, str(iV1)+":"+str(iV2)))

                else:
                    fPercent = 1.0
                    szBuffer = localText.getText("TXT_KEY_MAIN_REBELLION_3", (CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR), ()))

                screen.setLabel("PAE_Rebellion2Text", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 231, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("PAE_Rebellion2Text", HitTestTypes.HITTEST_NOHIT)
                screen.show("PAE_Rebellion2Text")

                if fPercent < 0.5:
                    screen.setStackedBarColorsRGB("PAE_Rebellion2Bar", 0, 255, 255, 0, 100)  # yellow
                else:
                    screen.setStackedBarColorsRGB("PAE_Rebellion2Bar", 0, 0, 255, 0, 100)  # green
                screen.setStackedBarColorsRGB("PAE_Rebellion2Bar", 1, 255, 0, 0, 100)  # red
                screen.setBarPercentage("PAE_Rebellion2Bar", 0, fPercent)
                screen.setBarPercentage("PAE_Rebellion2Bar", 1, 1.0)

                screen.show("PAE_Rebellion2Bar")

                szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0))
                screen.setLabel("NationalityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 205, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.setHitTest("NationalityText", HitTestTypes.HITTEST_NOHIT)
                screen.show("NationalityText")

                # PAE
                # iRemainder = 0
                # iWhichBar = 0
                # for h in xrange(gc.getMAX_PLAYERS()):
                    # if gc.getPlayer(h).isAlive():
                        # fPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
                        # if fPercent > 0:
                            # fPercent = fPercent / 100.0
                            # screen.setStackedBarColorsRGB(
                                # "NationalityBar",
                                # iWhichBar,
                                # gc.getPlayer(h).getPlayerTextColorR(),
                                # gc.getPlayer(h).getPlayerTextColorG(),
                                # gc.getPlayer(h).getPlayerTextColorB(),
                                # gc.getPlayer(h).getPlayerTextColorA()
                                # )
                            # if iRemainder == 1:
                                # screen.setBarPercentage("NationalityBar", iWhichBar, fPercent)
                            # else:
                                # screen.setBarPercentage("NationalityBar", iWhichBar, fPercent / (1 - iRemainder))
                            # iRemainder += fPercent
                            # iWhichBar += 1
                # kmod
                iRemainder = 100
                iWhichBar = 0
                for h in xrange(gc.getMAX_PLAYERS()):
                    if gc.getPlayer(h).isAlive():
                        fPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
                        if fPercent > 0:
                            screen.setStackedBarColorsRGB(
                                "NationalityBar",
                                iWhichBar,
                                gc.getPlayer(h).getPlayerTextColorR(),
                                gc.getPlayer(h).getPlayerTextColorG(),
                                gc.getPlayer(h).getPlayerTextColorB(),
                                gc.getPlayer(h).getPlayerTextColorA()
                                )

                            screen.setBarPercentage(
                                "NationalityBar",
                                iWhichBar,
                                float(fPercent) / iRemainder
                                )

                            iRemainder -= fPercent
                            iWhichBar += 1

                            if iRemainder <= 0:
                                break
                screen.show("NationalityBar")

                iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)

                if iDefenseModifier != 0:
                    szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))

                    if pHeadSelectedCity.getDefenseDamage() > 0:
                        szTempBuffer = u" (%d%%)" %(((gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage()) * 100) / gc.getMAX_CITY_DEFENSE_DAMAGE())
                        szBuffer = szBuffer + szTempBuffer
                    szNewBuffer = "<font=4>"
                    szNewBuffer = szNewBuffer + szBuffer
                    szNewBuffer = szNewBuffer + "</font>"
                    screen.setLabel("DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 270, 40, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1)
                    screen.show("DefenseText")

                if pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL:
                    iRate = pHeadSelectedCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
                    if iRate % 100 == 0:
                        szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), iRate/100))
                    else:
                        szRate = u"+%d.%02d" % (iRate/100, iRate % 100)
                        szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE_FLOAT", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), szRate))

# Mod BUG - Culture Turns - start
                    if CityScreenOpt.isShowCultureTurns() and iRate > 0:
                        iCultureTimes100 = pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())
                        iCultureLeftTimes100 = 100 * pHeadSelectedCity.getCultureThreshold() - iCultureTimes100
                        # K-Mod (don't display a negative countdown when we pass legendary culture)
                        if iCultureLeftTimes100 > 0:
                        # K-Mod end
                            szBuffer += u"" + localText.getText("INTERFACE_CITY_TURNS", (((iCultureLeftTimes100 + iRate - 1) / iRate),))
# Mod BUG - Culture Turns - end

                    screen.setLabel("CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 182, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                    screen.setHitTest("CultureText", HitTestTypes.HITTEST_NOHIT)
                    screen.show("CultureText")

                if pHeadSelectedCity.getGreatPeopleProgress() > 0 or pHeadSelectedCity.getGreatPeopleRate() > 0:
# Mod BUG - Great Person Turns - start
                    iRate = pHeadSelectedCity.getGreatPeopleRate()
                    if CityScreenOpt.isShowCityGreatPersonInfo():
                        iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
                        szBuffer = GPUtil.getGreatPeopleText(pHeadSelectedCity, iGPTurns, 230, MainOpt.isGPBarTypesNone(), MainOpt.isGPBarTypesOne(), False)
                    else:
                        szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))
                        if CityScreenOpt.isShowGreatPersonTurns() and iRate > 0:
                            iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
                            szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (iGPTurns, ))
# Mod BUG - Great Person Turns - end

                    screen.setLabel("GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 146, yResolution - 176, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                    screen.setHitTest("GreatPeopleText", HitTestTypes.HITTEST_NOHIT)
                    screen.show("GreatPeopleText")

                    iFirst = float(pHeadSelectedCity.getGreatPeopleProgress()) / float(gc.getPlayer(pHeadSelectedCity.getOwner()).greatPeopleThreshold(False))
                    screen.setBarPercentage("GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, iFirst)
                    if iFirst == 1:
                        screen.setBarPercentage("GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, (float(pHeadSelectedCity.getGreatPeopleRate()) / float(gc.getPlayer(pHeadSelectedCity.getOwner()).greatPeopleThreshold(False))))
                    else:
                        screen.setBarPercentage("GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ((float(pHeadSelectedCity.getGreatPeopleRate()) / float(gc.getPlayer(pHeadSelectedCity.getOwner()).greatPeopleThreshold(False)))) / (1 - iFirst))
                    screen.show("GreatPeopleBar")

                iFirst = float(pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())) / float(100 * pHeadSelectedCity.getCultureThreshold())
                screen.setBarPercentage("CultureBar", InfoBarTypes.INFOBAR_STORED, iFirst)
                if iFirst == 1:
                    screen.setBarPercentage("CultureBar", InfoBarTypes.INFOBAR_RATE, (float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold())))
                else:
                    screen.setBarPercentage("CultureBar", InfoBarTypes.INFOBAR_RATE, ((float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()))) / (1 - iFirst))
                screen.show("CultureBar")

        else:
            # Help Text Area
            if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
                screen.setHelpTextArea(350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH)
            else:
                screen.setHelpTextArea(350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH)

            screen.hide("InterfaceTopLeftBackgroundWidget")
            screen.hide("InterfaceTopRightBackgroundWidget")
            screen.hide("InterfaceCenterLeftBackgroundWidget")
            screen.hide("CityScreenTopWidget")
            screen.hide("CityNameBackground")
            screen.hide("TopCityPanelLeft")
            screen.hide("TopCityPanelRight")
            screen.hide("CityScreenAdjustPanel")
            screen.hide("InterfaceCenterRightBackgroundWidget")

            if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
                self.setMinimapButtonVisibility(True)

        return 0

    def getButtonSize(self, iCount):

        iMaxWidth = 250 # 228
        iMaxButtons = iCount
        if iCount < 8:
            iButtonSize = 24
            iButtonSpace = 10
        elif iCount == 8:
            iButtonSize = 24
            iButtonSpace = 5
        elif iCount == 9:
            iButtonSize = 24
            iButtonSpace = 2
        elif iCount == 10:
            iButtonSize = 21
            iButtonSpace = 2
        elif iCount == 11:
            iButtonSize = 20
            iButtonSpace = 1
        elif iCount == 12:
            iButtonSize = 18
            iButtonSpace = 1
        elif iCount == 13:
            iButtonSize = 18
            iButtonSpace = 0
        elif iCount == 14:
            iButtonSize = 16
            iButtonSpace = 0
        elif iCount == 15:
            iButtonSize = 15
            iButtonSpace = 0
        elif iCount == 16:
            iButtonSize = 14
            iButtonSpace = 0
        elif iCount == 17:
            iButtonSize = 13
            iButtonSpace = 0
        elif iCount == 18:
            iButtonSize = 13
            iButtonSpace = 0
        elif 37 > iCount > 18:
            iMaxButtons = 18
            iButtonSize = 13
            iButtonSpace = 0
        elif iCount == 37 or iCount == 38:
            iMaxWidth = 240
            iMaxButtons = int(round(iCount / 2.0, 0))
            iButtonSize = iMaxWidth / iMaxButtons
            iButtonSpace = (iMaxWidth - (iButtonSize * iMaxButtons)) // (iMaxButtons - 1)
        else:
            iMaxButtons = int(round(iCount / 2.0, 0))
            iButtonSize = iMaxWidth / iMaxButtons
            iButtonSpace = (iMaxWidth - (iButtonSize * iMaxButtons)) // (iMaxButtons - 1)
        return iMaxWidth, iMaxButtons, iButtonSize, iButtonSpace

    # Will update the info pane strings
    # PAE VI: changed for more Unit Info lines / PAE Unit Info bottom left
    def updateInfoPaneStrings(self):

        iRow = 0

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        pHeadSelectedCity = CyInterface().getHeadSelectedCity()
        pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

        # xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        # bShift = CyInterface().shiftKey()

        screen.addPanel("SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 162, 280, 156, PanelStyles.PANEL_STYLE_STANDARD) #8,y-140,280,130
        screen.setStyle("SelectedUnitPanel", "Panel_Game_HudStat_Style")
        screen.hide("SelectedUnitPanel")

        screen.addTableControlGFC("SelectedUnitText", 3, 6, yResolution - 132, 188, 122, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD) #3,6,y-109,188,102
        screen.setStyle("SelectedUnitText", "Table_EmptyScroll_Style")
        screen.hide("SelectedUnitText")
        screen.hide("SelectedUnitLabel")
        # PAE Unit Detail Promo Icons:
        # PAE: Unit Combat Type
        screen.hide("SelectedUnitCombatType")
        # PAE Unit Ethnic und Religion
        screen.hide("SelectedUnitEthnic")
        screen.hide("SelectedUnitReligion")
        # PAE Ranking etc
        screen.hide("SelectedUnitLoyalty")
        screen.hide("SelectedBadMoral")
        screen.hide("SelectedUnitCombatRank")
        screen.hide("SelectedUnitRang")
        screen.hide("SelectedUnitTrait")
        screen.hide("SelectedUnitFormation")
        screen.hide("SelectedUnitHero")
        # PAE Trade Infos
        screen.addTableControlGFC("SelectedTradeText", 1, 6, yResolution - 40, 188, 32, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
        screen.setStyle("SelectedTradeText", "Table_EmptyScroll_Style")
        screen.hide("SelectedTradeText")
        # PAE Statthalter Infos
        screen.addTableControlGFC("SelectedStatthalterText", 1, 150, yResolution - 40, 188, 32, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
        screen.setStyle("SelectedStatthalterText", "Table_EmptyScroll_Style")
        screen.hide("SelectedStatthalterText")

        screen.addTableControlGFC("SelectedCityText", 3, 10, yResolution - 139, 183, 128, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
        screen.setStyle("SelectedCityText", "Table_EmptyScroll_Style")
        screen.hide("SelectedCityText")

        for i in xrange(gc.getNumPromotionInfos()):
            szName = "PromotionButton" + str(i)
            screen.hide(szName)
# Mod BUG - Stack Promotions - start
            szName = "PromotionButtonCircle" + str(i)
            screen.hide(szName)
            szName = "PromotionButtonCount" + str(i)
            screen.hide(szName)
# Mod BUG - Stack Promotions - end

    # PAE - Unit Info Bar - start
        UnitBarType = ""
        iValue1 = 0
        iValue2 = 0
        screen.hide("UnitInfoBar")
        screen.hide("UnitInfoBarText")
        screen.hide("UnitInfoBarFlag")
        screen.hide("UnitInfoBarFlag2")
        screen.hide("UnitInfoBar2")
        screen.hide("UnitInfoBar2Text")
    # PAE - Unit Info Bar - end

        if CyEngine().isGlobeviewUp():
            return 0

        if pHeadSelectedCity:
            iOrders = CyInterface().getNumOrdersQueued()

            screen.setTableColumnHeader("SelectedCityText", 0, u"", 121)
            screen.setTableColumnHeader("SelectedCityText", 1, u"", 54)
            screen.setTableColumnHeader("SelectedCityText", 2, u"", 10)
            screen.setTableColumnRightJustify("SelectedCityText", 1)

            for i in xrange(iOrders):
                szLeftBuffer = u""
                szRightBuffer = u""

                if CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN:
                    szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
                    szRightBuffer = "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

                    if CyInterface().getOrderNodeSave(i):
                        szLeftBuffer = u"*" + szLeftBuffer

                elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT:
                    szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
                    szRightBuffer = "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

                elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE:
                    szLeftBuffer = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()
                    szRightBuffer = "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

                elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN:
                    szLeftBuffer = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()

                screen.appendTableRow("SelectedCityText")
                screen.setTableText("SelectedCityText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
                screen.setTableText("SelectedCityText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                screen.show("SelectedCityText")
                screen.show("SelectedUnitPanel")
                iRow += 1

        elif pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:

            screen.setTableColumnHeader("SelectedUnitText", 0, u"", 110) #110
            screen.setTableColumnHeader("SelectedUnitText", 1, u"", 75) #75
            screen.setTableColumnHeader("SelectedUnitText", 2, u"", 10)
            screen.setTableColumnRightJustify("SelectedUnitText", 1)

            if CyInterface().mirrorsSelectionGroup():
                pSelectedGroup = pHeadSelectedUnit.getGroup()
            else:
                pSelectedGroup = 0

            if CyInterface().getLengthSelectionList() > 1:

# Mod BUG - Stack Movement Display - start
                szBuffer = localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), ))
                if MainOpt.isShowStackMovementPoints():
                    iMinMoves = 100000
                    iMaxMoves = 0
                    for i in xrange(CyInterface().getLengthSelectionList()):
                        pUnit = CyInterface().getSelectionUnit(i)
                        if pUnit is not None:
                            iLoopMoves = pUnit.movesLeft()
                            if iLoopMoves > iMaxMoves:
                                iMaxMoves = iLoopMoves
                            if iLoopMoves < iMinMoves:
                                iMinMoves = iLoopMoves
                    if iMinMoves == iMaxMoves:
                        fMinMoves = float(iMinMoves) / gc.getMOVE_DENOMINATOR()
                        szBuffer += u" %.1f%c" % (fMinMoves, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
                    else:
                        fMinMoves = float(iMinMoves) / gc.getMOVE_DENOMINATOR()
                        fMaxMoves = float(iMaxMoves) / gc.getMOVE_DENOMINATOR()
                        szBuffer += u" %.1f - %.1f%c" % (fMinMoves, fMaxMoves, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))

                screen.setText("SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 157, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1)
# Mod BUG - Stack Movement Display - end

                # Mod BUG - Stack Promotions - start
                # + PAE Unit Info Bar inits
                iNumMilitaryUnits = 0
                iNumPromotions = gc.getNumPromotionInfos()
                lPromotionCounts = [0] * iNumPromotions
                iNumUnits = CyInterface().getLengthSelectionList()
                for i in xrange(iNumUnits):
                    pUnit = CyInterface().getSelectionUnit(i)
                    if pUnit:
                        for j in xrange(iNumPromotions):
                            if pUnit.isHasPromotion(j):
                                lPromotionCounts[j] += 1

                        # PAE Unit Info Bar
                        #if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_HEALER"):
                        if pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
                            UnitBarType = "HEALER"
                            iMax = PAE_Unit.getMaxSupply(pUnit)
                            iSup = PAE_Unit.getSupply(pUnit)
                            # CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Current Supply "+str(iSup)+" max Supply "+str(iMax),)), None, 2, None, ColorTypes(10), 0, 0, False, False)
                            iValue1 += iSup
                            iValue2 += iMax

                        elif pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_EMIGRANT"):
                            UnitBarType = "EMIGRANT"
                            sPlayer = CvUtil.getScriptData(pUnit, ["p", "t"])
                            if sPlayer != "":
                                iValue1 = int(sPlayer)
                            else:
                                iValue1 = pUnit.getOwner()

                        # elif pUnit.getUnitType() in L.LTradeUnits:
                        #  UnitBarType = "TRADE"
                        #  iValue1 = CvUtil.getScriptData(pUnit, ["b"], -1)

                        if pUnit.isMilitaryHappiness():
                            iNumMilitaryUnits += 1

                if iNumMilitaryUnits > 19 and UnitBarType != "HEALER":
                    UnitBarType = "NO_HEALER"
                # ------

                iPromotionCount = 0
                for i, iCount in enumerate(lPromotionCounts):
                    if iCount > 0:
                        szName = "PromotionButton" + str(i)
                        x, y = self.setPromotionButtonPosition(szName, iPromotionCount)
                        screen.moveToFront(szName)
                        screen.show(szName)
                        if iCount > 1:
                            szName = "PromotionButtonCircle" + str(iPromotionCount)
                            screen.moveItem(szName, x, y, -0.3)
                            screen.moveToFront(szName)
                            screen.show(szName)
                            szName = "PromotionButtonCount" + str(iPromotionCount)
                            szText = u"<font=2>%d</font>" % iCount
                            screen.setText(szName, "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, x + 18, y + 6, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_ACTION, -1, -1)
                            screen.setHitTest(szName, HitTestTypes.HITTEST_NOHIT)
                            screen.moveToFront(szName)
                            screen.show(szName)
                        iPromotionCount += 1

                if pSelectedGroup == 0 or pSelectedGroup.getLengthMissionQueue() <= 1:
                    if pHeadSelectedUnit:
                        for i in xrange(gc.getNumUnitInfos()):
                            iCount = CyInterface().countEntities(i)
                            # PAE: szLeftBuffer und szRightBuffer vertauscht
                            if iCount > 0:
                                szRightBuffer = u""
                                szLeftBuffer = gc.getUnitInfo(i).getDescription()
                                if iCount > 1:
                                    szRightBuffer = u"(" + str(iCount) + u")"

                                szBuffer = szLeftBuffer + u"  " + szRightBuffer
                                screen.appendTableRow("SelectedUnitText")
                                screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
                                screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                                screen.show("SelectedUnitText")
                                screen.show("SelectedUnitPanel")
                                iRow += 1
            else:
                if pHeadSelectedUnit.getHotKeyNumber() == -1:
                    szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
                else:
                    szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
                if len(szBuffer) > 60:
                    szBuffer = "<font=2>" + szBuffer + "</font>"

                # PAE Unit Info bottom left
                # PAE: Show Unit Type Button
                if pHeadSelectedUnit.getUnitCombatType() > -1:
                    x = 32
                    iUnitCombatType = pHeadSelectedUnit.getUnitCombatType()
                    screen.setImageButton("SelectedUnitCombatType", gc.getUnitCombatInfo(iUnitCombatType).getButton(), 10, yResolution - 160, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iUnitCombatType, -1)
                else:
                    x = 18  # Original

                # PAE change: x  / Original: y - 137
                screen.setText("SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, x, yResolution - 161, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1)

                if pSelectedGroup == 0 or pSelectedGroup.getLengthMissionQueue() <= 1:
                    screen.show("SelectedUnitText")
                    screen.show("SelectedUnitPanel")

                    iNumPromos = gc.getNumPromotionInfos()

                    szBuffer = u""

                    szLeftBuffer = u""
                    szRightBuffer = u""

                    if pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_AIR:
                        if pHeadSelectedUnit.airBaseCombatStr() > 0:
                            szLeftBuffer = localText.getText("INTERFACE_PANE_AIR_STRENGTH", ())
                            if pHeadSelectedUnit.isFighting():
                                szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                            elif pHeadSelectedUnit.isHurt():
                                szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.airBaseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                            else:
                                szRightBuffer = u"%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                    else:
                        if pHeadSelectedUnit.canFight():
                            szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
                            if pHeadSelectedUnit.isFighting():
                                szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                            elif pHeadSelectedUnit.isHurt():
                                szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                            else:
                                szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

                    szBuffer = szLeftBuffer + szRightBuffer
                    if szBuffer:
                        screen.appendTableRow("SelectedUnitText")
                        screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                        screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                        screen.show("SelectedUnitText")
                        screen.show("SelectedUnitPanel")
                        iRow += 1

                    szLeftBuffer = u""
                    szRightBuffer = u""

# Mod BUG - Unit Movement Fraction - start
                    szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
                    if MainOpt.isShowUnitMovementPointsFraction():
                        szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
                        if pHeadSelectedUnit.movesLeft() == 0:
                            szRightBuffer = u"0/" + szRightBuffer
                        elif pHeadSelectedUnit.movesLeft() == pHeadSelectedUnit.baseMoves() * gc.getMOVE_DENOMINATOR():
                            pass
                        else:
                            fCurrMoves = float(pHeadSelectedUnit.movesLeft()) / gc.getMOVE_DENOMINATOR()
                            szRightBuffer = (u"%.1f/" % fCurrMoves) + szRightBuffer
                    else:
                        if (pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0:
                            iDenom = 1
                        else:
                            iDenom = 0
                        iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom)
                        if pHeadSelectedUnit.baseMoves() == iCurrMoves:
                            szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
                        else:
                            szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
# Mod BUG - Unit Movement Fraction - end

                    screen.appendTableRow("SelectedUnitText")
                    screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                    screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                    screen.show("SelectedUnitText")
                    screen.show("SelectedUnitPanel")
                    iRow += 1

                    if pHeadSelectedUnit.getLevel() > 0:

                        szLeftBuffer = localText.getText("INTERFACE_PANE_LEVEL", ())
                        szRightBuffer = u"%d" % (pHeadSelectedUnit.getLevel())

                        screen.appendTableRow("SelectedUnitText")
                        screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                        screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                        screen.show("SelectedUnitText")
                        screen.show("SelectedUnitPanel")
                        iRow += 1

                    if pHeadSelectedUnit.getExperience() > 0 and not pHeadSelectedUnit.isFighting():
                        szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
                        szRightBuffer = u"(%d/%d)" % (pHeadSelectedUnit.getExperience(), pHeadSelectedUnit.experienceNeeded())
                        screen.appendTableRow("SelectedUnitText")
                        screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                        screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                        screen.show("SelectedUnitText")
                        screen.show("SelectedUnitPanel")
                        iRow += 1

                    # PAE Unit Detail Promo Icons:

                    # ZEILE 1 (Staerke)

                    # PAE Combat Ranking
                    iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT1")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        if pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT6")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT6")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT5")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT5")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT4")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT4")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT3")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT2")
                        screen.setImageButton("SelectedUnitCombatRank", gc.getPromotionInfo(iPromo).getButton(), 60, yResolution - 132, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, -1)

                    # PAE War Weariness
                    iPromo = gc.getInfoTypeForString("PROMOTION_MORAL_NEG1")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        if pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG5")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_MORAL_NEG5")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG4")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_MORAL_NEG4")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG3")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_MORAL_NEG3")
                        elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG2")):
                            iPromo = gc.getInfoTypeForString("PROMOTION_MORAL_NEG2")
                        screen.setImageButton("SelectedBadMoral", gc.getPromotionInfo(iPromo).getButton(), 84, yResolution - 132, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, -1)

                    # PAE Loyalty
                    iPromo = gc.getInfoTypeForString("PROMOTION_LOYALITAT")
                    iPromo2 = gc.getInfoTypeForString("PROMOTION_MERCENARY")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        screen.setImageButton("SelectedUnitLoyalty", gc.getPromotionInfo(iPromo).getButton(), 108, yResolution - 132, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo, -1)
                    elif pHeadSelectedUnit.isHasPromotion(iPromo2):
                        screen.setImageButton("SelectedUnitLoyalty", gc.getPromotionInfo(iPromo2).getButton(), 108, yResolution - 132, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo2, -1)

                    # ZEILE 2 (Fortbewegung)

                    # PAE Formation SelectedUnitFormation
                    iPromo = 0
                    for iPromo in xrange(iNumPromos):
                        if "_FORM_" in gc.getPromotionInfo(iPromo).getType() and pHeadSelectedUnit.isHasPromotion(iPromo):
                            screen.setImageButton("SelectedUnitFormation", gc.getPromotionInfo(iPromo).getButton(), 108, yResolution - 107, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo, -1)
                    # Begleitschutz (Handelskarren und Karawanen)
                    iPromo = gc.getInfoTypeForString("PROMOTION_SCHUTZ")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        screen.setImageButton("SelectedUnitFormation", gc.getPromotionInfo(iPromo).getButton(), 108, yResolution - 107, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo, -1)

                    # ZEILE 3 (Stufe)

                    # PAE Trait
                    iPromo = gc.getInfoTypeForString("PROMOTION_TRAIT_AGGRESSIVE")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        screen.setImageButton("SelectedUnitTrait", gc.getPromotionInfo(iPromo).getButton(), 60, yResolution - 82, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo, -1)
                    iPromo = gc.getInfoTypeForString("PROMOTION_TRAIT_MARITIME")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        screen.setImageButton("SelectedUnitTrait", gc.getPromotionInfo(iPromo).getButton(), 84, yResolution - 82, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo, -1)

                    # PAE Unit Ethnic und Religion
                    # if 1 != -1:
                    #   iUnitEthnic = 4 # => pHeadSelectedUnit.getEthnic()
                    #   screen.setImageButton("SelectedUnitEthnic", gc.getCivilizationInfo(iUnitEthnic).getButton(), 84, yResolution - 82, 24, 24, WidgetTypes.WIDGET_GENERAL, 750, iUnitEthnic)
                    # if 1 != -1:
                    #   iUnitReligion = 4 # => pHeadSelectedUnit.getReligion()
                    #   screen.setImageButton("SelectedUnitReligion", gc.getReligionInfo(iUnitReligion).getButton(), 108, yResolution - 82, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION, iUnitReligion, -1)

                    # ZEILE 4 (Erfahrung)

                    # PAE Held
                    iPromo = gc.getInfoTypeForString("PROMOTION_HERO")
                    if pHeadSelectedUnit.isHasPromotion(iPromo):
                        screen.setImageButton("SelectedUnitHero", gc.getPromotionInfo(iPromo).getButton(), 84, yResolution - 58, 24, 24, WidgetTypes.WIDGET_HELP_PROMOTION, iPromo, -1)

                    # PAE Unit Rang Promos
                    iPromo = iNumPromos-1
                    for iPromo in xrange(iNumPromos - 1, 0, -1):
                        if "_TRAIT_" in gc.getPromotionInfo(iPromo).getType():
                            break
                        if "_RANG_" in gc.getPromotionInfo(iPromo).getType():
                            if pHeadSelectedUnit.isHasPromotion(iPromo):
                                screen.setImageButton("SelectedUnitRang", gc.getPromotionInfo(iPromo).getButton(), 108, yResolution - 58, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, -1)
                                break
                    # ----

                    # PAE Cultivation and Trade: Handelskarren/Merchant
                    szText = ""
                    if pHeadSelectedUnit.getUnitType() in L.LTradeUnits + L.LCultivationUnits:
                        szText = localText.getText("TXT_UNIT_INFO_BAR_5", ()) + u" "
                        iValue1 = CvUtil.getScriptData(pHeadSelectedUnit, ["b"], -1)
                        if iValue1 != -1:
                            sBonusDesc = gc.getBonusInfo(iValue1).getDescription()
                            iBonusChar = gc.getBonusInfo(iValue1).getChar()
                            szText += localText.getText("TXT_UNIT_INFO_BAR_4", (iBonusChar, sBonusDesc))
                            iValue2 = CvUtil.getScriptData(pHeadSelectedUnit, ["originCiv"], -1)
                            if iValue2 != -1:
                                szText += " (" + gc.getPlayer(iValue2).getCivilizationShortDescription(0) + ")"
                        else:
                            szText += localText.getText("TXT_KEY_NO_BONUS_STORED", ())

                    # PAE Statthaltereigenschaften (siehe PAE_Unit.initStatthalter)
                    if pHeadSelectedUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_STATTHALTER"):
                        szText = localText.getText("TXT_UNIT_INFO_BAR_7", ()) + u": "
                        iValue = CvUtil.getScriptData(pHeadSelectedUnit, ["typ"], -1)
                        if iValue == 0:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_PHILOSOPHICAL",0) + localText.getText(" (+5 [ICON_RESEARCH])",())
                        elif iValue == 1:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_SPIRITUAL",0) + localText.getText(" (+5 [ICON_CULTURE])",())
                        elif iValue == 2:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_FINANCIAL",0) + localText.getText(" (+5 [ICON_GOLD])",())
                        elif iValue == 3:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_INDUSTRIOUS",0) + localText.getText(" (+5 [ICON_PRODUCTION])",())
                        elif iValue == 4:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_CREATIVE",0) + localText.getText(" (+5 [ICON_COMMERCE])",())
                        elif iValue == 5:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_IMPERIALIST",0) + localText.getText(" (+5 [ICON_ESPIONAGE])",())
                        elif iValue == 6:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_ORGANIZED",0) + localText.getText(" (+2 [ICON_HAPPY])",())
                        elif iValue == 7:
                            szText += localText.getObjectText("TXT_KEY_TRAIT_EXPANSIVE",0) + localText.getText(" (+2 [ICON_HEALTHY])",())

                    if szText != "":
                        if pHeadSelectedUnit.getExperience() == 0:
                            Zeile = "SelectedTradeText"
                        else:
                            Zeile = "SelectedStatthalterText"
                        screen.setTableColumnHeader(Zeile, 0, u"", 300)
                        screen.appendTableRow(Zeile)
                        screen.setTableText(Zeile, 0, 0, szText, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                        screen.show(Zeile)
                    # ----

                    # PAE HEALER and EMIGRANT + Unit Info Bar
                    #if pHeadSelectedUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_HEALER"):
                    if pHeadSelectedUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):

                        # Unit Info Bar rechts oben
                        UnitBarType = "HEALER"
                        iMax = PAE_Unit.getMaxSupply(pHeadSelectedUnit)
                        iSup = PAE_Unit.getSupply(pHeadSelectedUnit)
                        iValue1 += iSup
                        iValue2 += iMax
                        # CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Current Supply "+str(iValue1)+" max Supply "+str(iValue2),)), None, 2, None, ColorTypes(10), 0, 0, False, False)

                        # Transportiert der Versorger ein Heldendenkmal / Siegesdenkmal
                        iBuilding = PAE_Unit.getHeldendenkmal(pHeadSelectedUnit)
                        if iBuilding != -1:
                            szText = localText.getText("TXT_UNIT_INFO_BAR_8",()) + u": %s" % gc.getBuildingInfo(iBuilding).getDescription()
                            screen.setTableColumnHeader("SelectedTradeText", 0, u"", 300)
                            screen.appendTableRow("SelectedTradeText")
                            screen.setTableText("SelectedTradeText", 0, 0, szText, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                            screen.show("SelectedTradeText")

                        else:
                            szLeftBuffer = localText.getText("TXT_UNIT_INFO_BAR_6", ())
                            szRightBuffer = u"(%d/%d)" % (iValue1, iValue2)

                            screen.appendTableRow("SelectedUnitText")
                            screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                            screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                            screen.show("SelectedUnitText")
                            screen.show("SelectedUnitPanel")
                            iRow += 1

                    elif pHeadSelectedUnit.getUnitType() == gc.getInfoTypeForString("UNIT_EMIGRANT"):
                        # Unit Info Bar rechts oben
                        UnitBarType = "EMIGRANT"
                        txt = CvUtil.getScriptData(pHeadSelectedUnit, ["p", "t"])
                        # txt kann "NO_PLAYER" oder eine list mit "NO_PLAYER" enthalten
                        if txt != "" and isinstance(txt, int):
                            iValue1 = txt
                        else:
                            iValue1 = pHeadSelectedUnit.getOwner()

                        # Info links unten im Unit Status Fenster
                        szText = localText.getText("TXT_UNIT_INFO_BAR_1", (gc.getPlayer(iValue1).getCivilizationAdjective(2).capitalize(),0))
                        screen.setTableColumnHeader("SelectedTradeText", 0, u"", 300)
                        screen.appendTableRow("SelectedTradeText")
                        screen.setTableText("SelectedTradeText", 0, 0, szText, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                        screen.show("SelectedTradeText")

                        screen.addFlagWidgetGFC("UnitInfoBarFlag2", 20, yResolution - 90, 40, 100, iValue1, WidgetTypes.WIDGET_FLAG, iValue1, -1)
                        screen.show("UnitInfoBarFlag2")

              # ---

                    # Hidden Promotions: changed by Pie for PAE to avoid info type XY not found errors!
                    lIgnorePromos = [
                        "PROMOTION_COVER4",
                        "PROMOTION_PARADE_SKIRM4",
                        "PROMOTION_PARADE_AXE4",
                        "PROMOTION_PARADE_SWORD4",
                        "PROMOTION_PARADE_SPEAR4",
                        "PROMOTION_FORMATION4",
                        "PROMOTION_SKIRMISH4",
                        "PROMOTION_MEDIC6",
                        "PROMOTION_GUERILLA6",
                        "PROMOTION_WOODSMAN6",
                        "PROMOTION_JUNGLE6",
                        "PROMOTION_SUMPF6",
                        "PROMOTION_CITY_RAIDER6",
                        "PROMOTION_CITY_GARRISON6",
                        "PROMOTION_DRILL5",
                        "PROMOTION_BARRAGE6",
                        "PROMOTION_ACCURACY4",
                        "PROMOTION_FLANKING4",
                        "PROMOTION_OVERRUN4",
                        "PROMOTION_NAVIGATION5",
                        "PROMOTION_PILLAGE6",
                        "PROMOTION_DESERT6",
                        "PROMOTION_FLUCHT4",
                        "PROMOTION_FUROR4"
                    ]

                    iPromotionCount = 0
                    i = 0
                    for i in xrange(iNumPromos):
                        sPromotion = gc.getPromotionInfo(i).getType()

                        # PAE seperate Rankings etc
                        if "_COMBAT" in sPromotion:
                            continue
                        if "_RANG_" in sPromotion:
                            continue
                        if "_LOYAL" in sPromotion:
                            continue
                        if "_TRAIT_" in sPromotion:
                            continue
                        if "_FORM_" in sPromotion:
                            continue
                        if "_MORAL_" in sPromotion:
                            continue
                        if "_MERC" in sPromotion:
                            continue
                        if "_HERO" in sPromotion:
                            continue

                        if pHeadSelectedUnit.isHasPromotion(i):
                            ## Hidden Promotions (Platyping) ##
                            # adapted by Pie to avoid info type XY not found warnings
                            sLast = sPromotion[len(sPromotion)-1]
                            if sLast.isdigit():
                                sPromotion = sPromotion[:len(sPromotion)-1] + str(int(sLast)+1)
                                if sPromotion not in lIgnorePromos:
                                    if gc.getInfoTypeForString(sPromotion) > -1:
                                        if pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString(sPromotion)):
                                            continue
                            ## Hidden Promotions (Platyping) ##
                            szName = "PromotionButton" + str(i)
                            self.setPromotionButtonPosition(szName, iPromotionCount)
                            screen.moveToFront(szName)
                            screen.show(szName)

                            iPromotionCount = iPromotionCount + 1

            if pSelectedGroup:
                iNodeCount = pSelectedGroup.getLengthMissionQueue()
                if iNodeCount > 1:
                    for i in xrange(iNodeCount):
                        szLeftBuffer = u""
                        szRightBuffer = u""

                        if gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild():
                            if i == 0:
                                szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
                                szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))
                            else:
                                szLeftBuffer = u"%s..." % (gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
                        else:
                            szLeftBuffer = u"%s..." % (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

                        szBuffer = szLeftBuffer + "  " + szRightBuffer
                        screen.appendTableRow("SelectedUnitText")
                        screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
                        screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY)
                        screen.show("SelectedUnitText")
                        screen.show("SelectedUnitPanel")
                        iRow += 1

            # PAE: Unit Info Bar (rechts oben)
            if UnitBarType != "":
                self.updateUnitInfoBar(screen, UnitBarType, iValue1, iValue2)
            if UnitBarType == "HEALER":
                self.updateUnitInfoBar2(screen, pHeadSelectedUnit)

        return 0

    # PAE - Unit Info Bar (rechts oben) - start
    def updateUnitInfoBar(self, screen, UnitBarType, iValue1, iValue2):
        # if not CyInterface().isCityScreenUp():
        # pPlayer = gc.getActivePlayer()
        xResolution = screen.getXResolution()
        xCoord = xResolution - 250
        yCoord = 90
        szText = ""
        if UnitBarType == "EMIGRANT":
            szText = localText.getText("TXT_UNIT_INFO_BAR_1", (gc.getPlayer(iValue1).getCivilizationAdjective(2).capitalize(),))
            screen.setLabel("UnitInfoBarText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, xCoord + 40, yCoord + 5, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
            screen.setStackedBarColorsRGB("UnitInfoBar", 1, gc.getPlayer(iValue1).getPlayerTextColorR(), gc.getPlayer(iValue1).getPlayerTextColorG(), gc.getPlayer(iValue1).getPlayerTextColorB(), gc.getPlayer(iValue1).getPlayerTextColorA())
            screen.setBarPercentage("UnitInfoBar", 0, 0.0)  # disable
            screen.addFlagWidgetGFC("UnitInfoBarFlag", xCoord+5, yCoord-20, 30, 80, iValue1, WidgetTypes.WIDGET_FLAG, iValue1, -1)
            screen.show("UnitInfoBarFlag")

        elif UnitBarType == "HEALER":
            szText = localText.getText("TXT_UNIT_INFO_BAR_2", (CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR), iValue1, iValue2))
            screen.setLabel("UnitInfoBarText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, xCoord + 10, yCoord + 5, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
            screen.setStackedBarColorsRGB("UnitInfoBar", 1, 0, 0, 0, 100)  # black
            fPercent = 1.0 / float(iValue2) * float(iValue1)
            if fPercent > 0.0:
                if fPercent < 0.2:
                    screen.setStackedBarColorsRGB("UnitInfoBar", 0, 255, 0, 0, 100)  # red
                if fPercent < 0.5:
                    screen.setStackedBarColorsRGB("UnitInfoBar", 0, 255, 255, 0, 100)  # yellow
                else:
                    screen.setStackedBarColorsRGB("UnitInfoBar", 0, 0, 255, 0, 100)  # green
                screen.setBarPercentage("UnitInfoBar", 0, fPercent)  # 0.8

        elif UnitBarType == "NO_HEALER":
            szText = localText.getText("TXT_UNIT_INFO_BAR_3", (CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR), 0))
            screen.setLabel("UnitInfoBarText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, xCoord + 10, yCoord + 5, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
            screen.setStackedBarColorsRGB("UnitInfoBar", 1, 255, 0, 0, 100)  # red
            screen.setBarPercentage("UnitInfoBar", 0, 0.0)  # disable
        # red = 255,0,0
        # yellow = 255,255,0
        # green = 0,255,0
        # Bar 0 ist Balken von rechts / Bar 1 = Hintergrund
        screen.setBarPercentage("UnitInfoBar", 1, 1.0)  # immer 1 !
        screen.show("UnitInfoBar")
        screen.setHitTest("UnitInfoBarText", HitTestTypes.HITTEST_NOHIT)
        screen.show("UnitInfoBarText")
    # PAE - Unit Info Bar - end

    def updateUnitInfoBar2(self, screen, pUnit):
        # if not CyInterface().isCityScreenUp():
        xResolution = screen.getXResolution()
        xCoord = xResolution - 250
        yCoord = 120

        iSupplyFromPlot = PAE_Unit.getSupplyFromPlot(pUnit.getOwner(), pUnit.plot())
        iSupplyUnitCost = PAE_Unit.getPlotSupplyCost(pUnit.getOwner(), pUnit.plot())

        szBuffer = ""
        if iSupplyFromPlot > 0:
            szBuffer = u"+"
        szBuffer += u"%d" % iSupplyFromPlot
        szText = u"%s: %s %c   " % (localText.getText("TXT_KEY_SUPPLY_ERTRAG", ()), szBuffer, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
        szText += u" %s: -%d %c" % (localText.getText("TXT_KEY_SUPPLY_VERBRAUCH", ()), iSupplyUnitCost, CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
        screen.setLabel("UnitInfoBar2Text", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, xCoord + 10, yCoord + 5, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
        if iSupplyFromPlot < iSupplyUnitCost:
            screen.setStackedBarColorsRGB("UnitInfoBar2", 1, 255, 0, 0, 100)  # red
        else:
            screen.setStackedBarColorsRGB("UnitInfoBar2", 1, 0, 255, 0, 100)  # green
        screen.setBarPercentage("UnitInfoBar2", 0, 0.0)  # disable
        screen.setBarPercentage("UnitInfoBar2", 1, 1.0)  # immer 1 !
        screen.show("UnitInfoBar2")
        screen.setHitTest("UnitInfoBar2Text", HitTestTypes.HITTEST_NOHIT)
        screen.show("UnitInfoBar2Text")
    # PAE - Unit Info Bar 2 - end

    # Will update the scores
    def updateScoreStrings(self):

        # Platy Scoreboard adapted and changed by Pie and debugged by Ramk
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        screen.hide("ScoreBackground")
        screen.hide("ScoreBackground2")
        screen.hide("ScoreRowPlus")
        screen.hide("ScoreRowMinus")
        screen.hide("ScoreWidthPlus")
        screen.hide("ScoreWidthMinus")
        screen.hide("ScoreHidePoints")  # PAE
        if CyEngine().isGlobeviewUp():
            return
        if CyInterface().isCityScreenUp():
            return
        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL:
            return
        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY:
            return
        if not CyInterface().isScoresVisible():
            return

        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        lMasters = []
        lVassals = []
        lPlayers = []
        iRange = gc.getMAX_CIV_PLAYERS()
        for iPlayerX in xrange(iRange):
            if CyInterface().isScoresMinimized():
                if iPlayerX == CyGame().getActivePlayer():
                    lPlayers.append(iPlayerX)
                    break
            else:
                pPlayerX = gc.getPlayer(iPlayerX)
                if pPlayerX.isAlive():
                    iTeamX = pPlayerX.getTeam()
                    pTeamX = gc.getTeam(iTeamX)
                    if pTeamX.isHasMet(CyGame().getActiveTeam()) or CyGame().isDebugMode():
                        if pTeamX.isAVassal():
                            for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
                                if pTeamX.isVassal(iTeamY):
                                    lVassals.append([CyGame().getTeamRank(iTeamY), CyGame().getTeamRank(iTeamX), CyGame().getPlayerRank(iPlayerX), iPlayerX])
                                    break
                        else:
                            lMasters.append([CyGame().getTeamRank(iTeamX), CyGame().getPlayerRank(iPlayerX), iPlayerX])
        lMasters.sort()
        lVassals.sort()
        iOldRank = -1
        for i in lMasters:
            if iOldRank != i[0]:
                for j in lVassals:
                    if j[0] == iOldRank:
                        lPlayers.append(j[3])
                    elif j[0] > iOldRank:
                        break
                iOldRank = i[0]
            lPlayers.append(i[2])

        nRows = len(lPlayers)
        self.iScoreRows = max(0, min(self.iScoreRows, nRows - 1))
        iHeight = min(yResolution - 300, max(1, (nRows - self.iScoreRows)) * 24 + 2)
    #                screen.addTableControlGFC("ScoreBackground", 6, xResolution - self.iScoreWidth - 230, yResolution - iHeight - 180, self.iScoreWidth + 230, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
    #                screen.enableSelect("ScoreBackground", False)
    #                screen.setTableColumnHeader("ScoreBackground", 0, "", self.iScoreWidth)
    #                screen.setTableColumnHeader("ScoreBackground", 1, "", 23)
    #                screen.setTableColumnHeader("ScoreBackground", 2, "", 23)
    #                screen.setTableColumnHeader("ScoreBackground", 3, "", 23)
    #                screen.setTableColumnHeader("ScoreBackground", 4, "", 90)
    #                screen.setTableColumnHeader("ScoreBackground", 5, "", 73)
        screen.addTableControlGFC("ScoreBackground2", 6, xResolution - self.iScoreWidth - 230, yResolution - iHeight - 180, self.iScoreWidth + 230, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
        screen.enableSelect("ScoreBackground2", False)
        screen.setTableColumnHeader("ScoreBackground2", 0, "", self.iScoreWidth)
        screen.setTableColumnHeader("ScoreBackground2", 1, "", 23)
        screen.setTableColumnHeader("ScoreBackground2", 2, "", 23)
        screen.setTableColumnHeader("ScoreBackground2", 3, "", 23)
        screen.setTableColumnHeader("ScoreBackground2", 4, "", 90)
        screen.setTableColumnHeader("ScoreBackground2", 5, "", 73)
        if self.iScoreWidth > 0:
            screen.setButtonGFC("ScoreWidthMinus", "", "", xResolution - 48, yResolution - 179, 17, 17, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
        screen.setButtonGFC("ScoreRowMinus", "", "", xResolution - 70, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
        screen.setButtonGFC("ScoreHidePoints", "", "", xResolution - 90, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
        screen.setButtonGFC("ScoreRowPlus", "", "", xResolution - 110, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
        if self.iScoreWidth < 200:
            screen.setButtonGFC("ScoreWidthPlus", "", "", xResolution - 129, yResolution - 179, 17, 17, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
        for iPlayer in lPlayers:
            #       iRow = screen.appendTableRow("ScoreBackground")
            iRow = screen.appendTableRow("ScoreBackground2")
            pPlayer = gc.getPlayer(iPlayer)
            iTeam = pPlayer.getTeam()
            pTeam = gc.getTeam(iTeam)

            sText1 = u"<font=2>"

            if CyGame().isGameMultiPlayer():
                if not pPlayer.isTurnActive():
                    sText1 += "*"
            if CyGame().isNetworkMultiPlayer():
                sText1 += CyGameTextMgr().getNetStats(iPlayer)
            if pPlayer.isHuman() and CyInterface().isOOSVisible():
                sText1 += u" <color=255,0,0>* %s *</color>" % (CyGameTextMgr().getOOSSeeds(iPlayer))
            if not pTeam.isHasMet(CyGame().getActiveTeam()):
                sText1 += "? "

            #sButton = "INTERFACE_ATTITUDE_BOY"
            # if not pPlayer.isHuman():
            #        lVincent = ["INTERFACE_ATTITUDE_0", "INTERFACE_ATTITUDE_1", "INTERFACE_ATTITUDE_2", "INTERFACE_ATTITUDE_3", "INTERFACE_ATTITUDE_4"]
            #        sButton = lVincent[pPlayer.AI_getAttitude(CyGame().getActivePlayer())]

            # PAE
            # Flunky: don't call AI_getAttitude on ourselves
            sButton = ""
            if gc.getGame().getActivePlayer() != iPlayer and not pPlayer.isHuman():
                iAtt = pPlayer.AI_getAttitude(gc.getGame().getActivePlayer())
                sButton = u"%c" % (CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4 + iAtt)
            # None was: ArtFileMgr.getInterfaceArtInfo(sButton).getPath()
            screen.setTableText("ScoreBackground2", 1, iRow, sButton, None, WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
            #szTempBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pPlayer.getName())
            #screen.setTableText("ScoreBackground2", 2, iRow, szTempBuffer, None, WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
            screen.setTableText("ScoreBackground2", 2, iRow, "", gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
            screen.setTableText("ScoreBackground2", 3, iRow, "", gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton(), WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
            szTempBuffer = u"<color=%d,%d,%d,%d>%s</color>" % (pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pPlayer.getCivilizationShortDescription(0))
            screen.setTableText("ScoreBackground2", 4, iRow, szTempBuffer, None, WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)

            if pTeam.isAVassal():
                sText1 += CyTranslator().getText("[ICON_SILVER_STAR]", ())

            # if iPlayer == CyGame().getActivePlayer():
            #        sText1 += CyTranslator().getText("[ICON_POWER]", ())
            # else:
            if iPlayer != CyGame().getActivePlayer():
                if pTeam.getPower(1) >= gc.getTeam(gc.getGame().getActiveTeam()).getPower(1):
                    sText1 += CyTranslator().getText("[ICON_STRENGTH]", ())
                if pTeam.isDefensivePact(CyGame().getActiveTeam()):
                    sText1 += CyTranslator().getText("[ICON_DEFENSIVEPACT]", ())
                if pTeam.getEspionagePointsAgainstTeam(CyGame().getActiveTeam()) > gc.getTeam(CyGame().getActiveTeam()).getEspionagePointsAgainstTeam(iTeam):
                    sText1 += CyTranslator().getText("[ICON_ESPIONAGE]", ())
                if pTeam.isAtWar(CyGame().getActiveTeam()):
                    #sText1 += CyTranslator().getText("[ICON_OCCUPATION]", ())
                    sText1 += "(" + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_RED")).upper() + ")"
                if pTeam.isOpenBorders(CyGame().getActiveTeam()):
                    sText1 += CyTranslator().getText("[ICON_OPENBORDERS]", ())
                if pPlayer.canTradeNetworkWith(CyGame().getActivePlayer()):
                    sText1 += CyTranslator().getText("[ICON_TRADE]", ())

            iReligion = pPlayer.getStateReligion()
            if iReligion > -1:
                if pPlayer.hasHolyCity(iReligion):
                    sText1 += u"%c" % (gc.getReligionInfo(iReligion).getHolyCityChar())
                else:
                    sText1 += u"%c" % (gc.getReligionInfo(iReligion).getChar())

            if not self.iScoreHidePoints:
                sText1 += u"<color=%d,%d,%d,%d>%d</color>" % (pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), CyGame().getPlayerScore(iPlayer))

            screen.setTableText("ScoreBackground2", 0, iRow, sText1, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

            bEspionageCanSeeResearch = False
            for iMissionLoop in xrange(gc.getNumEspionageMissionInfos()):
                if gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch():
                    bEspionageCanSeeResearch = gc.getPlayer(CyGame().getActivePlayer()).canDoEspionageMission(iMissionLoop, iPlayer, None, -1)
                    break

            if iTeam == CyGame().getActiveTeam() or pTeam.isVassal(CyGame().getActiveTeam()) or CyGame().isDebugMode() or bEspionageCanSeeResearch:
                iTech = pPlayer.getCurrentResearch()
                if iTech > -1:
                    sTech = u"<color=%d,%d,%d,%d>%d</color>" % (pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pPlayer.getResearchTurnsLeft(pPlayer.getCurrentResearch(), True))
                    screen.setTableText("ScoreBackground2", 5, iRow, sTech, gc.getTechInfo(iTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, CvUtil.FONT_LEFT_JUSTIFY)
    # Platy Scoreboard - End

    # Will update the scores - TEAMS Ansicht
    def updateScoreStrings_PAEIV(self):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        screen.hide("ScoreBackground")
        screen.hide("ScoreBackground2")

        for i in xrange(gc.getMAX_PLAYERS()):
            szName = "ScoreText" + str(i)
            screen.hide(szName)

        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL \
            or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY:
            return
        if not CyInterface().isScoresVisible() \
            or CyInterface().isCityScreenUp() \
            or CyEngine().isGlobeviewUp():
            return

        iWidth = 0
        iCount = 0
        iBtnHeight = 22

        for i in xrange(gc.getMAX_CIV_TEAMS()-1, -1, -1):
            eTeam = gc.getGame().getRankTeam(i)

            # PBMod: show only players we met
            if gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getGame().isDebugMode():
                for j in xrange(gc.getMAX_CIV_PLAYERS()-1, -1, -1):
                    ePlayer = gc.getGame().getRankPlayer(j)
                    pPlayer = gc.getPlayer(ePlayer)
                    if CyInterface().isScoresMinimized() and gc.getGame().getActivePlayer() != ePlayer:
                        continue

# Mod BUG - Minor Civs - start
                    if pPlayer.isMinorCiv() and not ScoreOpt.isShowMinorCivs():
                        continue
# Mod BUG - Minor Civs - end
# Mod BUG - Dead Civs - start
                    if not pPlayer.isEverAlive():
                        continue
                    if pPlayer.isBarbarian():
                        continue
                    if not pPlayer.isAlive() and not ScoreOpt.isShowDeadCivs():
                        continue
# Mod BUG - Dead Civs - end
                    if pPlayer.getTeam() != eTeam:
                        continue

                    szBuffer = u"<font=2>"

                    if gc.getGame().isGameMultiPlayer():
                        if not pPlayer.isTurnActive():
                            szBuffer = szBuffer + "*"

                    # Leadername OR Civname (Leadername) OR Civname
                    # szPlayerName = gc.getPlayer(ePlayer).getName() # Original
                    # szPlayerName = gc.getPlayer(ePlayer).getCivilizationDescription(0) + " (" + gc.getPlayer(ePlayer).getName() + ")" # PAE currently
                    # szPlayerName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)

                    if ScoreOpt.isUsePlayerName():
                        szPlayerName = pPlayer.getName()
                    else:
                        szPlayerName = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription()

                    if ScoreOpt.isShowBothNames():
                        szCivName = pPlayer.getCivilizationDescription(0)
                        szPlayerName = szPlayerName + "/" + szCivName
                    elif ScoreOpt.isShowBothNamesShort():
                        szCivName = pPlayer.getCivilizationShortDescription(0)
                        szPlayerName = szPlayerName + "/" + szCivName
                    elif ScoreOpt.isShowLeaderName():
                        szPlayerName = szPlayerName
                    elif ScoreOpt.isShowCivName():
                        szCivName = pPlayer.getCivilizationShortDescription(0)
                        szPlayerName = szCivName
                    else:
                        szCivName = pPlayer.getCivilizationDescription(0)
                        szPlayerName = szCivName

# Mod BUG - Dead Civs - start
                    if not pPlayer.isAlive() and ScoreOpt.isShowDeadTag():
                        szPlayerScore = localText.getText("TXT_KEY_BUG_DEAD_CIV", ())
                    else:
                        iScore = gc.getGame().getPlayerScore(ePlayer)
                        szPlayerScore = u"%d" % iScore
# Mod BUG - Score Delta - start
                        if ScoreOpt.isShowScoreDelta():
                            iGameTurn = gc.getGame().getGameTurn()
                            if ePlayer >= gc.getGame().getActivePlayer():
                                iGameTurn -= 1
                            if ScoreOpt.isScoreDeltaIncludeCurrentTurn():
                                iScoreDelta = iScore
                            elif iGameTurn >= 0:
                                iScoreDelta = pPlayer.getScoreHistory(iGameTurn)
                            else:
                                iScoreDelta = 0
                            iPrevGameTurn = iGameTurn - 1
                            if iPrevGameTurn >= 0:
                                iScoreDelta -= pPlayer.getScoreHistory(iPrevGameTurn)
                            if iScoreDelta != 0:
                                if iScoreDelta > 0:
                                    iColorType = gc.getInfoTypeForString("COLOR_GREEN")
                                elif iScoreDelta < 0:
                                    iColorType = gc.getInfoTypeForString("COLOR_RED")
                                szScoreDelta = "%+d" % iScoreDelta
                                if iColorType >= 0:
                                    szScoreDelta = localText.changeTextColor(szScoreDelta, iColorType)
                                szPlayerScore += szScoreDelta + u" "
# Mod BUG - Score Delta - end

                    if not CyInterface().isFlashingPlayer(ePlayer) or CyInterface().shouldFlash(ePlayer):
                        if ePlayer == gc.getGame().getActivePlayer():
                            szPlayerName = u"[<color=%d,%d,%d,%d>%s</color>]" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), szPlayerName)
                        elif not gc.getPlayer(ePlayer).isAlive() and ScoreOpt.isGreyOutDeadCivs():
                            szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(175, 175, 175, pPlayer.getPlayerTextColorA(), szPlayerName)
                        else:
                            szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), szPlayerName)
                    szTempBuffer = u"%s: %s" %(szPlayerScore, szPlayerName)
                    szBuffer = szBuffer + szTempBuffer

                    if pPlayer.isAlive():
                        if gc.getTeam(eTeam).isAlive():
                            if gc.getTeam(eTeam).isAtWar(gc.getGame().getActiveTeam()):
                                szBuffer = szBuffer + "(" + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_RED")).upper() + ")"
                            if pPlayer.canTradeNetworkWith(gc.getGame().getActivePlayer()) and (ePlayer != gc.getGame().getActivePlayer()):
                                szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
                                szBuffer = szBuffer + szTempBuffer
                            if gc.getTeam(eTeam).isOpenBorders(gc.getGame().getActiveTeam()):
                                szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
                                szBuffer = szBuffer + szTempBuffer
                            if gc.getTeam(eTeam).isDefensivePact(gc.getGame().getActiveTeam()):
                                szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
                                szBuffer = szBuffer + szTempBuffer

                            if GameUtil.isEspionage() and gc.getTeam(eTeam).getEspionagePointsAgainstTeam(gc.getGame().getActiveTeam()) < gc.getTeam(gc.getGame().getActiveTeam()).getEspionagePointsAgainstTeam(eTeam):
                                szTempBuffer = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
                                szBuffer = szBuffer + szTempBuffer

                            if pPlayer.getStateReligion() != -1:
                                if gc.getPlayer(ePlayer).hasHolyCity(pPlayer.getStateReligion()):
                                    szTempBuffer = u"%c" %(gc.getReligionInfo(pPlayer.getStateReligion()).getHolyCityChar())
                                else:
                                    szTempBuffer = u"%c" %(gc.getReligionInfo(pPlayer.getStateReligion()).getChar())
                                szBuffer = szBuffer + szTempBuffer

                        # K-Mod (original code deleted)
                        if gc.getGame().isDebugMode() \
                            or (gc.getActivePlayer().canSeeResearch(ePlayer) \
                                and (pPlayer.getTeam() != gc.getGame().getActiveTeam() \
                                    or gc.getTeam(gc.getGame().getActiveTeam()).getNumMembers() > 1)):
                        # K-Mod end
                            if pPlayer.getCurrentResearch() != -1:
                                szTempBuffer = u"-%s (%d)" %(gc.getTechInfo(pPlayer.getCurrentResearch()).getDescription(), pPlayer.getResearchTurnsLeft(pPlayer.getCurrentResearch(), True))
                                szBuffer = szBuffer + szTempBuffer
# Mod BUG - Dead Civs - end
# Attitude Icons - start smileys
                        if not pPlayer.isHuman() and gc.getGame().getActivePlayer() != ePlayer:
                            iAtt = pPlayer.AI_getAttitude(gc.getGame().getActivePlayer())
                            szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4 + iAtt)
                            szBuffer = szBuffer + szTempBuffer
# Attitude Icons - end
# Mod BUG - Refuses to Talk - start
                        if not PlayerUtil.isWillingToTalk(ePlayer, gc.getGame().getActivePlayer()):
                            cRefusesToTalk = u"!"
                            szBuffer += cRefusesToTalk
# Mod BUG - Refuses to Talk - end

# Mod BUG - Worst Enemy - start
                        if ScoreOpt.isShowWorstEnemy():
                            if AttitudeUtil.isWorstEnemy(ePlayer, gc.getGame().getActivePlayer()):
                                cWorstEnemy = u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
                                szBuffer += cWorstEnemy
# Mod BUG - Worst Enemy - end
# Mod BUG - WHEOOH - start
                        if ScoreOpt.isShowWHEOOH():
                            if PlayerUtil.isWHEOOH(ePlayer, PlayerUtil.getActivePlayerID()):
                                szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR))
                                szBuffer = szBuffer + szTempBuffer
# Mod BUG - WHEOOH - end
# Mod BUG - Num Cities - start
                        if ScoreOpt.isShowCountCities():
                            # if PlayerUtil.canSeeCityList(ePlayer):
                                # szTempBuffer = u"%d" % PlayerUtil.getNumCities(ePlayer)
                            # else:
                                # szTempBuffer = BugUtil.colorText(u"%d" % PlayerUtil.getNumRevealedCities(ePlayer), "COLOR_CYAN")
                            # K-Mod. count revealed cities only.
                            if gc.getGame().isDebugMode():
                                szTempBuffer = u"%d" % gc.getPlayer(ePlayer).getNumCities()
                            else:
                                szTempBuffer = u"%d" % PlayerUtil.getNumRevealedCities(ePlayer)
                            # K-Mod end
                            szBuffer = szBuffer + " " + szTempBuffer
# Mod BUG - Num Cities - end

                    if CyGame().isNetworkMultiPlayer():
                        szBuffer = szBuffer + CyGameTextMgr().getNetStats(ePlayer)

                    if pPlayer.isHuman() and CyInterface().isOOSVisible():
                        szTempBuffer = u" <color=255,0,0>* %s *</color> (%d)" %(CyGameTextMgr().getOOSSeeds(ePlayer), CyGame().getTurnSlice()%8) # K-Mod, added TurnSlice
                        szBuffer = szBuffer + szTempBuffer

                    szBuffer = szBuffer + "</font>"

                    if CyInterface().determineWidth(szBuffer) > iWidth:
                        iWidth = CyInterface().determineWidth(szBuffer)

                    szName = "ScoreText" + str(ePlayer)
                    if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart():
                        yCoord = yResolution - 206
                    else:
                        yCoord = yResolution - 88

# Mod BUG - Dead Civs - start
                    # Don't try to contact dead civs
                    if pPlayer.isAlive():
                        iWidgetType = WidgetTypes.WIDGET_CONTACT_CIV
                        iPlayer = ePlayer
                    else:
                        iWidgetType = WidgetTypes.WIDGET_GENERAL
                        iPlayer = -1
                    screen.setText(szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - (iCount * iBtnHeight), -0.3, FontTypes.SMALL_FONT, iWidgetType, iPlayer, -1)
# Mod BUG - Dead Civs - end
                    screen.show(szName)

                    CyInterface().checkFlashReset(ePlayer)

                    iCount = iCount + 1

        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart():
            yCoord = yResolution - 186
        else:
            yCoord = yResolution - 68
        screen.setPanelSize("ScoreBackground", xResolution - 21 - iWidth, yCoord - (iBtnHeight * iCount) - 4, iWidth + 12, (iBtnHeight * iCount) + 8)
        screen.show("ScoreBackground")

    # Will update the help Strings
    def updateHelpStrings(self):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL:
            screen.setHelpTextString("")
        else:
            screen.setHelpTextString(CyInterface().getHelpString())

        return 0

    # Will set the promotion button position
    def setPromotionButtonPosition(self, szName, iPromotionCount):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

# Mod BUG - Stack Promotions - start
        x, y = self.calculatePromotionButtonPosition(screen, iPromotionCount)
        screen.moveItem(szName, x, y, -0.3)
        return x, y
# Mod BUG - Stack Promotions - end

    def calculatePromotionButtonPosition(self, screen, iPromotionCount):
        yResolution = screen.getYResolution()
        # x=266, y=144
        return (266 - (24 * (iPromotionCount / 6)), yResolution - 164 + (24 * (iPromotionCount % 6)))
    # Mod BUG - Stack Promotions - end

    # Will set the selection button position
    def setResearchButtonPosition(self, szButtonID, iCount):

        # PAE: x+5 and Original modulo: 15
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        xResolution = screen.getXResolution()
# Mod BUG - Bars on single line for higher resolution screens - start
        if xResolution >= 1440: #\
           # and (MainOpt.isShowGGProgressBar() or MainOpt.isShowGPProgressBar()):
            xCoord = 268 + (xResolution - 1440) / 2
            xCoord += 6 + 84
        else:
            xCoord = 264 + (xResolution - 1024)/2
        screen.moveItem(szButtonID, xCoord + 5 + (34 * (iCount % 12)), 0 + (34 * (iCount / 12)), -0.3)
# Mod BUG - Bars on single line for higher resolution screens - end

    # Will set the selection button position
    def setScoreTextPosition(self, szButtonID, iWhichLine):

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        yResolution = screen.getYResolution()
        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
            yCoord = yResolution - 180
        else:
            yCoord = yResolution - 88
        screen.moveItem(szButtonID, 996, yCoord - (iWhichLine * 18), -0.3)

    # Will build the globeview UI
    def updateGlobeviewButtons(self):
        # kInterface = CyInterface()
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        kEngine = CyEngine()
        kGLM = CyGlobeLayerManager()
        # iNumLayers = kGLM.getNumLayers()
        iCurrentLayerID = kGLM.getCurrentLayerID()

        # Positioning things based on the visibility of the globe
        if kEngine.isGlobeviewUp():
            screen.setHelpTextArea(350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH)
        else:
            if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
                screen.setHelpTextArea(350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH)
            else:
                screen.setHelpTextArea(350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH)

        # Set base Y position for the LayerOptions, if we find them
        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
            iY = yResolution - iGlobeLayerOptionsY_Minimal
        else:
            iY = yResolution - iGlobeLayerOptionsY_Regular

        # Hide the layer options ... all of them
        for i in xrange(20):
            szName = "GlobeLayerOption" + str(i)
            screen.hide(szName)

        # Setup the GlobeLayer panel
        # iNumLayers = kGLM.getNumLayers()
        if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
            # set up panel
            if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
                bHasOptions = True
            else:
                bHasOptions = False
                screen.hide("ScoreBackground")
                screen.hide("ScoreBackground2")

            # set up toggle button
            screen.setState("GlobeToggle", True)

            # Set GlobeLayer indicators correctly
            for i in xrange(kGLM.getNumLayers()):
                szButtonID = "GlobeLayer" + str(i)
                screen.setState(szButtonID, iCurrentLayerID == i)

            # Set up options pane
            if bHasOptions:
                kLayer = kGLM.getLayer(iCurrentLayerID)

                iCurY = iY
                iNumOptions = kLayer.getNumOptions()
                iCurOption = kLayer.getCurrentOption()
                iMaxTextWidth = -1
                for iTmp in xrange(iNumOptions):
                    iOption = iTmp  # iNumOptions - iTmp - 1
                    szName = "GlobeLayerOption" + str(iOption)
                    szCaption = kLayer.getOptionName(iOption)
                    if iOption == iCurOption:
                        szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
                    else:
                        szBuffer = "  %s  " % (szCaption)
                    iTextWidth = CyInterface().determineWidth(szBuffer)

                    screen.setText(szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1)
                    screen.show(szName)

                    iCurY -= iGlobeLayerOptionHeight

                    if iTextWidth > iMaxTextWidth:
                        iMaxTextWidth = iTextWidth

                # make extra space
                iCurY -= iGlobeLayerOptionHeight
                iPanelWidth = iMaxTextWidth + 32
                iPanelHeight = iY - iCurY
                iPanelX = xResolution - 14 - iPanelWidth
                iPanelY = iCurY
                screen.setPanelSize("ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight)
                screen.show("ScoreBackground")

        else:
            if iCurrentLayerID != -1:
                kLayer = kGLM.getLayer(iCurrentLayerID)
                if kLayer.getName() == "RESOURCES":
                    screen.setState("ResourceIcons", True)
                else:
                    screen.setState("ResourceIcons", False)

                if kLayer.getName() == "UNITS":
                    screen.setState("UnitIcons", True)
                else:
                    screen.setState("UnitIcons", False)
            else:
                screen.setState("ResourceIcons", False)
                screen.setState("UnitIcons", False)

            screen.setState("Grid", CyUserProfile().getGrid())
            screen.setState("BareMap", CyUserProfile().getMap())
            screen.setState("Yields", CyUserProfile().getYields())
            screen.setState("ScoresVisible", CyUserProfile().getScores())

            screen.hide("InterfaceGlobeLayerPanel")
            screen.setState("GlobeToggle", False)

    # Update minimap buttons
    def setMinimapButtonVisibility(self, bVisible):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        # kInterface = CyInterface()
        kGLM = CyGlobeLayerManager()
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()

        if CyInterface().isCityScreenUp():
            bVisible = False

        kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
        kGlobeButtons = []
        for i in xrange(kGLM.getNumLayers()):
            szButtonID = "GlobeLayer" + str(i)
            kGlobeButtons.append(szButtonID)

        if bVisible:
            if CyEngine().isGlobeviewUp():
                kHide = kMainButtons
                kShow = kGlobeButtons
            else:
                kHide = kGlobeButtons
                kShow = kMainButtons
            screen.show("GlobeToggle")

        else:
            kHide = kMainButtons + kGlobeButtons
            kShow = []
            screen.hide("GlobeToggle")

        for szButton in kHide:
            screen.hide(szButton)

        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
            iY = yResolution - iMinimapButtonsY_Minimal
            iGlobeY = yResolution - iGlobeButtonY_Minimal
        else:
            iY = yResolution - iMinimapButtonsY_Regular
            iGlobeY = yResolution - iGlobeButtonY_Regular

        iBtnX = xResolution - 39
        screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)

        iBtnAdvance = 28
        iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
        if kShow:
            i = 0
            for szButton in kShow:
                screen.moveItem(szButton, iBtnX, iY, 0.0)
                screen.moveToFront(szButton)
                screen.show(szButton)
                iBtnX += iBtnAdvance
                i += 1

    def createGlobeviewButtons(self):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        # xResolution = screen.getXResolution()
        # yResolution = screen.getYResolution()

        # kEngine = CyEngine()
        kGLM = CyGlobeLayerManager()
        # iNumLayers = kGLM.getNumLayers()

        for i in xrange(kGLM.getNumLayers()):
            szButtonID = "GlobeLayer" + str(i)

            kLayer = kGLM.getLayer(i)
            szStyle = kLayer.getButtonStyle()

            if szStyle == 0 or szStyle == "":
                szStyle = "Button_HUDSmall_Style"

            screen.addCheckBoxGFC(szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
            screen.setStyle(szButtonID, szStyle)
            screen.hide(szButtonID)

    def createMinimapButtons(self):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        # xResolution = screen.getXResolution()
        # yResolution = screen.getYResolution()

        screen.addCheckBoxGFC("UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("UnitIcons", "Button_HUDGlobeUnit_Style")
        screen.setState("UnitIcons", False)
        screen.hide("UnitIcons")

        screen.addCheckBoxGFC("Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("Grid", "Button_HUDBtnGrid_Style")
        screen.setState("Grid", False)
        screen.hide("Grid")

        screen.addCheckBoxGFC("BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("BareMap", "Button_HUDBtnClearMap_Style")
        screen.setState("BareMap", False)
        screen.hide("BareMap")

        screen.addCheckBoxGFC("Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("Yields", "Button_HUDBtnTileAssets_Style")
        screen.setState("Yields", False)
        screen.hide("Yields")

        screen.addCheckBoxGFC("ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("ScoresVisible", "Button_HUDBtnRank_Style")
        screen.setState("ScoresVisible", True)
        screen.hide("ScoresVisible")

        screen.addCheckBoxGFC("ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("ResourceIcons", "Button_HUDBtnResources_Style")
        screen.setState("ResourceIcons", False)
        screen.hide("ResourceIcons")

        screen.addCheckBoxGFC("GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
        screen.setStyle("GlobeToggle", "Button_HUDZoom_Style")
        screen.setState("GlobeToggle", False)
        screen.hide("GlobeToggle")

    def handleInput(self, inputClass):
        'Will handle the input for this screen...'
#       BugUtil.debugInput(inputClass)
        # sendModNetMessage -> sends data to GLOBAL GAME AREA (CvEventManager)

# Mod BUG - PLE - start
        # if  inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON or \
            # inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF or \
            # inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            # if self.MainInterfaceInputMap.has_key(inputClass.getFunctionName()):
                # return self.MainInterfaceInputMap.get(inputClass.getFunctionName())(inputClass)
            # if self.MainInterfaceInputMap.has_key(inputClass.getFunctionName() + "1"):
                # return self.MainInterfaceInputMap.get(inputClass.getFunctionName() + "1")(inputClass)
# Mod BUG - PLE - end

# Mod BUG - Raw Yields - start
        if inputClass.getFunctionName().startswith("RawYields"):
            return self.handleRawYieldsButtons(inputClass)
# Mod BUG - Raw Yields - end

        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            # PAE - Great Person Bar - start
            if inputClass.getFunctionName().startswith("GreatPersonBar"):
                pPlayer = gc.getActivePlayer()
                # Zoom to next GP city
                iCity = inputClass.getData1()
                if iCity == -1:
                    pCity, _ = GPUtil.findNextCity()
                else:
                    pCity = pPlayer.getCity(iCity)

                if pCity and not pCity.isNone():
                    CyInterface().selectCity(pCity, False)
                return 1
            # PAE - Great Person Bar - end

            # PAE Taxes Bar
            if inputClass.getFunctionName().startswith("TaxesBar"):
                self.bHideTaxes = not self.bHideTaxes
                self.updateGameDataStrings()
                self.updatePercentButtons()
                return 1

        # Field of View
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_SLIDER_NEWSTOP:
            if bFieldOfView:
                if inputClass.getFunctionName() == self.szSliderId:
                    screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
                    self.iField_View = inputClass.getData() + 1
                    self.setFieldofView(screen, False)
                    self.setFieldofView_Text(screen)
                    MainOpt.setFieldOfView(self.iField_View)
# Mod BUG - field of view slider - end

        # PAE TradeRouteAdvisor Screen
        if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == 10000 and inputClass.getData2() == 1:
            import CvTradeRouteAdvisor
            CvTradeRouteAdvisor.CvTradeRouteAdvisor().interfaceScreen()
            return 1
        if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == 10000 and inputClass.getData2() == 2:
            import CvTradeRouteAdvisor2
            CvTradeRouteAdvisor2.CvTradeRouteAdvisor2().interfaceScreen()
            return 1

        # Initialisierung
        if g_pSelectedUnit:
            iOwner = g_pSelectedUnit.getOwner()
            iUnitID = g_pSelectedUnit.getID()
            pPlot = g_pSelectedUnit.plot()

        if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
            if inputClass.getNotifyCode() == 11:
                iData1 = inputClass.getData1()
                iData2 = inputClass.getData2()
                bOption = inputClass.getOption()

                # Inquisitor
                if iData1 == 665 and iData2 == 665:
                    CyMessageControl().sendModNetMessage(665, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Horse down
                elif iData1 == 666 and iData2 == 666:
                    CyAudioGame().Play2DSound('AS2D_HORSE_DOWN')
                    CyMessageControl().sendModNetMessage(666, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Horse up
                elif iData1 == 667 and iData2 == 667:
                    CyAudioGame().Play2DSound('AS2D_HORSE_UP')
                    CyMessageControl().sendModNetMessage(667, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave -> Bordell / Freudenhaus
                elif iData1 == 668 and iData2 == 668:
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(668, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave -> Gladiator
                elif iData1 == 669 and iData2 == 669:
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(669, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave -> Theater
                elif iData1 == 670 and iData2 == 670:
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(670, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # ID 671 frei

                # Auswanderer / Emigrant
                elif iData1 == 672 and iData2 == 672:
                    CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_SETTLER')
                    CyMessageControl().sendModNetMessage(672, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Stadt aufloesen / disband city
                elif iData1 == 673 and iData2 == 673 and bOption:
                    CyMessageControl().sendModNetMessage(673, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # ID 674 vergeben durch Hunnen-PopUp (CvScreensInterface - popupHunsPayment)

                # ID 675 vergeben durch Revolten-PopUp (CvScreensInterface - popupRevoltPayment)

                # ID 676 vergeben durch freie Unit durch Tech (Kulte)

                # Goldkarren
                elif iData1 == 677:
                    if iData2 == 1:
                        CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(677, iData2, -1, iOwner, iUnitID)

                # ID 678 vergeben durch Provinz-PopUp

                # Sklave -> Schule
                elif iData1 == 679 and iData2 == 679:
                    CyAudioGame().Play2DSound('AS2D_BUILD_UNIVERSITY')
                    CyMessageControl().sendModNetMessage(679, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave -> Manufaktur Nahrung
                elif iData1 == 680 and iData2 == 680:
                    CyAudioGame().Play2DSound('AS2D_BUILD_GRANARY')
                    CyMessageControl().sendModNetMessage(680, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave -> Manufaktur Produktion
                elif iData1 == 681 and iData2 == 681:
                    CyAudioGame().Play2DSound('AS2D_BUILD_FORGE')
                    CyMessageControl().sendModNetMessage(681, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # ID 682 PopUp Vassal03
                # ID 683 PopUp Vassal04
                # ID 684 PopUp Vassal05
                # ID 685 PopUp Vassal06
                # ID 686 PopUp Vassal07
                # ID 687 PopUp Vassal08
                # ID 688 PopUp Vassal09
                # ID 689 PopUp Vassal10
                # ID 690 PopUp Vassal11
                # ID 691 PopUp Vassal12

                # Sklave -> Palast
                elif iData1 == 692 and iData2 == 692:
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(692, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave -> Tempel
                elif iData1 == 693 and iData2 == 693:
                    CyAudioGame().Play2DSound('AS2D_BUILD_TAOIST')
                    CyMessageControl().sendModNetMessage(693, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sklave wird verkauft
                elif iData1 == 694 and iData2 == 694:
                    CyAudioGame().Play2DSound('AS2D_COINS')
                    CyMessageControl().sendModNetMessage(694, iOwner, iUnitID, 0, 0)

                # Unit wird verkauft
                elif iData1 == 695:
                    # Confirmation required
                    CyMessageControl().sendModNetMessage(695, 0, 0, iOwner, iUnitID)

                # Sklave -> Feuerwehr
                elif iData1 == 696 and iData2 == 696:
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(696, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Trojanisches Pferd
                elif iData1 == 697 and iData2 == 697:
                    CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_UNIT')
                    CyMessageControl().sendModNetMessage(697, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # ID 698 vergeben durch freie Unit durch Tech (Religion)

                # ID 699 Kauf einer Edlen Ruestung
                elif iData1 == 699 and bOption:
                    CyAudioGame().Play2DSound('AS2D_COINS')
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(699, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # ID 700
                elif iData1 == 700:
                    CyAudioGame().Play2DSound('AS2D_PILLAGE')
                    CyMessageControl().sendModNetMessage(700, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)


                # ID 701 Kauf des Wellen-Oels
                elif iData1 == 701 and bOption:
                    CyAudioGame().Play2DSound('AS2D_COINS')
                    CyMessageControl().sendModNetMessage(701, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # ID 702 PopUp Vassal Tech
                # ID 703 PopUp Vassal Tech2
                # ID 704 Religionsaustreibung

                # ID 705 Update Veteran Einheit zu neuer Elite Einheit
                # Bsp: Principes or Hastati Veterans -> Triarii
                elif iData1 == 705:
                    CyAudioGame().Play2DSound("AS2D_IF_LEVELUP")
                    CyAudioGame().Play2DSound("AS2D_WELOVEKING")
                    CyMessageControl().sendModNetMessage(705, 0, iData2, iOwner, iUnitID)

                # ID 706 PopUp Renegade City (keep or raze)

                # ID 707 Soeldner anheuern / Mercenaries hire or assign
                elif iData1 == 707 and iData2 == 707:
                    CyMessageControl().sendModNetMessage(707, pPlot.getPlotCity().getID(), -1, -1, iOwner)

                # ID 708-715 Hire/Assign Mercenaries
                # ID 716-717 Mercenary Torture

                # ID 718 Unit Formations (eigenes Widget weiter unten)

                # ID 719 Promotion Trainer Building (Forest 1, Hills1, ...)
                elif iData1 == 719:
                    CyAudioGame().Play2DSound('AS2D_BUILD_BARRACKS')
                    CyMessageControl().sendModNetMessage(719, pPlot.getPlotCity().getID(), iData2, iOwner, iUnitID)

                # ID 720 Legendary Hero can become a Great General
                elif iData1 == 720:
                    CyAudioGame().Play2DSound('AS2D_WELOVEKING')
                    CyMessageControl().sendModNetMessage(720, 0, 0, iOwner, iUnitID)

                # ID 721: 1,4,14: Stallungen, Camel, Elefant, Pferd
                elif iData1 == 721:
                    if iData2 in [1,4,14]:
                        if pPlot.isCity():
                            iCityID = pPlot.getPlotCity().getID()
                        else:
                            iCityID = -1
                    if iData2 == 1:
                        CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_WAR_ELEPHANT')
                        CyMessageControl().sendModNetMessage(721, iCityID, 1, iOwner, iUnitID)
                    elif iData2 == 4:
                        CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_ARABIAN_CAMEL_ARCHER')
                        CyMessageControl().sendModNetMessage(721, iCityID, 2, iOwner, iUnitID)
                    elif iData2 == 14:
                        CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_HORSE_ARCHER')
                        CyMessageControl().sendModNetMessage(721, iCityID, 3, iOwner, iUnitID)

                # ID 722 Piraten-Feature
                # Data2=1: Pirat->Normal, Data2=2: Normal->Pirat
                elif iData1 == 722:
                    if iData2 != 3:
                        CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_GALLEY')
                        CyMessageControl().sendModNetMessage(722, iData2, 0, iOwner, iUnitID)

                # ID 723 EspionageMission Info im TechChooser

                # ID 724 Veteran Unit -> Reservist in city
                elif iData1 == 724:
                    CyAudioGame().Play2DSound("AS2D_GOODY_SETTLER")
                    CyMessageControl().sendModNetMessage(724, pPlot.getPlotCity().getID(), 0, iOwner, iUnitID)

                # ID 725 Reservist -> Veteran Unit
                elif iData1 == 725:
                    CyMessageControl().sendModNetMessage(725, pPlot.getPlotCity().getID(), iOwner, -1, 0)

                # ID 726 Bonusverbreitung (Obsolete)
                # elif iData1 == 726:
                #  CyMessageControl().sendModNetMessage( 726, -1, -1, iOwner, iUnitID )

                # ID 727
                # iData2: Nahrung an Stadt liefern
                # iData2: Nahrung aufsammeln
                elif iData1 == 727:
                    CyAudioGame().Play2DSound("AS2D_BUILD_GRANARY")
                    CyMessageControl().sendModNetMessage(727, pPlot.getPlotCity().getID(), iData2, iOwner, iUnitID)

                # ID 728 Karte zeichnen
                elif iData1 == 728:
                    CyMessageControl().sendModNetMessage(728, -1, -1, iOwner, iUnitID)

                # Sklave -> Library
                elif iData1 == 729:
                    CyAudioGame().Play2DSound('AS2D_BUILD_UNIVERSITY')
                    CyMessageControl().sendModNetMessage(729, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Release slaves
                elif iData1 == 730:
                    CyMessageControl().sendModNetMessage(730, pPlot.getPlotCity().getID(), 0, iOwner, -1)

                # Send Missionary to a friendly city
                elif iData1 == 731:
                    CyMessageControl().sendModNetMessage(731, -1, -1, iOwner, iUnitID)

                # Send Trade merchant into next foreign city (Obsolete)
                # elif iData1 == 732:
                #  CyMessageControl().sendModNetMessage( 732, -1, -1, iOwner, iUnitID )

                # Build Limes PopUp
                elif iData1 == 733:
                    CyMessageControl().sendModNetMessage(733, -1, -1, iOwner, iUnitID)

                # Sklaven zu Feldsklaven oder Bergwerkssklaven
                elif iData1 == 734:
                    if iData2 == 1:
                        if bOption:
                            CyMessageControl().sendModNetMessage(734, pPlot.getPlotCity().getID(), 1, iOwner, iUnitID)
                    elif iData2 == 2:
                        if bOption:
                            CyMessageControl().sendModNetMessage(734, pPlot.getPlotCity().getID(), 2, iOwner, iUnitID)

                # Salae oder Dezimierung
                elif iData1 == 735:
                    if iData2 == 1:
                        if bOption:
                            CyMessageControl().sendModNetMessage(735, 1, 0, iOwner, iUnitID)
                    elif iData2 == 2:
                        if bOption:
                            CyMessageControl().sendModNetMessage(735, 2, 0, iOwner, iUnitID)

                # Handelsposten erstellen
                elif iData1 == 736:
                    CyMessageControl().sendModNetMessage(736, iData2, 0, iOwner, iUnitID)

                # Provinzstatthalter / Tribut
                elif iData1 == 737:
                    CyMessageControl().sendModNetMessage(737, pPlot.getPlotCity().getID(), iOwner, -1, -1)

                # Bonus cultivation (Boggy)
                elif iData1 == 738:
                    # Karren aufladen
                    if bOption:
                        iIsCity = 1
                    else:
                        iIsCity = 0
                    CyMessageControl().sendModNetMessage(738, iOwner, iUnitID, iIsCity, -1)

                # Collect bonus (iData2: 0 = remove, 1 = kaufen)
                elif iData1 == 739:
                    if bOption:
                        CyMessageControl().sendModNetMessage(739, -1, iData2, iOwner, iUnitID)

                # Buy bonus (in city)
                elif iData1 == 740:
                    CyMessageControl().sendModNetMessage(740, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Sell bonus (in city)
                elif iData1 == 741:
                    CyMessageControl().sendModNetMessage(741, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # 742 is used by CvScreensInterface.

                # Automated trade route - choose civ 1
                elif iData1 == 744:
                    CyMessageControl().sendModNetMessage(744, -1, -1, iOwner, iUnitID)

                # 745, 746, 747 are used by CvScreensInterface.

                elif iData1 == 748:
                    # Button von TradeAdvisor2
                    if iData2 != 748:
                        #iOwner = gc.getActivePlayer()
                        iUnitID = iData2
                    CyMessageControl().sendModNetMessage(748, -1, -1, iOwner, iUnitID)

                # 749: Generelle MouseOverInfos lediglich fuer (aktionslose) Buttons

                # 750: Unit Ethnic Info

                # Unit Rang Promo / Upgrade to new unit with new rank
                elif iData1 == 751:
                    # Unit is in capital city
                    if bOption:
                        CyAudioGame().Play2DSound("AS2D_COINS")
                        CyAudioGame().Play2DSound("AS2D_IF_LEVELUP")
                        CyAudioGame().Play2DSound("AS2D_WELOVEKING")
                        CyMessageControl().sendModNetMessage(iData1, -1, -1, iOwner, iUnitID)

                # iData2 0: Bless units (Great General or Hagia Sophia)
                # iData2 1: Better morale (Zeus)
                elif iData1 == 752:
                    if iData2 == 0:
                        CyAudioGame().Play2DSound("AS2D_BUILD_CHRISTIAN")
                    else:
                        CyAudioGame().Play2DSound("AS2D_WELOVEKING")
                    CyMessageControl().sendModNetMessage(iData1, iData2, -1, iOwner, iUnitID)

                # Slave -> Latifundium oder Village
                elif iData1 == 753:
                    CyAudioGame().Play2DSound("AS2D_BUILD_GRANARY")
                    CyMessageControl().sendModNetMessage(iData1, iData2, 0, iOwner, iUnitID)

                # 754: Obsolete Unit text in Tech Screen

                # Sklave -> Manufaktur Nahrung
                elif iData1 == 755 and iData2 == 755:
                    CyAudioGame().Play2DSound("AS2D_BUILD_GRANARY")
                    CyMessageControl().sendModNetMessage(iData1, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Legion Rang Ausbildung / Upgrade to rank via academy/kastell
                elif iData1 == 756:
                    if bOption:
                        CyAudioGame().Play2DSound("AS2D_COINS")
                        CyAudioGame().Play2DSound("AS2D_IF_LEVELUP")
                        CyMessageControl().sendModNetMessage(iData1, -1, -1, iOwner, iUnitID)

                # Statthalter ansiedeln
                elif iData1 == 757:
                    CyAudioGame().Play2DSound("AS2D_WELOVEKING")
                    CyMessageControl().sendModNetMessage(iData1, -1, iOwner, iUnitID, pPlot.getPlotCity().getID())

                # Collect Heldendenkmal (iData2: 0 = collect, 1 = build)
                elif iData1 == 758:
                    CyMessageControl().sendModNetMessage(iData1, iData2, -1, iOwner, iUnitID)

                # Give units morale
                elif iData1 == 759:
                    if iData2 == 2:
                        CyAudioGame().Play2DSound("AS2D_HIT_UNIT")
                    CyAudioGame().Play2DSound("AS2D_WELOVEKING")
                    CyMessageControl().sendModNetMessage(iData1, iData2, -1, iOwner, iUnitID)

                # Slave on plot: head off
                elif iData1 == 760:
                    CyAudioGame().Play2DSound("AS2D_HIT_UNIT")
                    CyMessageControl().sendModNetMessage(iData1, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Slave on plot: win XP
                elif iData1 == 761:
                    if bOption:
                        CyMessageControl().sendModNetMessage(iData1, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Escort for merchant / Begleitschutz
                elif iData1 == 762:
                    CyAudioGame().Play2DSound("AS2D_COINS")
                    CyMessageControl().sendModNetMessage(iData1, iData2, -1, iOwner, iUnitID)

                # Fort/Handelsposten erobern
                elif iData1 == 763:
                    CyAudioGame().Play2DSound("AS2D_CITYCAPTURED")
                    CyMessageControl().sendModNetMessage(iData1, iData2, -1, iOwner, iUnitID)

                # Provinzstatthalter / Tribut
                elif iData1 == 764:
                    CyMessageControl().sendModNetMessage(iData1, iOwner, -1, -1, -1)

                # Wald verbrennen
                elif iData1 == 765:
                    CyAudioGame().Play2DSound("AS2D_PILLAGE")
                    CyMessageControl().sendModNetMessage(iData1, pPlot.getX(), pPlot.getY(), iOwner, iUnitID)

                # Pferdewechsel
                elif iData1 == 766:
                    CyAudioGame().Play2DSound("AS2D_HORSE_UP")
                    CyMessageControl().sendModNetMessage(iData1, iData2, -1, iOwner, iUnitID)

            # Platy ScoreBoard - Start
            if inputClass.getFunctionName() == "ScoreRowPlus":
                self.iScoreRows -= 1
                self.updateScoreStrings()
            elif inputClass.getFunctionName() == "ScoreRowMinus":
                self.iScoreRows += 1
                self.updateScoreStrings()
            elif inputClass.getFunctionName() == "ScoreWidthPlus":
                self.iScoreWidth += 10
                self.updateScoreStrings()
            elif inputClass.getFunctionName() == "ScoreWidthMinus":
                self.iScoreWidth = max(0, self.iScoreWidth - 10)
                self.updateScoreStrings()
            elif inputClass.getFunctionName() == "ScoreHidePoints":
                self.iScoreHidePoints = not self.iScoreHidePoints
                self.updateScoreStrings()
            # Platy ScoreBoard - End

        # ID 718 Unit Formations
        # Zusatz: Eigenes Widget for Formations !!!
        elif inputClass.getButtonType() == WidgetTypes.WIDGET_HELP_PROMOTION:
            if inputClass.getNotifyCode() == 11 and inputClass.getData2() == 718 and inputClass.getOption():
                if g_pSelectedUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
                    CyAudioGame().Play2DSound('AS2D_UNIT_BUILD_GALLEY')
                else:
                    CyAudioGame().Play2DSound('AS2D_BUILD_BARRACKS')
                CyMessageControl().sendModNetMessage(718, 0, inputClass.getData1(), iOwner, iUnitID)


        # PAE, Ramk - Fix jumping in build menu
        if inputClass.getButtonType() in self.buildWidgets:
            if inputClass.getFunctionName() == "BottomButtonContainer":
                screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
                # This just work in fullscreen mode
                # iRow = self.findIconRow( inputClass.getButtonType(), inputClass.getData1() )
                # This change could be False in window mode.
                # if self.secondRowBorder < CyInterface().getMousePos().y:
                #     iRow -= 1

                # Use mouse clicks to estimate border between both rows.
                iRow = self.findIconRow(inputClass.getButtonType(), inputClass.getData1())
                y = CyInterface().getMousePos().y
                self.ySecondRow = max(self.ySecondRow, y)
                if (y - self.ySecondRow + 100) > (self.ySecondRow - y):
                    iRow -= 1
                CyInterface().setCityTabSelectionRow(iRow)
                screen.selectMultiList("BottomButtonContainer", iRow)

        elif inputClass.getData1() == 88000:
            # CITY_TAB replacements
            screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
            iRow = self.cityTabsJumpmarks[inputClass.getData2()]
            CyInterface().setCityTabSelectionRow(iRow)
            screen.selectMultiList("BottomButtonContainer", iRow)

        # PAE, Ramk - End
        return 0

# Begin - From PLE

    def displayHelpHover(self, sKey):
        sText = u"<font=2>%s</font>" % BugUtil.getPlainText(sKey)
        self.displayInfoPane(sText)

    # calculates the height of a text in pixels
    def getTextLines(self, szText):
        szText = mt.removeFonts(szText)
        szText = mt.removeColor(szText)
        szText = mt.removeLinks(szText)
        iNormalLines = 0
        iBulletLines = 0
        lChapters = szText.split('\n')
        sComp = u"%c"%CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
        for lLine in lChapters:
            iWidth = CyInterface().determineWidth(lLine)/(self.CFG_INFOPANE_DX-3)+1
            if lLine.find(sComp) != -1:
                iBulletLines += iWidth
            else:
                iNormalLines += iWidth
        dy = iNormalLines*self.CFG_INFOPANE_PIX_PER_LINE_1 + (iBulletLines)*self.CFG_INFOPANE_PIX_PER_LINE_2 + 20
        return dy

    # base function to display a self sizing info pane
    def displayInfoPane(self, szText):

        self.bInfoPaneActive = True
        self.iInfoPaneCnt += 1
        self.tLastMousePos = (CyInterface().getMousePos().x, CyInterface().getMousePos().y)

        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

        # calculate text size
        dy = self.getTextLines(szText)

        # draw panel
        if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
            y = self.CFG_INFOPANE_Y
        else:
            y = self.CFG_INFOPANE_Y2
        dx = 0
        if CyInterface().isCityScreenUp():
            dx = 260

        screen.addPanel(self.UNIT_INFO_PANE, u"", u"", True, True, \
                        PleOpt.getInfoPaneX() + dx, y - dy, self.CFG_INFOPANE_DX, dy, \
                        PanelStyles.PANEL_STYLE_HUD_HELP)

        # create shadow text
        szTextBlack = localText.changeTextColor(mt.removeColor(szText), gc.getInfoTypeForString("COLOR_BLACK"))

        # display shadow text
        screen.addMultilineText(self.UNIT_INFO_TEXT_SHADOW, szTextBlack, \
                                PleOpt.getInfoPaneX() + dx + 5, y - dy + 5, \
                                self.CFG_INFOPANE_DX - 3, dy - 3, \
                                WidgetTypes.WIDGET_GENERAL, -1, -1, \
                                CvUtil.FONT_LEFT_JUSTIFY)
        # display text
        screen.addMultilineText(self.UNIT_INFO_TEXT, szText, \
                                PleOpt.getInfoPaneX() + dx + 4, y - dy + 4, \
                                self.CFG_INFOPANE_DX - 3, dy - 3, \
                                WidgetTypes.WIDGET_GENERAL, -1, -1, \
                                CvUtil.FONT_LEFT_JUSTIFY)

        return dy

    def checkInfoPane(self, tMousePos):
        if self.bInfoPaneActive and (self.iInfoPaneCnt == (self.iLastInfoPaneCnt+1)):
            if tMousePos.x < self.tLastMousePos[0]-self.iMousePosTol or \
               tMousePos.x > self.tLastMousePos[0]+self.iMousePosTol or \
               tMousePos.y < self.tLastMousePos[1]-self.iMousePosTol or \
               tMousePos.y > self.tLastMousePos[1]+self.iMousePosTol:
                self.hideInfoPane()
                if self.bUnitPromoButtonsActive:
                    self.hideUnitInfoPromoButtons()

    # hides the info pane
    def hideInfoPane(self):
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        screen.hide(self.UNIT_INFO_TEXT)
        screen.hide(self.UNIT_INFO_TEXT_SHADOW)
        screen.hide(self.UNIT_INFO_PANE)
        self.bInfoPaneActive = False
        self.iLastInfoPaneCnt = self.iInfoPaneCnt
# End - from PLE

# Mod BUG - Raw Yields - start
    def handleRawYieldsButtons(self, inputClass):
        iButton = inputClass.getID()
        if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON:
            self.displayHelpHover(RAW_YIELD_HELP[iButton])
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF:
            self.hideInfoPane()
        elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
            global g_bYieldView
            global g_iYieldType
            global g_iYieldTiles
            if iButton == 0:
                g_bYieldView = False
            elif iButton in (1, 2, 3):
                g_bYieldView = True
                g_iYieldType = RawYields.YIELDS[iButton - 1]
            elif iButton in (4, 5, 6):
                g_bYieldView = True
                g_iYieldTiles = RawYields.TILES[iButton - 4]
            else:
                return 0
            CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
            return 1
        return 0
# Mod BUG - Raw Yields - end

    def update(self, fDelta):
        return

    def forward(self):
        if not CyInterface().isFocused() or CyInterface().isCityScreenUp():
            if CyInterface().isCitySelection():
                CyGame().doControl(ControlTypes.CONTROL_NEXTCITY)
            else:
                CyGame().doControl(ControlTypes.CONTROL_NEXTUNIT)

    def back(self):
        if not CyInterface().isFocused() or CyInterface().isCityScreenUp():
            if CyInterface().isCitySelection():
                CyGame().doControl(ControlTypes.CONTROL_PREVCITY)
            else:
                CyGame().doControl(ControlTypes.CONTROL_PREVUNIT)

# Mod BUG - field of view slider - start
    def setFieldofView(self, screen, bDefault):
        if bDefault: # K-Mod ##(not MainOpt.isShowFieldOfView() and not MainOpt.isRememberFieldOfView())
            self._setFieldofView(screen, self.DEFAULT_FIELD_OF_VIEW)
        else:
            self._setFieldofView(screen, self.iField_View)

    def _setFieldofView(self, screen, iFoV):
        if self.iField_View_Prev != iFoV:
            gc.setDefineFLOAT("FIELD_OF_VIEW", float(iFoV))
            self.iField_View_Prev = iFoV

    def setFieldofView_Text(self, screen):
        zsFieldOfView_Text = "%s [%i]" % (self.sFieldOfView_Text, self.iField_View)
        screen.setLabel(self.szSliderTextId, "", zsFieldOfView_Text, CvUtil.FONT_RIGHT_JUSTIFY, self.iX_FoVSlider, self.iY_FoVSlider + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
# Mod BUG - field of view slider - end

    # PAE, Ramk - Position der Bauauftrag-Icons optimieren
    def sortButtons(self, buttons, maxNumIcons):
        if maxNumIcons < 1:
            return
        numRows = len(buttons)
        iRow = 0
        while iRow < numRows:
            # Entferne leere Zeilen
            if not buttons[iRow]:
                del buttons[iRow]
                numRows -= 1
                continue

            # Entfernte None-Eintraege nach ihrer Benutzung und bevor die Laenge der Liste benutzt wird.
            if buttons[iRow][0] is None:
                del buttons[iRow][0]
                continue

            if len(buttons[iRow]) > maxNumIcons:
                if iRow < numRows-1 and (not buttons[iRow+1] or buttons[iRow+1][0] is not None):
                    # Shift to next row
                    buttons[iRow+1] = buttons[iRow][maxNumIcons:] + buttons[iRow+1]
                    del buttons[iRow][maxNumIcons:]
                else:
                    # Insert new row
                    buttons.insert(iRow+1, buttons[iRow][maxNumIcons:])
                    del buttons[iRow][maxNumIcons:]
                    numRows += 1
            iRow += 1

    # Ermittle, ob links weniger genutzt wird als vorhanden ist
    # und gebe es der rechten Seite, falls es dort benoetigt wird.
    def optimalPartition(self, numIconsLeft, numIconsRight, leftButtons, rightButtons):
        if leftButtons:
            maxUsedWidthLeft = max([len(x) for x in leftButtons])
        else:
            maxUsedWidthLeft = 0
        if maxUsedWidthLeft >= numIconsLeft:
            return [numIconsLeft, numIconsRight]
            # return [maxUsedWidthLeft, numIconsRight - ( maxUsedWidthLeft - numIconsLeft )]

        if rightButtons:
            maxUsedWidthRight = max([len(x) for x in rightButtons])
        else:
            maxUsedWidthRight = 0
        if maxUsedWidthRight >= numIconsRight:
            return [maxUsedWidthLeft, numIconsRight + (numIconsLeft - maxUsedWidthLeft)]

        return [numIconsLeft, numIconsRight]

    def insertButtons(self, leftButtons, rightButtons, numIconsLeft, numIcons):
        """ Remark: Structure of objects in *Buttons[i][j]:
         (
          [szButton, WidgetTypes.WIDGET_TRAIN, i, -1, False],
          isBuildable-Flag,
          cityTab-Index
         )
        """
        screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
        emptyButton = "Art/Interface/Buttons/empty.dds"
        lastRow = max(len(leftButtons), len(rightButtons))-1

        for iRow in xrange(lastRow+1):
            iCount = 0
            # Left Icons
            if iRow < len(leftButtons):
                for iconData in leftButtons[iRow]:
                    if iconData is None:
                        continue
                    # Die Liste iconData[0] entspricht fast der Argumentliste von appendMultiListButton.
                    # Es muss aber noch das dritte Argument eingefuegt werden
                    iconData[0].insert(1, iRow)
                    screen.appendMultiListButton("BottomButtonContainer", *(iconData[0]))
                    if not iconData[1]:
                        screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, iconData[0][0])
                    # Manufaktur Einheiten
                    elif iconData[3]:
                        # "Art/Interface/Buttons/Unitoverlay/PAE_unitoverlay_promo.dds"
                        screen.attachButtonGFC ("BottomButtonContainer", "", "", WidgetTypes.WIDGET_GENERAL, iRow, iCount)
                        screen.enableMultiListPulse("BottomButtonContainer", True, iRow, iCount) # Pie: double unit prod (manufactories)
                    iCount += 1

            # Insert Dummy icon on empty positions. Add extra column to separate both groups.
            while iCount < numIconsLeft:
                screen.appendMultiListButton("BottomButtonContainer", emptyButton, iRow, WidgetTypes.WIDGET_GENERAL, 99999, 99999, False)
                screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, emptyButton)
                iCount += 1

            # Right Icons
            if iRow < len(rightButtons):
                for iconData in rightButtons[iRow]:
                    if iconData is None:
                        continue
                    if len(iconData[0]) != 5:  # Ursache fuer teilweise falsche Listenlaenge unbekannt.
                        continue
                    iconData[0].insert(1, iRow)
                    screen.appendMultiListButton("BottomButtonContainer", *(iconData[0]))
                    if not iconData[1]:
                        screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, iconData[0][0])
                    iCount += 1

            # Insert Dummy icon on empty positions to fill up whole row
            if iRow != lastRow:
                while iCount < numIcons:
                    screen.appendMultiListButton("BottomButtonContainer", emptyButton, iRow, WidgetTypes.WIDGET_GENERAL, 99999, 99999, False)
                    screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, emptyButton)
                    iCount += 1

    def findCityTabRow(self, buttons, cityTabIndex):
        for iRow in xrange(len(buttons)):
            for iconData in buttons[iRow]:
                if iconData is None:
                    continue
                if iconData[2] == cityTabIndex:
                    return iRow
                # Just test the first icon in each line
                break
        # index not found
        return len(buttons)

    def findIconRow(self, buildType, index):
        """
        # Achtung, in iconData[0] wird in der insertButtons-Methode
        # vorne ein Element eingefuegt. Das verschiebt Listenelemente nach hinten.
        """
        offset = 0
        if buildType == WidgetTypes.WIDGET_TRAIN:
            buttons = self.iconsLeft
        else:
            buttons = self.iconsRight
            if self.m_iNumMenuButtons < 16:
                offset = len(self.iconsLeft)

        for iRow in xrange(len(buttons)):
            for iconData in buttons[iRow]:
                if iconData is None:
                    continue
                if iconData[0][3] == index and iconData[0][2] == buildType:
                    return iRow+offset
        return 0

    def updateCityTabs(self, screen):
        """PAE, Ramk:
        Die urspruenglichen CITY_TAB-Buttons koennen nur auf die Zeilen 0,1 und 2 springen und
        diese stehen immer fuer Einheiten, Gebaeude und Wunder.
        Daher sind die Buttons durch eigene (WIDGET_GENERAL) ausgetauscht worden.
        """
        iBtnX = self.xResolution - 324
        iBtnY = self.yResolution - 94
        iBtnWidth = 24
        iBtnAdvance = 24
        iBtnX = screen.getXResolution() - 324
        iBtnY = screen.getYResolution() - 94

        #screen.setButtonGFC( "CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, jumpMarks[0], -1, ButtonStyles.BUTTON_STYLE_STANDARD )
        screen.setButtonGFC("CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_GENERAL, 88000, 0, ButtonStyles.BUTTON_STYLE_STANDARD)
        screen.setStyle("CityTab0", "Button_HUDJumpUnit_Style")
        #screen.hide( "CityTab0" )

        iBtnY += iBtnAdvance
        #screen.setButtonGFC( "CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, jumpMarks[1], -1, ButtonStyles.BUTTON_STYLE_STANDARD )
        screen.setButtonGFC("CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_GENERAL, 88000, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
        screen.setStyle("CityTab1", "Button_HUDJumpBuilding_Style")
        #screen.hide( "CityTab1" )

        iBtnY += iBtnAdvance
        #screen.setButtonGFC( "CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, jumpMarks[2], -1, ButtonStyles.BUTTON_STYLE_STANDARD )
        screen.setButtonGFC("CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_GENERAL, 88000, 2, ButtonStyles.BUTTON_STYLE_STANDARD)
        screen.setStyle("CityTab2", "Button_HUDJumpWonder_Style")
        #screen.hide( "CityTab2" )
# End PAE
