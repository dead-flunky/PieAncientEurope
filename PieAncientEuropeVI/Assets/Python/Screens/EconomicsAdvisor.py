## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
                                FontTypes, NotifyCode, WidgetTypes, PanelStyles,
                                CyInterface, InterfaceDirtyBits, CyGame,
                                CyGInterfaceScreen, CommerceTypes, PopupStates,
                                ButtonStyles, YieldTypes)
# import PyHelpers
import CvUtil
# import ScreenInput
import CvScreenEnums
import BugDll
import BugUtil
import PlayerUtil
import TradeUtil
# TODO remove
# DEBUG code for Python 3 linter
unicode = str
xrange = range

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class EconomicsAdvisor:

    def __init__(self):
        self.SCREEN_NAME = "FinanceAdvisor"
        self.DEBUG_DROPDOWN_ID =  "FinanceAdvisorDropdownWidget"
        self.WIDGET_ID = "FinanceAdvisorWidget"
        self.WIDGET_HEADER = "FinanceAdvisorWidgetHeader"
        self.EXIT_ID = "FinanceAdvisorExitWidget"
        self.BACKGROUND_ID = "FinanceAdvisorBackground"
        self.X_SCREEN = 500
        self.Y_SCREEN = 396
        self.W_SCREEN = 1024
        self.H_SCREEN = 768
        self.Y_TITLE = 12
        self.BORDER_WIDTH = 4
        self.PANE_HEIGHT = 450
        self.PANE_WIDTH = 283
        self.X_LEFT_PANEL = 50
        self.X_MIDDLE_PANEL = 373
        self.X_RIGHT_PANEL = 696
        self.Y_TOP_PANEL = 90
        self.H_TOP_PANEL = 100
        self.Y_LOCATION = 230
        self.Y_SPACING = 30
        self.TEXT_MARGIN = 15
        self.Z_BACKGROUND = -2.1
        self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
        self.DZ = -0.2
        #self.X_EXIT = 994
        self.X_EXIT = self.W_SCREEN - 30
        #self.Y_EXIT = 726
        self.Y_EXIT = self.H_SCREEN - 42

        self.nWidgetCount = 0

    def getScreen(self):
        return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.FINANCE_ADVISOR)

    def interfaceScreen (self):

        self.iActiveLeader = CyGame().getActivePlayer()

        # player = gc.getPlayer(self.iActiveLeader)

        screen = self.getScreen()
        if screen.isActive():
            return
        screen.setRenderInterfaceOnly(True);
        screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

# # Flunky - Economics Screen Resolution - start
# Easy to do, but why? The narrow screen shows all there is
#         if screen.getXResolution() > 1024:
#             self.W_SCREEN = screen.getXResolution() - 60
#         else:
#             self.W_SCREEN = 1024

