import re

def OnPluginInstall():
    win = world.GetPluginID
    height = world.GetInfo(280)
    width = 400
    world.WindowCreate(win, 0, 0, width, height, 6, 0, 0x000000)
    world.WindowFont(win, "f", "Bitstream Vera Sans Mono", 11, True, False, False, False, 1, 0)

def OnPluginClose():
    pass

def OnPluginConnect():
    pass

def OnPluginEnable():
    pass

def OnPluginDisable():
    pass

def OnPluginPacketReceived(sText):
    return sText

def OnPluginSend(sText):
    return True

def OnPluginSent(sText):
    pass

