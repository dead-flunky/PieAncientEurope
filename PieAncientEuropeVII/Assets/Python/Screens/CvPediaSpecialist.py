## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
                                FontTypes, CivilopediaPageTypes,
                                WidgetTypes, PanelStyles,
                                CyGameTextMgr, TableStyles)
import CvUtil
# import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaSpecialist:
        "Civilopedia Screen for Specialists"

        def __init__(self, main):
                self.iSpecialist = -1
                self.top = main

                self.X_MAIN_PANEL = 20
                self.Y_MAIN_PANEL = 80
                self.W_MAIN_PANEL = 250
                self.H_MAIN_PANEL = 250

                self.W_ICON = 100
                self.H_ICON = 100
                self.X_ICON = self.X_MAIN_PANEL + (self.W_MAIN_PANEL - self.W_ICON) / 2
                self.Y_ICON = self.Y_MAIN_PANEL + (self.H_MAIN_PANEL - self.H_ICON) / 2
                self.ICON_SIZE = 64

                self.X_SPECIAL = self.X_MAIN_PANEL + self.W_MAIN_PANEL + 40
                self.Y_SPECIAL = self.Y_MAIN_PANEL
                self.W_SPECIAL = 420
                self.H_SPECIAL = self.H_MAIN_PANEL

                self.X_TEXT = self.X_MAIN_PANEL
                self.Y_TEXT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL + 26
                self.W_TEXT = 755
                self.H_TEXT = 343

        # Screen construction function
        def interfaceScreen(self, iSpecialist):

                self.iSpecialist = iSpecialist

                self.top.deleteAllWidgets()

                screen = self.top.getScreen()

                bNotActive = (not screen.isActive())
                if bNotActive:
                        self.top.setPediaCommonWidgets()

                # Header...
                szHeader = u"<font=4b>" + gc.getSpecialistInfo(self.iSpecialist).getDescription().upper() + u"</font>"
                szHeaderId = self.top.getNextWidgetName()
                screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Top
                screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST, -1)

                if self.top.iLastScreen        != CvScreenEnums.PEDIA_SPECIALIST or bNotActive:
                        self.placeLinks(True)
                        self.top.iLastScreen = CvScreenEnums.PEDIA_SPECIALIST
                else:
                        self.placeLinks(False)

                # Icon
                screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
                    self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_BLUE50)
                screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
                    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
                screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpecialistInfo(self.iSpecialist).getButton(),
                    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#                screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
#                    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_BLUE50)
#                screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpecialistInfo(self.iSpecialist).getButton(),
#                    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

                self.placeSpecial()
                self.placeText()

        def placeSpecial(self):

                screen = self.top.getScreen()

                panelName = self.top.getNextWidgetName()
                screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_YIELDS", ()), "", True, False,
                                 self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )

                listName = self.top.getNextWidgetName()
                screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
                screen.enableSelect(listName, False)

                szSpecialText = CyGameTextMgr().getSpecialistHelp(self.iSpecialist, True)
### Anzeige der Geburtspunkte Great Person (von Kathy)
                iGreatPersonClass = gc.getSpecialistInfo(self.iSpecialist).getGreatPeopleUnitClass()
                if iGreatPersonClass > -1:
                   szText = gc.getUnitClassInfo(iGreatPersonClass).getDescription()
                   szSpecialText += " (" + szText + ")"
### ----------------------------------
                splitText = string.split(szSpecialText, "\n")
                for special in splitText:
                        if len( special ) != 0:
                                screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

        def placeText(self):

                screen = self.top.getScreen()

                panelName = self.top.getNextWidgetName()
                screen.addPanel( panelName, "", "", True, True,
                                 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )

                # PAE Upgrade: Strategy Text in Pedia
                szText = u""
                if len(gc.getSpecialistInfo(self.iSpecialist).getStrategy()) > 0:
                        sz = gc.getSpecialistInfo(self.iSpecialist).getStrategy()
                        if not "TXT_KEY" in sz:
                           szText = localText.getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
                           szText += sz
                           szText += u"\n\n"
                           #szText += localText.getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())

                szText += gc.getSpecialistInfo(self.iSpecialist).getCivilopedia()
                screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

        def placeLinks(self, bRedraw):

                screen = self.top.getScreen()

                if bRedraw:
                        screen.clearListBoxGFC(self.top.LIST_ID)

                # sort Improvements alphabetically
                listSorted=[(0,0)]*gc.getNumSpecialistInfos()
                for j in xrange(gc.getNumSpecialistInfos()):
                        listSorted[j] = (gc.getSpecialistInfo(j).getDescription(), j)
                listSorted.sort()

                i = 0
                iSelected = 0
                for iI in xrange(gc.getNumSpecialistInfos()):
                        if (not gc.getSpecialistInfo(iI).isGraphicalOnly()):
                                if bRedraw:
                                        screen.appendListBoxString(self.top.LIST_ID, listSorted[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, listSorted[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY )
                                if listSorted[iI][1] == self.iSpecialist:
                                        iSelected = i
                                i += 1

                screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

        # Will handle the input for this screen...
        def handleInput (self, inputClass):
                return 0