#         # Set the background and exit button, and show the screen
#         screen.setDimensions((screen.getXResolution() - self.W_SCREEN) / 2, screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
# # Flunky - Economics Screen Resolution - end

        # Set the background and exit button, and show the screen
        screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

        screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
        screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

        screen.showWindowBackground(False)
        screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

        # Header...
        screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        if (CyGame().isDebugMode()):
            self.szDropdownName = self.DEBUG_DROPDOWN_ID
            screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
            for j in xrange(gc.getMAX_CIV_PLAYERS()):
                if (gc.getPlayer(j).isAlive()):
                    screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )
        self.drawContents()

    def drawContents(self):
        self.deleteAllWidgets()

        self.drawFinance()

    def drawFinance(self):
        screen = self.getScreen()
        # Header...
        screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_ECONOMICS_ADVISOR_FINANCE_TAB", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        player = gc.getPlayer(self.iActiveLeader)

        # numCities = player.getNumCities()

        # K-Mod - I've changed these costs to include inflation.
        inflationFactor = 100+player.getInflationRate()
        totalUnitCost = (player.calculateUnitCost() * inflationFactor + 50)/100
        totalUnitSupply = (player.calculateUnitSupply() * inflationFactor + 50)/100
        totalMaintenance = (player.getTotalMaintenance() * inflationFactor + 50)/100
        totalCivicUpkeep = (player.getCivicUpkeep([], False) * inflationFactor + 50)/100

        # totalPreInflatedCosts = player.calculatePreInflatedCosts()
        totalInflatedCosts = player.calculateInflatedCosts()
        goldCommerce = player.getCommerceRate(CommerceTypes.COMMERCE_GOLD)
        # if (not player.isCommerceFlexible(CommerceTypes.COMMERCE_RESEARCH)):
            # goldCommerce += player.calculateBaseNetResearch()
        gold = player.getGold()
        goldFromCivs = player.getGoldPerTurn()
        goldPerTurn = player.calculateGoldRate()

        szTreasuryPanel = self.getNextWidgetName()
        screen.addPanel(szTreasuryPanel, u"", "", True, True, self.X_LEFT_PANEL, self.Y_TOP_PANEL, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.X_LEFT_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_MAIN )
        szText = localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (gold, )).upper()
        if gold < 0:
            if goldPerTurn != 0:
                if gold + goldPerTurn >= 0:
                    szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", goldPerTurn)
                elif goldPerTurn >= 0:
                    szText += BugUtil.getText("TXT_KEY_MISC_POS_WARNING_GOLD_PER_TURN", goldPerTurn)
                else:
                    szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", goldPerTurn)
        else:
            if goldPerTurn != 0:
                if goldPerTurn >= 0:
                    szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", goldPerTurn)
                elif gold + goldPerTurn >= 0:
                    szText += BugUtil.getText("TXT_KEY_MISC_NEG_WARNING_GOLD_PER_TURN", goldPerTurn)
                else:
                    szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", goldPerTurn)
        screen.setLabel(self.getNextWidgetName(), szTreasuryPanel, u"<font=4>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, (self.X_LEFT_PANEL + self.PANE_WIDTH + self.X_RIGHT_PANEL)/2, self.Y_TOP_PANEL + self.H_TOP_PANEL/2 - self.Y_SPACING/2, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_HELP_FINANCE_GOLD_RESERVE, -1, -1 )

        szCommercePanel = self.getNextWidgetName()
        screen.addPanel(szCommercePanel, u"", "", True, True, self.X_LEFT_PANEL, self.Y_LOCATION, self.PANE_WIDTH, self.PANE_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )
        screen.setLabel(self.getNextWidgetName(), "Background",  u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_COMMERCE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH/2, self.Y_LOCATION + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        szIncomePanel = self.getNextWidgetName()
        screen.addPanel(szIncomePanel, u"", "", True, True, self.X_MIDDLE_PANEL, self.Y_LOCATION, self.PANE_WIDTH, self.PANE_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )
        screen.setLabel(self.getNextWidgetName(), "Background",  u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_INCOME_HEADER", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH/2, self.Y_LOCATION + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        szExpensePanel = self.getNextWidgetName()
        screen.addPanel(szExpensePanel, u"", "", True, True, self.X_RIGHT_PANEL, self.Y_LOCATION, self.PANE_WIDTH, self.PANE_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )
        screen.setLabel(self.getNextWidgetName(), "Background",  u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_EXPENSES_HEADER", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH/2, self.Y_LOCATION + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        # Commerce
        yLocation  = self.Y_LOCATION
        iCommerce = 0

        # sum all worked tiles' commerce yields for player
        # move to MapUtil?
        iWorkedTileCount = 0
        iWorkedTiles = 0
        for city in PlayerUtil.playerCities(player):
            if not city.isDisorder():
                for i in xrange(gc.getNUM_CITY_PLOTS()):
                    plot = city.getCityIndexPlot(i)
                    if plot and not plot.isNone() and plot.hasYield():
                        if city.isWorkingPlot(plot):
                            iWorkedTileCount += 1
                            iWorkedTiles += plot.getYield(YieldTypes.YIELD_COMMERCE)

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_WORKED_TILES", (iWorkedTileCount,)) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iWorkedTiles) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        iCommerce += iWorkedTiles

        # trade
        iDomesticTrade, _, iForeignTrade, _ = TradeUtil.calculateTradeRoutes(player)

        if iDomesticTrade > 0:
            if TradeUtil.isFractionalTrade():
                iDomesticTrade //= 100
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_DOMESTIC_TRADE", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT,
                            *BugDll.widget("WIDGET_HELP_FINANCE_DOMESTIC_TRADE", self.iActiveLeader, 1) )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iDomesticTrade) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT,
                            *BugDll.widget("WIDGET_HELP_FINANCE_DOMESTIC_TRADE", self.iActiveLeader, 1) )
            iCommerce += iDomesticTrade

        if iForeignTrade > 0:
            if TradeUtil.isFractionalTrade():
                iForeignTrade //= 100
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_FOREIGN_TRADE", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT,
                            *BugDll.widget("WIDGET_HELP_FINANCE_FOREIGN_TRADE", self.iActiveLeader, 1) )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iForeignTrade) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT,
                            *BugDll.widget("WIDGET_HELP_FINANCE_FOREIGN_TRADE", self.iActiveLeader, 1) )
            iCommerce += iForeignTrade

        # corporations
        iCorporations = 0
        for city in PlayerUtil.playerCities(player):
            if not city.isDisorder():
                iCorporations += city.getCorporationYield(YieldTypes.YIELD_COMMERCE)

        if iCorporations > 0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iCorporations) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            iCommerce += iCorporations

        # specialists
        iSpecialists = 0
        for city in PlayerUtil.playerCities(player):
            if not city.isDisorder():
                for eSpec in xrange(gc.getNumSpecialistInfos()):
                    iSpecialists += player.specialistYield(eSpec, YieldTypes.YIELD_COMMERCE) * (city.getSpecialistCount(eSpec) + city.getFreeSpecialistCount(eSpec))

        if iSpecialists > 0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_SPECIALISTS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iSpecialists) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            iCommerce += iSpecialists

        # buildings
        iTotalCommerce = player.calculateTotalYield(YieldTypes.YIELD_COMMERCE)
        # buildings includes 50% capital bonus for Bureaucracy civic
        iBuildings = iTotalCommerce - iCommerce
        if iBuildings > 0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iBuildings) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            iCommerce += iBuildings

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_BUG_FINANCIAL_ADVISOR_COMMERCE", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iCommerce) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        # Slider percentages

        yLocation += 0.5 * self.Y_SPACING
        for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
            eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES

            if (player.isCommerceFlexible(eCommerce)):
                yLocation += self.Y_SPACING
                screen.setButtonGFC(self.getNextWidgetName(), u"", "", self.X_LEFT_PANEL + self.TEXT_MARGIN, int(yLocation) + self.TEXT_MARGIN, 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
                screen.setButtonGFC(self.getNextWidgetName(), u"", "", self.X_LEFT_PANEL + self.TEXT_MARGIN + 24, int(yLocation) + self.TEXT_MARGIN, 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )

                szText = u"<font=3>" + gc.getCommerceInfo(eCommerce).getDescription() + u" (" + unicode(player.getCommercePercent(eCommerce)) + u"%)</font>"
                screen.setLabel(self.getNextWidgetName(), "Background",  szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN + 50, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
                szRate = u"<font=3>" + unicode(player.getCommerceRate(CommerceTypes(eCommerce))) + u"</font>"
                screen.setLabel(self.getNextWidgetName(), "Background", szRate, CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


        # K-Mod. Show gold rate if it hasn't been shown already
        if (not player.isCommerceFlexible(CommerceTypes.COMMERCE_GOLD)):
            yLocation += self.Y_SPACING
            szText = u"<font=3>" + gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getDescription() + u" (" + unicode(player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)) + u"%)</font>"
            screen.setLabel(self.getNextWidgetName(), "Background",  szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_LEFT_PANEL + self.TEXT_MARGIN + 50, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            szCommerce = u"<font=3>" + unicode(goldCommerce) + u"</font>"
            screen.setLabel(self.getNextWidgetName(), "Background", szCommerce, CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

        # Income
        yLocation  = self.Y_LOCATION
        iTaxRate = player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)

        multipliers = []
        for eBldg in xrange(gc.getNumBuildingInfos()):
            info = gc.getBuildingInfo(eBldg)
            iMultiplier = info.getCommerceModifier(CommerceTypes.COMMERCE_GOLD)
            if iMultiplier > 0:
                multipliers.append([eBldg, iMultiplier, 0, 0.0])

        iBuildingCount = 0
        iHeadquartersCount = 0
        iShrinesCount = 0
        fTaxes = 0.0
        fBuildings = 0.0
        fHeadquarters = 0.0
        fShrines = 0.0
        fCorporations = 0.0
        fSpecialists = 0.0
        iWealthCount = 0
        fWealth = 0.0
        eWealth = gc.getInfoTypeForString("PROCESS_WEALTH")
        # ignores
        #   CyCity.getReligionCommerce() -- excludes shrines
        #   CyPlayer.getFreeCityCommerce()
        #   CyPlayer.getSpecialistExtraCommerce() * (CyCity.getSpecialistPopulation() + CyCity.getNumGreatPeople())
        for city in PlayerUtil.playerCities(player):
            if not city.isDisorder():
                fCityTaxes = city.getYieldRate(YieldTypes.YIELD_COMMERCE) * iTaxRate / 100.0
                fTaxes += fCityTaxes

                fCityBuildings = 0.0
                fCityHeadquarters = 0.0
                fCityShrines = 0.0
                for eBldg in xrange(gc.getNumBuildingInfos()):
                    iCount = city.getNumRealBuilding(eBldg)
                    if iCount > 0:
                        iBuildingGold = city.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_GOLD, eBldg)
                        if iBuildingGold > 0:
                            info = gc.getBuildingInfo(eBldg)
                            if info.getFoundsCorporation() != -1:
                                fCityHeadquarters += iBuildingGold
                                iHeadquartersCount += 1
                            elif info.getGlobalReligionCommerce() != -1:
                                fCityShrines += iBuildingGold
                                iShrinesCount += 1
                            else:
                                fCityBuildings += iBuildingGold
                                iBuildingCount += iCount
                fBuildings += fCityBuildings
                fHeadquarters += fCityHeadquarters
                fShrines += fCityShrines

                fCityCorporations = city.getCorporationCommerce(CommerceTypes.COMMERCE_GOLD)
                fCorporations += fCityCorporations

                fCitySpecialists = city.getSpecialistCommerce(CommerceTypes.COMMERCE_GOLD)
                fSpecialists += fCitySpecialists

                fCityWealth = 0.0
                if city.isProductionProcess() and city.getProductionProcess() == eWealth:
                    fCityWealth = city.getProductionToCommerceModifier(CommerceTypes.COMMERCE_GOLD) * city.getYieldRate(YieldTypes.YIELD_PRODUCTION) / 100.0
                    fWealth += fCityWealth
                    iWealthCount += 1

                # buildings don't multiply wealth
                fCityTotel = fCityTaxes + fCityBuildings + fCityHeadquarters + fCityCorporations + fCitySpecialists
                for entry in multipliers:
                    eBldg, iMultiplier, _, _ = entry
                    iCount = city.getNumRealBuilding(eBldg)
                    if iCount > 0:
                        entry[2] += iCount
                        entry[3] += iCount * fCityTotel * iMultiplier / 100.0

        # K-Mod, karadoc
        # The 'total minus taxes' was wrong. We don't need to use that anyway
        # I've changed the 'taxes' output to use fTaxes instead of goldcommerce - totalminustaxes
        ##
        #iTotalMinusTaxes = int(fBuildings) + int(fCorporations) + int(fSpecialists) + int(fWealth)
        #for _, _, _, fGold in multipliers:
        #    iTotalMinusTaxes += int(fGold)

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TAXES", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fTaxes)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        if fBuildings > 0.0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()) + " (%d)</font>" % iBuildingCount, CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fBuildings)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        if fHeadquarters > 0.0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CORPORATION_HEADQUARTERS", ()) + " (%d)</font>" % iHeadquartersCount, CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fHeadquarters)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        if fCorporations > 0.0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fCorporations)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        if fShrines > 0.0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_RELIGIOUS_SHRINES", ()) + " (%d)</font>" % iShrinesCount, CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fShrines)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        if fSpecialists > 0.0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_CONCEPT_SPECIALISTS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT,
                             *BugDll.widget("WIDGET_HELP_FINANCE_SPECIALISTS", self.iActiveLeader, 1))
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fSpecialists)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT,
                             *BugDll.widget("WIDGET_HELP_FINANCE_SPECIALISTS", self.iActiveLeader, 1))

        for eBldg, iMultiplier, iCount, fGold in multipliers:
            if iCount > 0 and fGold > 0.0:
                fAverage = fGold / iCount
                szDescription = gc.getBuildingInfo(eBldg).getDescription() + u" " + localText.getText("TXT_KEY_BUG_FINANCIAL_ADVISOR_BUILDING_COUNT_AVERAGE", (iCount, BugUtil.formatFloat(fAverage, 2)))
                yLocation += self.Y_SPACING
                screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szDescription + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
                screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fGold)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        if fWealth > 0.0 and iWealthCount > 0:
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_PROCESS_WEALTH", ()) + " (%d)</font>" % iWealthCount, CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(int(fWealth)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

        iIncome = goldCommerce
        if (goldFromCivs > 0):
            yLocation += self.Y_SPACING
            szText = unicode(goldFromCivs) + " : " + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_PER_TURN", ())
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_PER_TURN", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(goldFromCivs) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
            iIncome += goldFromCivs

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_INCOME", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MIDDLE_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iIncome) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_MIDDLE_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )


        # Expenses
        yLocation = self.Y_LOCATION
        iExpenses = 0

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_UNITCOST", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_UNIT_COST, self.iActiveLeader, 1)
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(totalUnitCost) + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_UNIT_COST, self.iActiveLeader, 1)
        iExpenses += totalUnitCost

        yLocation += self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_UNITSUPPLY", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_AWAY_SUPPLY, self.iActiveLeader, 1)
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(totalUnitSupply) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_AWAY_SUPPLY, self.iActiveLeader, 1)
        iExpenses += totalUnitSupply

        yLocation += self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_MAINTENANCE", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CITY_MAINT, self.iActiveLeader, 1)
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(totalMaintenance) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CITY_MAINT, self.iActiveLeader, 1)
        iExpenses += totalMaintenance

        yLocation += self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_CIVICS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CIVIC_UPKEEP, self.iActiveLeader, 1)
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(totalCivicUpkeep) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CIVIC_UPKEEP, self.iActiveLeader, 1)
        iExpenses += totalCivicUpkeep

        if (goldFromCivs < 0):
            yLocation += self.Y_SPACING
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_COST_PER_TURN", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
            screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(-goldFromCivs) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
            iExpenses -= goldFromCivs

        # yLocation += self.Y_SPACING
        # iInflation = totalInflatedCosts - totalPreInflatedCosts
        # screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>(" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_INFLATION", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS, self.iActiveLeader, 1)
        # screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iInflation) + ")</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS, self.iActiveLeader, 1)
        # iExpenses += iInflation

        yLocation += 1.5 * self.Y_SPACING
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_EXPENSES", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_RIGHT_PANEL + self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        #screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(iExpenses) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
        screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + unicode(totalInflatedCosts) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANEL + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation + self.TEXT_MARGIN, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS, self.iActiveLeader, 1 )

        return 0

    # returns a unique ID for a widget in this screen
    def getNextWidgetName(self):
        szName = self.WIDGET_ID + str(self.nWidgetCount)
        self.nWidgetCount += 1
        return szName

    def deleteAllWidgets(self):
        screen = self.getScreen()
        i = self.nWidgetCount - 1
        while (i >= 0):
            self.nWidgetCount = i
            screen.deleteWidget(self.getNextWidgetName())
            i -= 1

        self.nWidgetCount = 0

    # Will handle the input for this screen...
    def handleInput (self, inputClass):
        'Calls function mapped in FinanceAdvisorInputMap'
        iNotifyCode = inputClass.getNotifyCode()
        if (iNotifyCode == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
            screen = self.getScreen()
            iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
            self.iActiveLeader = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
            self.drawContents()
        return 0

    def update(self, fDelta):
        if (CyInterface().isDirty(InterfaceDirtyBits.Financial_Screen_DIRTY_BIT) == True):
            CyInterface().setDirty(InterfaceDirtyBits.Financial_Screen_DIRTY_BIT, False)
            self.drawContents()
        return
