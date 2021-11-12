## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
                                FontTypes, CivilopediaPageTypes, YieldTypes,
                                WidgetTypes, PanelStyles, TableStyles,
                                CyGameTextMgr)
import CvUtil
# import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaFeature:
        "Civilopedia Screen for Terrain Features"

        def __init__(self, main):
                self.iFeature = -1
                self.top = main

                self.X_ICON_PANE = 20 + 30
                self.Y_ICON_PANE = 70 + 30
                self.W_ICON_PANE = 433
                self.H_ICON_PANE = 210

                self.X_ICON = 73 + 30
                self.Y_ICON = 130 + 30
                self.W_ICON = 100
                self.H_ICON = 100
                self.ICON_SIZE = 64

                self.X_STATS_PANE = 215 + 30
                self.Y_STATS_PANE = 150 + 20
                self.W_STATS_PANE = 230
                self.H_STATS_PANE = 120

                self.X_SPECIAL_PANE = 50
                self.Y_SPECIAL_PANE = 320
                self.W_SPECIAL_PANE = 690
                self.H_SPECIAL_PANE = 350

        # Screen construction function
        def interfaceScreen(self, iFeature):

                self.iFeature = iFeature

                self.top.deleteAllWidgets()

                screen = self.top.getScreen()

                bNotActive = (not screen.isActive())
                if bNotActive:
                        self.top.setPediaCommonWidgets()

                # Header...
                szHeader = u"<font=4b>" + gc.getFeatureInfo(self.iFeature).getDescription().upper() + u"</font>"
                szHeaderId = self.top.getNextWidgetName()
                screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Top
                screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE, -1)

                if self.top.iLastScreen        != CvScreenEnums.PEDIA_FEATURE or bNotActive:
                        self.placeLinks(True)
                        self.top.iLastScreen = CvScreenEnums.PEDIA_FEATURE
                else:
                        self.placeLinks(False)

                # Icon
                screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
                    self.X_ICON_PANE, self.Y_ICON_PANE, self.W_ICON_PANE, self.H_ICON_PANE, PanelStyles.PANEL_STYLE_BLUE50)
                screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
                    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
                screen.addDDSGFC(self.top.getNextWidgetName(), gc.getFeatureInfo(self.iFeature).getButton(),
                    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#                screen.addDDSGFC(self.top.getNextWidgetName(), gc.getFeatureInfo(self.iFeature).getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_GENERAL, self.iFeature, -1 )

                self.placeStats()

                self.placeSpecial()

                return

        def placeStats(self):

                screen = self.top.getScreen()

                panelName = self.top.getNextWidgetName()
                screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
#                screen.addPanel( panelName, "", "", True, True, self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, PanelStyles.PANEL_STYLE_EMPTY )
                screen.enableSelect(panelName, False)

                for k in xrange(YieldTypes.NUM_YIELD_TYPES):
                        iYieldChange = gc.getFeatureInfo(self.iFeature).getYieldChange(k)
                        if (iYieldChange != 0):
                                if (iYieldChange > 0):
                                        sign = "+"
                                else:
                                        sign = ""

                                szYield = (u"%s: %s%i " % (gc.getYieldInfo(k).getDescription().upper(), sign, iYieldChange))

                                screen.appendListBoxString(panelName, u"<font=4>" + szYield + (u"%c" % gc.getYieldInfo(k).getChar()) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
#                                screen.attachTextGFC(panelName, "", szYield + (u"%c" % gc.getYieldInfo(k).getChar()), FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        def placeSpecial(self):

                screen = self.top.getScreen()

                panelName = self.top.getNextWidgetName()
                screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

                listName = self.top.getNextWidgetName()
                screen.attachListBoxGFC(panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY)
                screen.enableSelect(listName, False)

                szSpecialText = CyGameTextMgr().getFeatureHelp(self.iFeature, True)
                splitText = string.split( szSpecialText, "\n" )
                for special in splitText:
                        if len( special ) != 0:
                                screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

        def placeLinks(self, bRedraw):

                screen = self.top.getScreen()

                if bRedraw:
                        screen.clearListBoxGFC(self.top.LIST_ID)

                # sort resources alphabetically
                listSorted=[(0,0)]*gc.getNumFeatureInfos()
                for j in xrange(gc.getNumFeatureInfos()):
                        listSorted[j] = (gc.getFeatureInfo(j).getDescription(), j)
                listSorted.sort()

                iSelected = 0
                i = 0
                for iI in xrange(gc.getNumFeatureInfos()):
                        if (not gc.getFeatureInfo(listSorted[iI][1]).isGraphicalOnly()):
                                if bRedraw:
                                        screen.appendListBoxString( self.top.LIST_ID, listSorted[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, listSorted[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY )
                                if listSorted[iI][1] == self.iFeature:
                                        iSelected = i
                                i += 1

                screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

        # Will handle the input for this screen...
        def handleInput (self, inputClass):
                return 0
