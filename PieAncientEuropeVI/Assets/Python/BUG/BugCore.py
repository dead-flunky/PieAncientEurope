## BugCore
##
## Provides a top-level Game that manages the Mods and their Options.
##
## TODO
##   - Fix syntax error in _createParameterizedAccessorPair()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptions
import BugUtil


## Game and Mods

class Game(object):
    """Manages a set of Mods."""

    def __init__(self):
        self._mods = {}
        self._emptyMods = {}
        self._screens = {}
        self._inited = False

    def _createMod(self, mod_id):
        'create mod with id if not yet initialized'
        if self._inited:
            raise BugUtil.ConfigError("cannot create mod '%s' after initialization" % mod_id)
        else:
            return self._newMod(mod_id)

    def _newMod(self, mod_id):
        'new mod with id'
        mod = Mod(mod_id)
        self._emptyMods[mod_id] = mod
        self._mods[mod_id] = mod
        return mod

    def _getMod(self, mod_id):
        'get mod by id'
        if mod_id in self._mods:
            return self._mods[mod_id]
        if not self._inited:
            BugUtil.info("BugCore - creating uninitialized mod %s", mod_id)
            return self._newMod(mod_id)

        raise BugUtil.error("BugCore - invalid mod %s", mod_id)

    def _addMod(self, mod):
        'add mod to list if not yet initialized'
        mod_id = mod._getID()
        if self._inited:
            BugUtil.warn("BugCore - cannot add mod %s post-init", mod_id)
        elif mod_id in self._emptyMods:
            if not mod._inited:
                BugUtil.error("BugCore - mod %s not initialized", mod_id)
            del self._emptyMods[mod_id]
        elif mod_id in self._mods:
            BugUtil.error("BugCore - mod %s already exists", mod_id)
        else:
            self._mods[mod_id] = mod

    def _removeMod(self, mod_id):
        'remove mod from list'
        if mod_id in self._mods:
            del self._mods[mod_id]

    def _initDone(self):
        'init done'
        if self._inited:
            BugUtil.warn("BugCore - game already initialized")
        else:
            for mod in self._emptyMods.values():
                mod_id = mod._getID()
                if mod._inited:
                    BugUtil.warn("BugCore - mod %s not added; adding", mod_id)
                    del self._emptyMods[mod_id]
                else:
                    BugUtil.warn("BugCore - mod %s not initialized; removing", mod_id)
                    self._removeMod(mod_id)
            self._inited = True

    def __getattr__(self, mod_id):
        """Returns the Mod with the given ID."""
        if not mod_id.startswith("_"):
            mod = self._getMod(mod_id)
            if mod is not None:
                return mod
        raise AttributeError(mod_id)

    def _getScreen(self, screen_id):
        """Returns the screen with the given ID."""
        return self._screens[screen_id]

    def _addScreen(self, screen):
        """Add the screen."""
        self._screens[screen.id] = screen


class Mod(object):
    """Provides Option accessors."""

    def __init__(self, mod_id):
        self._id = mod_id
        self._options = {}
        self._inited = False

    def _getID(self):
        'returns the mod\'s ID'
        return self._id

    def qualify(self, qual_id):
        "Returns a fully qualified option ID by inserting the mod's ID if necessary."
        return BugOptions.qualify(self._id, qual_id)

    def _addOption(self, option):
        'adds an option to the list of options'
        self._options[option.getID()] = option

    def _hasOption(self, optionId):
        return self.qualify(optionId) in self._options

    def _getOption(self, optionId):
        try:
            return self._options[self.qualify(optionId)]
        except KeyError:
            raise BugUtil.ConfigError("Option %s not found in mod %s", optionId, self._id)

    def _initDone(self):
        if self._inited:
            BugUtil.warn("BugCore - mod already initialized")
        else:
            self._inited = True

    def __getattr__(self, attr_id):
        """Returns the Option with the given ID or False for is/getters
        and None for setters that don't exist."""
        if not attr_id.startswith("_"):
            # Try bare option
            if self._hasOption(attr_id):
                return self._getOption(attr_id)
            # If not yet initialized, return False for getters and setters
            if not self._inited:
                if attr_id.startswith("get") or attr_id.startswith("is"):
                    return lambda *ignored: False
                if attr_id.startswith("set"):
                    return lambda *ignored: False
        raise AttributeError(attr_id)


    def _createParameterizedAccessorPair(self, optionId, getter=None, setter=None, values=None):
        'createParameterizedAccessorPair'
        optionId = BugOptions.qualify(self._id, optionId)
        if getter:
            if values is None:
                def get_fun(*args):
                    'getter for plain option'
                    option = self._getOption(optionId % args)
                    if option.isColor():
                        return option.getColor()
                    return option.getValue()
            else:
                def get_fun(*args):
                    'getter for option in values'
                    option = self._getOption(optionId % args)
                    return option.getValue() in values
            setattr(self, getter, get_fun)

        if setter:
            def set_fun(value, *args):
                'setter for option'
                option = self._getOption(optionId % args)
                option.setValue(value)
            setattr(self, setter, set_fun)


game = Game()

def initDone():
    'initDone'
    game._initDone()
