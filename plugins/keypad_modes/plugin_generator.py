import re

class DefaultMode(object):
    def __init__(self):
        pass
    def pluginWantsToSend(self, sText):
        return True

class ShipMode(object):
    def __init__(self):
        pass
    def pluginWantsToSend(self, sText):
        if re.match("north", sText):
            world.send("fore")
        elif re.match("south", sText):
            world.send("aft")
        elif re.match("east", sText):
            world.send("starboard")
        elif re.match("west", sText):
            world.send("port")
        elif re.match("up", sText):
            world.send("above")
        elif re.match("down", sText):
            world.send("below")
        else:
            return True
        return False

mode = DefaultMode()

def setShipMode(*args):
    global mode
    mode = ShipMode()
    world.note("Ship mode active")

def setDefaultMode(*args):
    global mode
    mode = DefaultMode()
    world.note("Default mode active")

def OnPluginSend(sText):
    return mode.pluginWantsToSend(sText)
