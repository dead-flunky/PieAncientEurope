## BugAdvisorOptionsTab
##
## Tab for the BUG Advisor Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugAdvisorOptionsTab(BugOptionsTab.BugOptionsTab):
    "BUG General Options Screen Tab"

    def __init__(self, screen):
        BugOptionsTab.BugOptionsTab.__init__(self, "Advisors", "Advisors")

    def create(self, screen):
        tab = self.createTab(screen)
        panel = self.createMainPanel(screen)
        left, right = self.addTwoColumnLayout(screen, panel, panel, True)

        self.addLabel(screen, left, "Foreign_Advisor", "Foreign [F4]:")
        comboBox = "Advisors_ComboBoxEFA"
        screen.attachHBox(left, comboBox)
        # self.addCheckbox(screen, comboBox, "Advisors__EFAGlanceTab")
        # self.addTextDropdown(screen, None, comboBox, "Advisors__EFAGlanceAttitudes")
        # self.addCheckbox(screen, left, "Advisors__EFAImprovedInfo")
        # self.addCheckbox(screen, left, "Advisors__EFADealTurnsLeft")
        #self.addCheckbox(screen, left, "MiscHover__TechTradeDenial")
        #self.addCheckbox(screen, left, "MiscHover__BonusTradeDenial")

        self.addLabel(screen, left, "Military_Advisor", "Military [F5]:")
        self.addCheckbox(screen, left, "Advisors__BugMA")


        self.addLabel(screen, left, "Technology_Advisor", "Technology [F6]:")
        self.addCheckbox(screen, left, "Advisors__GPTechPrefs")
        #self.addCheckbox(screen, center, "MiscHover__SpedUpTechs")
        
        # Flunky PAE hide tech screen options (enabled)
        # self.addCheckbox(screen, center, "Advisors__WideTechScreen")
        # self.addCheckbox(screen, center, "Advisors__ShowTechEra")

        self.addLabel(screen, left, "Religious_Advisor", "Religion [F7]:")
        # self.addCheckbox(screen, left, "Advisors__BugReligiousTab")
        # self.addTextDropdown(screen, left, left, "Advisors__ShowReligions", True)

        #self.addLabel(screen, center, "Victory_Conditions", "Victory [F8]:")
        #self.addCheckbox(screen, center, "Advisors__BugVictoriesTab")
        #self.addCheckbox(screen, center, "Advisors__BugMembersTab")

        # K-Mod, info stuff moved from center panel to right
        self.addLabel(screen, right, "Info_Screens", "Info [F9]:")
        self.addCheckbox(screen, right, "Advisors__BugGraphsTab")
        self.addCheckbox(screen, right, "Advisors__BugGraphsLogScale")
        self.addCheckbox(screen, right, "Advisors__BugStatsTab")
        self.addCheckbox(screen, right, "Advisors__NonZeroStatsOnly") # K-Mod
        self.addCheckbox(screen, right, "Advisors__BugInfoWonders")
        self.addCheckbox(screen, right, "Advisors__BugInfoWondersPlayerColor", True)


        self.addLabel(screen, right, "Sevopedia", "Sevopedia [F12]:")
        self.addCheckbox(screen, right, "Advisors__Sevopedia")
        self.addCheckbox(screen, right, "Advisors__SevopediaSortItemList")

        self.addSpacer(screen, right, "Advisors_Tab")
